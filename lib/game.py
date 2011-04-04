"""
State-manager.
"""

import pyglet

from tdgl.gl import *

from states import *

class GameWin(pyglet.window.Window):
    def __init__(self,**kw):
        super(GameWin,self).__init__(**kw)
        pyglet.clock.schedule(self.on_tick)

        self.all_states = {
            "game":GameState(),
                }
        self.state = self.all_states["game"]
    def change_state(self,new_state,refresh=False):
        """ Changes to a new state. If refresh, a new state is made."""
        self.state = self.all_states[new_state]

    def on_tick(self,secs):
        ms = secs*1000
        self.state.step(ms)

    def on_draw(self):
        self.clear()
        tdgl_draw_parts(self.state)

    def on_resize(self,w,h):
        self.state.resize(w,h)
        self.state.restyle()
        return True
