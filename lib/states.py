import pyglet

from tdgl import part
from tdgl.gl import *
from tdgl import lighting
from tdgl.viewpoint import OrthoView, SceneView

from rooms import Room

class State(part.Group):
    def __init__(self,name="",**kw):
        super(State,self).__init__(name,*kw)
        self.build_parts(**kw)
        
    def resize(self,w,h):
        self.size = w,h
        for p in self.contents:
            if hasattr(p,"resize"):
                p.resize(w,h)

class GameState(State):
    def __init__(self,name="",**kw):
        super(GameState,self).__init__(name,**kw)

    def build_parts(self,**kw):
        sv = SceneView("scene",[])
        sv.append(Room("Hroom","hotelroom1.txt"))
        sv.camera.look_at((0,0,0),1)
        sv.camera.look_from_spherical(10,-90,30)
        sv.camera.look_from_spherical(10,-50,30,1000)
        sv.camera.step(1)
        self.light = lighting.claim_light()
        with sv.compile_style():
            glEnable(GL_LIGHTING)
        lighting.light_position(self.light,(10,10,10,0))
        lighting.light_colour(self.light,(1,1,1,1))
        lighting.light_switch(self.light,True)
        self.append(sv)
        
