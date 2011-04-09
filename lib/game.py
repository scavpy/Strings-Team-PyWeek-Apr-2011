"""
State-manager.
"""

import pyglet
from pyglet.window import key

from tdgl.gl import *

from states import *
import story

class GameWin(pyglet.window.Window):
    def __init__(self,**kw):
        super(GameWin,self).__init__(**kw)
        pyglet.clock.schedule(self.on_tick)
        self.newstate = None
        story.chapter_setup(None, 1)
        self.state = GameState(room="Chapter1",start="begin")

    def on_tick(self,secs):
        ms = secs*1000
        if self.state.quit:
            self.change_room(*self.state.quit)
        self.state.step(ms)

    def on_draw(self):
        if self.newstate:
            self.state = self.newstate
            self.newstate = None
            self.state.resize(*self.size)
            self.state.restyle()
        self.clear()
        tdgl_draw_parts(self.state)

    def on_resize(self,w,h):
        self.size = w,h
        self.state.resize(w,h)
        self.state.restyle()
        return True

    def on_key_press(self,sym,mod):
        self.state.key_press(sym)

    def on_mouse_press(self,x,y,button,mods):
        if button == 1:
            self.state.click(x,y)

    def change_room(self,room,gate):
        self.newstate = GameState(room=room,start=gate)
