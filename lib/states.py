import pyglet

from pyglet.window import key

from tdgl import part, picking, lighting
from tdgl.gl import *
from tdgl.viewpoint import OrthoView, SceneView
from tdgl.panel import LabelPanel, SelectTextPanel

from rooms import Room
import story

from math import cos,radians,sin

MOVESPEED = 600

class Player:
    def __init__(self,pos,angle,height = 1.5):
        self.pos = pos
        self.angle = angle
        self.lasta = angle
        self.height = height
        self.walking = 0
        self.look = 0
    def move_cam(self,cam,instant=False):
        ms = 1 if instant else MOVESPEED
        cam.look_at((self.pos[0],self.pos[1],self.height),ms)
        cam.look_from_spherical(self.look*45,self.angle,1,ms)
    def walk(self,mag,walkable_tiles):
        a = self.angle if self.angle%90 == 0 else self.lasta
        x,y = self.pos
        x += int(cos( radians(a) )*mag)
        y += int(sin( radians(a) )*mag)
        if (x,y) in walkable_tiles:
            self.pos = (x,y)
    def turn(self,mag):
        self.lasta = self.angle
        self.angle += mag

# Warning! Monkey-patch
def __repr__Hit(ob):
    return "Hit({0})".format(ob.__dict__)
picking.Hit.__repr__ = __repr__Hit

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
    
    def pick_at(self,x,y):
        """Pick topmost object at x,y"""
        picking.start(x,y,1,1)
        self.draw('PICK')
        objects = picking.end()
        if objects:
            minz,maxz,label = objects[0]
            self.pick(label,x,y)
            print objects


class GameState(State):
    def __init__(self,name="",room="hotelroom1",start="begin",**kw):
        self.light = lighting.claim_light()
        self.room = room
        self.start = start
        self.action_menu = None
        super(GameState,self).__init__(name,**kw)

    def __del__(self):
        lighting.release_light(self.light)

    def setup_style(self):
        lighting.setup()

    def build_parts(self,**kw):
        sv = SceneView("scene",[],
                       _vport=(0.0, 128, 1.0, 1.0), 
                       _ClearColor=(0.3, 0.3, 0.3, 1.0),
                       _perspective_angle=30.0)
        hroom = Room("Room",self.room+".txt")
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
        self.append(sv)
        ov = OrthoView("itembar", [],
                       _vport=(0.0,0.0,1.0,128),
                       _ClearColor=(0.1, 0, 0, 1.0),
                       _left=0, _right=1024, _top=128, _bottom=0)
        self.append(ov)
        with ov.compile_style():
            glDisable(GL_LIGHTING)
        tpanel = LabelPanel("text", "You enter the room.", _pos=(512,64,0))
        ov.append(tpanel)
        menus = OrthoView("menus",[], _vport=(0,0,1024,768),
                          _left=0, _right=1024, _top=768, _bottom=0)
        with menus.compile_style():
            glDisable(GL_LIGHTING)
        self.append(menus)
    
    def key_press(self,sym):
        wt = self["Room"].walktiles
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
        
    def popup_menu(self, objname, x, y):
        self.action_options = story.menu_for_object(objname)
        m = SelectTextPanel("actionmenu",
                            self.action_options, _pos=(x,y,0),
                            _bg = (0.2, 0.2, 0.0, 1.0))
        m.prepare()
        self.hide_menu()
        self.action_menu = m
        self["menus"].append(m)
        self.action_object = objname
        print objname, m, self.action_options

    def choose_from_menu(self, objname, n):
        action = self.action_options(n)
        story.action_for_object(self, self.action_object, action)
        self.action_options = []
        self.action_menu._expired = True
        self.action_menu = None

    def hide_menu(self):
        if self.action_menu:
            self.action_menu._expired = True
            self.action_menu = None

    def pick(self,label, x, y):
        if type(label.target) == tuple:
            prop,name,piece = label.target
            tpan = self["text"]
            if name != "":
                obj = self[name]
                tpan.text = obj.text 
                tpan.prepare()
                if getattr(obj,"door",None):
                    text,room,gate = obj.door.split(",")
                    print text
                    self.quit = (room,gate)
                else:
                    self.popup_menu(name,x,y)
            else:
                self.hide_menu()
        elif label.target.__class__ == SelectTextLabel:
            self.choose_from_menu(label.selected)
            

        
    def click(self,x,y):
        self.pick_at(x,y)
