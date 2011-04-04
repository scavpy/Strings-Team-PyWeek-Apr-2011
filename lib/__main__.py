"""
Main. Creates the game window and runs the app
"""


import pyglet

from tdgl.gl import tdgl_usual_setup

from game import GameWin

def main():
    pyglet.clock.set_fps_limit(60)

    win = GameWin(width=1024,height=768)
    tdgl_usual_setup()
    pyglet.app.run()
