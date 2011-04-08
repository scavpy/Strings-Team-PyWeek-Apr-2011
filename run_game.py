import pyglet.resource

import os, sys
if __name__ == "__main__":
    here = os.path.abspath(os.path.dirname(__file__))
    os.chdir(here)
    libdir = os.path.join(here, 'lib')
    sys.path.insert(0, libdir)

    pyglet.resource.path = ["data", "data/models", "data/icons"]
    pyglet.resource.reindex()

    import lib.__main__
    lib.__main__.main()
