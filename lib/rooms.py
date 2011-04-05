import pyglet

from tdgl import objpart, part

import data

class RoomPart(objpart.ObjPart):
    _default_style = {
        "obj-pieces":None,
        "obj-filename":None,
        }

class Room(part.Group):
    def __init__(self,name,fname,**kw):
        super(Room,self).__init__(name,(),**kw)
        self.width = 0
        self.height = 0
        self.key = {}
        self.gates = {}
        self.data = []
        self.walktiles = set()
        self.loadfile(fname)
        self.buildparts(**kw)

    def loadfile(self,fname):
        mode = "reading"
        roomdata = data.load(fname)
        lines = roomdata.readlines()
        for L in lines:
            if L.strip():
                if L.startswith("/"):
                    mode = "reading"
                elif mode == "reading":
                    if L.startswith("name"):
                        self.name = L.split("=")[1].strip()
                    elif L.startswith("["):
                        mode = L.strip("[]\n")
                        self.width = 0
                        self.height = 0
                elif mode == "key":
                    k,v = L.split("=")
                    self.key[k.strip()] = v.strip()
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
    def add_cells(self,row,walk=False):
        """ Returns a tuple with the format (objfile,pos,angle) """
        self.width = max(self.width,len(row))
        self.height += 1
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
    def buildparts(self,**kw):
        for d in self.data:
            p = d[1]
            p = (p[0]*2,p[1]*2,0)
            o = RoomPart(_pos=p,_angle=d[2],_obj_filename=d[0]+".obj")
            o.prepare()
            self.append(o)
