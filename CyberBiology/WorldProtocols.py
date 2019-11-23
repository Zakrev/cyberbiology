from enum import Enum, Flag, auto

class Protocol(Enum):
    Other = auto()
    EatUnit = auto()

class WorldProtocol(object):
    _unit = None
    _type = None

    def __init__(self, unit):
        self._unit = unit
        self._type = Protocol.Other

    def process(self, world):
        pass

class Direction(Flag):
    UP = auto()
    DOWN = auto()
    RIGHT = auto()
    LEFT = auto()

class CreateUnit(WorldProtocol):
    __h = None
    __w = None

    def __init__(self, h, w, unit):
        super().__init__(unit)
        self.__h = h
        self.__w = w

    def process(self, world):
        h = self.__h % world._h_size
        w = self.__w % world._w_size
        units = world.unit_lists.get((h, w))
        if not units:
            units = []
            world.unit_lists[(h, w)] = units
        units.insert(0, self._unit)
        self._unit.update_position(h, w)
        world.redraw_enable()

class WalkUnit(WorldProtocol):
    __steps = None
    __direction = None
    _success = False

    def __init__(self, unit, direction, steps=1):
        super().__init__(unit)
        self.__direction = direction
        self.__steps = steps

    def process(self, world):
        if not self._unit._active:
            return
        h = self._unit._h_pos
        w = self._unit._w_pos
        for i in range(self.__steps):
            old_h = h
            old_w = w
            if self.__direction & Direction.UP:
                h = (h - 1) % world._h_size
            elif self.__direction & Direction.DOWN:
                h = (h + 1) % world._h_size
            if self.__direction & Direction.RIGHT:
                w = (w + 1) % world._w_size
            elif self.__direction & Direction.LEFT:
                w = (w - 1) % world._w_size
            units = world.unit_lists.get((h, w))
            if not units or len(units) == 0:
                continue
            if not units[0]._overstep:
                h = old_h
                w = old_w
                break
        if self._unit._h_pos == h and self._unit._w_pos == w:
            return
        units = world.unit_lists.get((self._unit._h_pos, self._unit._w_pos))
        units.remove(self._unit)
        units = world.unit_lists.get((h, w))
        if not units:
            units = []
            world.unit_lists[(h, w)] = units
        units.insert(0, self._unit)
        self._unit.update_position(h, w)
        world.redraw_enable()
        self._success = True

class EatUnit(WorldProtocol):
    _points = None
    result = None

    def __init__(self, unit, points=1):
        super().__init__(unit)
        self._points = points
        self._type = Protocol.EatUnit

    def process(self, world):
        if not self._unit._active:
            return
        h = self._unit._h_pos
        w = self._unit._w_pos
        units = world.unit_lists.get((h, w))
        if not units or len(units) == 0:
            return
        index = units.index(self._unit)
        index += 1
        if index >= len(units):
            return
        target = units[index]
        target.protocol_process(self)
        if not target._active:
            units.remove(target)

