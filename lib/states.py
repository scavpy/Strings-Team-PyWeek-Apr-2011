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
    "bg":(0.0,0.0,0.0,1.0),
    "bd":(1.0,1.0,1.0,1.0),
    "border":2,
    "bg_radius":8,
    "bd_radius":8,
    "bg_round":4,
    "bd_round":4,
    "bg_margin":(5,5),
    "bd_margin":(5,5),
    }

class Player:
    def __init__(self,pos,angle,height = 1.2):
        self.pos = pos
        self.angle = angle
        self.lasta = angle
        self.height = height
        self.walking = 0
        self.look = 0
        self.stuck = False
    def move_cam(self,cam,instant=False):
        ms = 1 if instant else MOVESPEED
        cam.look_at((self.pos[0],self.pos[1],self.height),ms)
        cam.look_from_spherical(self.look*45,self.angle,1,ms)
    def walk(self,mag,walkable_tiles):
        if not self.stuck:
            a = self.angle if self.angle%90 == 0 else self.lasta
            x,y = self.pos
            x += int(cos( radians(a) )*mag)
            y += int(sin( radians(a) )*mag)
            if (x,y) in walkable_tiles:
                self.pos = (x,y)
    def turn(self,mag):
        self.lasta = self.angle
        self.angle += mag

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
    
    def pick(self,label):
        pass
    
    def pick_at(self,x,y):
        """Pick topmost object at x,y"""
        picking.start(x,y,1,1)
        self.draw('PICK')
        objects = picking.end()
        if objects:
            minz,maxz,label = objects[0]
            self.pick(label)


class GameState(State):
    def __init__(self,name="",room="hotelroom1",start="begin",**kw):
        self.light = lighting.claim_light()
        self.room = room
        self.start = start
        self.speaking = False
        self.options = None
        super(GameState,self).__init__(name,**kw)

    def __del__(self):
        lighting.release_light(self.light)

    def setup_style(self):
        lighting.setup()

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
        self.player = Player((ppos[0],ppos[1]),ppos[2])
        sv.append(hroom)
        self.camera = sv.camera
        self.player.move_cam(self.camera,instant=True)
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
        tpanel = LabelPanel("text", "You go outside" if outdoors else "You enter the room", 
                            _text_width=1000, _pos=(512,64,0))
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
                self.player.look = max(self.player.look-1,-1)
            elif sym == key.END:
                self.player.look = min(self.player.look+1,1)
            self.player.move_cam(self.camera)
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
            n = 0
            for o in options:
                p = LabelPanel("opt%d"%n,"%d. %s"%(n+1,o),style = bubble_style, _text_width=800, _pos=(512,200-n*40,0))
                self["speech"].append(p)
                n += 1

    def close_speech(self,choice=None):
        self.speaking = False
        self["speech"].contents = []
        if choice:
            c,o = self.options
            self.options = None
            story.action_for_object(self,c,choice)

    def pick(self,label):
        prop,name,piece = label.target
        tpan = self["text"]
        if name != "":
            obj = self[name]
            if not story.action_for_object(self, name, "click"):
                tpan.text = obj.text 
                tpan.prepare()
        
    def click(self,x,y):
        if not self.speaking:
            self.pick_at(x,y)
        elif self.speaking and not self.options:
            self.close_speech()
