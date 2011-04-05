import pyglet

from pyglet.window import key

from tdgl import part
from tdgl.gl import *
from tdgl import lighting
from tdgl.viewpoint import OrthoView, SceneView

from rooms import Room

from math import cos,radians,sin

class Player:
    def __init__(self,pos,angle,height = 1.5):
        self.pos = pos
        self.angle = angle
        self.height = height
        self.walking = 0
        self.lookup = False
    def move_cam(self,cam,instant=False):
        ms = 1 if instant else 800
        cam.look_at((self.pos[0],self.pos[1],self.height),ms)
        cam.look_from_spherical(10-self.lookup*40,self.angle,1,ms)
    def walk(self,mag):
        a = self.angle
        x,y = self.pos
        x += cos( radians(a) )*mag
        y += sin( radians(a) )*mag
        self.pos = (x,y)
    def turn(self,mag):
        self.angle += mag

class State(part.Group):
    def __init__(self,name="",**kw):
        super(State,self).__init__(name,*kw)
        self.build_parts(**kw)
        
    def resize(self,w,h):
        self.size = w,h
        for p in self.contents:
            if hasattr(p,"resize"):
                p.resize(w,h)

    def key_press(self,sym):
        pass

class GameState(State):
    def __init__(self,name="",room="hotelroom1",start="begin",**kw):
        self.light = lighting.claim_light()
        self.room = room
        self.start = start
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
    
    def key_press(self,sym):
        if sym == key.UP:
            self.player.walk(-2)
        elif sym == key.DOWN:
            self.player.walk(2)
        elif sym == key.RIGHT:
            self.player.turn(-90)
        elif sym == key.LEFT:
            self.player.turn(90)
        elif sym == key.HOME:
            self.player.lookup = not self.player.lookup
        self.player.move_cam(self.camera)
