import pyglet

from pyglet.window import *

from tdgl import part, picking, lighting
from tdgl.gl import *
from tdgl.viewpoint import OrthoView, SceneView
from tdgl.panel import LabelPanel

from rooms import Room
import story

from math import cos,radians,sin

MOVESPEED = 600

bubble_style = {
    "bg":(0.0,0.0,0.0,0.9),
    "bd":(1.0,1.0,1.0,0.5),
    "border":2,
    "bg_radius":10,
    "bd_radius":8,
    "bg_round":4,
    "bd_round":4,
    "bg_margin":(8,8),
    "bd_margin":(5,5),
    }

class Player:
    def __init__(self,pos,angle,height,camera):
        self.pos = pos
        self.angle = angle
        self.height = height
        self.walking = 0
        self.look = 0
        self.stuck = False
        self.deltas = {
            0:(1,0), 45:(1,1), 90:(0,1), 135:(-1,1),
            180:(-1,0), 225:(-1,-1), 270:(0,-1), 315:(1,-1),
            -315:(1,1), -270:(0,1), -225:(-1,1),
            -180:(-1,0), -135:(-1,-1), -90:(0,-1), -45:(1,-1),
            }
        self.camera = camera
        self.speed = 1
        self.move_cam(True)

    def move_cam(self,instant=False):
        ms = 1 if instant else MOVESPEED * max(self.speed, 1)
        cam = self.camera
        cam.look_at((self.pos[0],self.pos[1],self.height),ms)
        cam.look_from_spherical(self.look*45,self.angle,1,ms)

    def walk(self,mag,walkable_tiles):
        if not self.stuck:
            dx, dy = self.deltas[self.angle]
            x,y = self.pos
            x += dx * mag
            y += dy * mag
            if (x,y) in walkable_tiles:
                self.pos = (x,y)
                self.speed = mag * (1.4 if (dx and dy) else 1)
        self.lasta = self.angle
        self.move_cam()

    def turn(self,mag):
        if self.angle in (360, -360):
            self.angle = 0
            self.camera.look_from_spherical(self.look*45, 0,1,0)
            self.camera.step(1)
        self.angle = self.angle + mag
        self.speed = 1
        self.move_cam()

    def look_up(self):
        self.look = max(self.look-1,-1)
        self.speed = 1
        self.move_cam()

    def look_down(self):
        self.look = min(self.look+1, 1)
        self.speed = 1
        self.move_cam()

class State(part.Group):
    def __init__(self,name="",**kw):
        super(State,self).__init__(name,*kw)
        self.quit = False
        self.build_parts(**kw)
        
    def resize(self,w,h):
        self.size = w,h
        for p in self.contents:
            if hasattr(p,"resize"):
                p.resize(w,h)

    def key_press(self,sym):
        pass
    
    def pick(self,label,x,y):
        pass

    def nothing_near(self):
        pass
    
    def pick_at(self,x,y):
        """Pick topmost object at x,y"""
        picking.start(x,y,1,1)
        self.draw('PICK')
        objects = picking.end()
        if objects:
            minz,maxz,label = objects[0]
            if minz > 1.6:
                self.nothing_near()
            else:
                self.pick(label,x,y)


class GameState(State):
    def __init__(self,name="",room="Chapter1",start="begin",**kw):
        self.light = lighting.claim_light()
        self.room = room
        self.start = start
        self.speaking = False
        self.options = None
        self.quit_after_fade_out = None
        super(GameState,self).__init__(name,**kw)
        story.action_for_object(self, room, "begin")

    def __del__(self):
        lighting.release_light(self.light)

    def setup_style(self):
        lighting.setup()

    def step(self, ms):
        super(GameState, self).step(ms)
        lighting.step(ms)
        if self.quit_after_fade_out:
            if lighting.conditions[GL_LIGHT0 + self.light].finished():
                self.quit = self.quit_after_fade_out
                self.quit_after_fade_out = None

    def build_parts(self,**kw):
        menus = OrthoView("menus",[], _vport=(0,0,1024,768))
        with menus.compile_style():
            glDisable(GL_LIGHTING)
        sv = SceneView("scene",[],
                       _vport=(0.0, 128, 1.0, 1.0), 
                       _ClearColor=(0.3, 0.3, 0.3, 1.0),
                       _perspective_angle=30.0)
        hroom = Room("Room",self.room+".txt")
        outdoors = "outdoors" in hroom.flags
        ppos = hroom.gates.get(self.start,(0,0,0))
        sv.append(hroom)
        self.camera = sv.camera
        self.player = Player((ppos[0],ppos[1]),ppos[2], 1.2, self.camera)
        with sv.compile_style():
            glEnable(GL_LIGHTING)
        lighting.two_side(True)
        lighting.local_viewer(True)
        lighting.light_position(self.light,(hroom.width/2, hroom.height/2, 2,1))
        lighting.light_colour(self.light,(1,1,0.9,1))
        lighting.light_switch(self.light,True)
        if not outdoors:
            lighting.light_attenuation(self.light, (0.01,))
        self.append(sv)
        ov = OrthoView("itembar", [],
                       _vport=(0.0,0.0,1.0,128),
                       _ClearColor=(0.1, 0, 0, 1.0),
                       _left=0, _right=1024, _top=128, _bottom=0)
        speechport = OrthoView("speech", [],
                               _ClearColor=None,
                               _left=0, _right=1024, _top=768, _bottom=0)
        with ov.compile_style():
            glDisable(GL_LIGHTING)
        self.append(ov)
        self.append(speechport)
        tpanel = LabelPanel("text", hroom.name, 
                            _text_width=1000, _pos=(512,48,0))
        ov.append(tpanel)
    
    def key_press(self,sym):
        wt = self["Room"].walktiles
        if not self.speaking:
            if sym == key.UP:
                self.player.walk(-2,wt)
            elif sym == key.DOWN:
                self.player.walk(2,wt)
            elif sym == key.RIGHT:
                self.player.turn(-45)
            elif sym == key.LEFT:
                self.player.turn(45)
            elif sym == key.HOME:
                self.player.look_up()
            elif sym == key.END:
                self.player.look_down()
        elif self.speaking and self.options:
            s = key.symbol_string(sym).strip("_")
            try:
                n = int(s)
            except ValueError:
                return
            if n <= len(self.options[1]):
                self.close_speech(choice=n)
        
    def open_speech(self,conv,text,options):
        self.speaking = True
        b = LabelPanel("talktext", text, style = bubble_style, _text_width=800, _pos=(512,384,0))
        self["speech"].append(b)
        if options:
            self.options = (conv,options)
            for n,o in enumerate(options):
                p = LabelPanel("opt%d"%n,"%d. %s"%(n+1,o),style = bubble_style, _text_width=800, _pos=(512,200-n*55,0))
                self["speech"].append(p)


    def close_speech(self,choice=None):
        self.speaking = False
        self["speech"].contents = []
        if choice:
            c,o = self.options
            self.options = None
            story.action_for_object(self,c,choice)

    def fade_to(self, fcolour, room, gate):
        print fcolour, room, gate
        self.quit_after_fade_out = room, gate
        lighting.light_colour(self.light, fcolour, 5000)

    def footer_text(self, text):
        tpan = self["text"]
        tpan.text = text
        tpan.prepare()

    def nothing_near(self):
        self.player.walk(-2, self["Room"].walktiles)
        self.footer_text("you can't touch things that are too far away")

    def pick(self,label,x,y):
        prop,name,piece = label.target
        text = self["Room"].name
        if name != "":
            obj = self[name]
            if obj.text:
                text = obj.text
            story.action_for_object(self, name, "click")
        self.footer_text(text)
        
    def click(self,x,y):
        if not self.speaking:
            self.pick_at(x,y)
        elif self.speaking and not self.options:
            self.close_speech()
