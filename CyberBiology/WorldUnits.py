import sys

sys.path.insert(0, ".")
from WorldProtocols import Protocol

class WorldUnit(object):
    # color - str with format "#ffffff"
    _color = None
    # position in WorldMap
    _h_pos = None
    _w_pos = None
    # protocols - signals to WorldUnit from WorldMap in list, 'next node' is last node in list
    __protocols = None
    # world parameters
    _active = True
    _overstep = True

    def __init__(self, color):
        self._color = color
        self.__protocols = []

    def update_position(self, h, w):
        self._h_pos = h
        self._w_pos = w

    def life_process(self, world):
        pass

    def protocol_process(self, proto):
        pass

class UnitOrganic(WorldUnit):
    _life_point = None

    def __init__(self):
        super().__init__("#86bd46")
        self._life_point = 1

    def protocol_process(self, proto):
        if proto._type == Protocol.EatUnit:
            if self._life_point <= proto._points:
                proto.result = self._life_point
                self._life_point = 0
            else:
                proto.result = proto._points
                self._life_point -= proto._points
            if self._life_point <= 0:
                self._active = False

class UnitInorganic(WorldUnit):
    def __init__(self):
        self._overcome = False
        super().__init__("#583922")