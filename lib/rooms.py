import pyglet

from tdgl import objpart, part, animator, panel
from math import atan2, degrees

import data

class PropPart(objpart.ObjPart):
    _default_style = {
        "obj-pieces":None,
        "obj-filename":None,
        "mat-filename":None,
        }
    def __init__(self, name='', **kw):
        super(PropPart, self).__init__(name, **kw)
        self.anim = animator.Mutator(self._geom)

    def step(self, ms):
        self.anim.step(ms)

    def turn_to_angle(self, angle, ms):
        self.anim.change('angle', angle, ms)

    def turn_to_face(self, other, ms):
        wx,wy,wz = self.pos
        x,y,z = other.pos
        theta = atan2(y - wy, x - wx)
        self.turn_to_angle(degrees(theta), ms)

class ImagePanel(panel.Panel):
    _default_style = panel.Panel._default_style.copy()
    _default_style.update(dict(
            bg=(1,1,1,1),
            border=0, bd=None))
    _default_geom = panel.Panel._default_geom.copy()
    _default_geom.update(dict(size=(512,512)))
    def __init__(self, name, image, **kw):
        super(ImagePanel, self).__init__(name, **kw)
        self.setstyle("texture", image)

    def content_size(self):
        return self.getgeom("size")

class Room(part.Group):
    def __init__(self,name,fname,**kw):
        super(Room,self).__init__(name,(),**kw)
        self.width = 0
        self.height = 0
        self.key = {}
        self.gates = {}
        self.data = []
        self.flags = set()
        self.walktiles = set()
        self.loadfile(fname)
        self.buildparts(**kw)

    def loadfile(self,fname):
        mode = "reading"
        prop = {}
        roomdata = data.load(fname)
        lines = roomdata.readlines()
        for L in lines:
            L = L.strip()
            if not L:
                continue
            if L.startswith("/"):
                if mode == "object":
                    self.add_prop(prop)
                    prop = {}
                mode = "reading"
            elif mode == "reading":
                if L.startswith("name"):
                    self.name = L.split("=")[1].strip()
                elif L.startswith("flags"):
                    _1, _2, rest = L.partition("=")
                    self.flags = set(rest.split())
                elif L.startswith("["):
                    mode = L.strip("[]\n")
                    self.width = 0
                    self.height = 0
            elif mode == "key":
                k,v = L.split("=")
                style = v.strip().split(":")
                self.key[k.strip()] = style
            elif mode == "layer":
                row = L.split()
                self.add_cells(row)
            elif mode == "gates":
                k,v = L.split("=")
                gate = v.strip().split(",")
                self.gates[k.strip()] = tuple(int(x) for x in gate)
            elif mode == "walk":
                row = L.split()
                self.add_cells(row,walk=True)
            elif mode == "object":
                k,v = (s.strip() for s in L.split("="))
                prop[k] = v
    def add_cells(self,row,walk=False):
        """ Returns a tuple with the format (objfile,pos,angle) """
        self.width = max(self.width,len(row))
        x = 0
        if walk:
            for c in row:
                if c == "1":
                    self.walktiles.add((x*2,self.height*2))
                x += 1
        else:
            for c in row:
                o = self.key.get(c[:-1])
                if o:
                    d = (self.key[c[:-1]],(x,self.height),int(c[-1])*-90)
                    self.data.append(d)
                x += 1
        self.height += 1
    def add_prop(self,data):
        pos = tuple(float(x) for x in data.get("pos").split(","))
        o = data.get("model")
        m = data.get("material")
        
        p = PropPart(data.get("name"),_pos=pos[:3],_angle=pos[3],_obj_filename=o+".obj")
        if m:
            p._style["mat-filename"] = m+".mtl"
        p.text = data.get("text")
        d = data.get("door")
        if d:
            p.door = d
        p.prepare()
        self.append(p)
        
    def buildparts(self,**kw):
        for d in self.data:
            style = d[0]
            if len(style) == 1:
                model = d[0][0]
                mat = None
            else:
                model,mat = d[0]
                mat+=".mtl"
            p = d[1]
            p = (p[0]*2,p[1]*2,0)
            o = PropPart(_pos=p,_angle=d[2],_obj_filename=model+".obj",_mat_filename=mat)
            o.prepare()
            self.append(o)
