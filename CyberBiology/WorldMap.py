import random
import time
from enum import Flag, auto

class WorldCmd(Flag):
    STEP_TO = auto()
    EAT_TO = auto()
    RIGHT = auto()
    LEFT = auto()
    UP = auto()
    DOWN = auto()

class WorldCmdRes(Flag):
    FAILED = auto()
    SUCCESS = auto()

class WorldMap(object):
    _w = 0
    _h = 0
    # map structure is rows
    # map[0] == [0,w]
    # map[h] == [0,w]
    # when every row is list of WorldUnits, i.e.
    # map[h][w] == [unit0,unitN]
    __map = None
    __iterations = 0
    # background color
    _space_color = None
    # need redraw world map
    _redraw = False

    def __init__(self, width, height):
        self._h = height
        self._w = width
        self.__map = [[None for h in range(0, height)] for w in range(0, width)]
        self._space_color = "#000"

    def iterate(self):
        self.__iterations += 1
        cells = self._h * self._w
        cells = [i for i in range(0, cells)]
        random.shuffle(cells)

        usek_start = time.time_ns()
        try:
            for cell in cells:
                h = int(cell / self._w)
                w = int(cell - (h * self._w))
                units = self.__map[h][w]
                if not units:
                    continue
                for unit in units:
                    if unit._iterations == self.__iterations:
                        continue
                    self.__iterate_unit(h, w, unit)
        except Exception as e:
            print("Iteration #{} failed: {}".format(self.__iterations, e))
            return
        else:
            print("Iteration #{} done, {} sec".format(self.__iterations, (time.time_ns() - usek_start)/1000000000))

    def __iterate_unit(self, h, w, unit):
        result = None
        wcmd = unit.iterate_start()
        if not wcmd:
            return
        elif wcmd & WorldCmd.STEP_TO or wcmd & WorldCmd.EAT_TO:
            new_w = w
            new_h = h
            if wcmd & WorldCmd.LEFT:
                new_w = (w - 1) % self._w
                if wcmd & WorldCmd.UP:
                    new_h = (h - 1) % self._h
                elif wcmd & WorldCmd.DOWN:
                    new_h = (h + 1) % self._h
            elif wcmd & WorldCmd.RIGHT:
                new_w = (w + 1) % self._w
                if wcmd & WorldCmd.UP:
                    new_h = (h - 1) % self._h
                elif wcmd & WorldCmd.DOWN:
                    new_h = (h + 1) % self._h
            elif wcmd & WorldCmd.UP:
                new_h = (h - 1) % self._h
            elif wcmd & WorldCmd.DOWN:
                new_h = (h + 1) % self._h

            if wcmd & WorldCmd.STEP_TO:
                if 0 == self.insert_unit(unit, new_h, new_w):
                    self.__map[h][w].remove(unit)
                    result = WorldCmdRes.SUCCESS
                else:
                    result = WorldCmdRes.FAILED
            elif wcmd & WorldCmd.EAT_TO:
                if w == new_w and h == new_h:
                    target = self.__map[new_h][new_w].index(unit)
                    target += 1
                    if target >= len(self.__map[new_h][new_w]) or not self.__map[new_h][new_w][target]._is_organic:
                        result = WorldCmdRes.FAILED
                    else:
                        self.__map[new_h][new_w].pop(target) # FIXME: use WorldUnit:die()
                        result = WorldCmdRes.SUCCESS
                elif not self.__map[new_h][new_w] or not self.__map[new_h][new_w][0]._is_organic:
                    result = WorldCmdRes.FAILED
                else:
                    self.__map[new_h][new_w].pop(0) # FIXME: use WorldUnit:die()
                    result = WorldCmdRes.SUCCESS
        else:
            raise ValueError
        unit.iterate_end(result)

    def insert_unit(self, unit, h, w):
        assert h < self._h, "Invalid height coordinate"
        assert w < self._w, "Invalid width coordinate"
        if not self.__map[h][w]:
            self.__map[h][w] = []
        else:
            for unitn in self.__map[h][w]:
                if unitn._is_not_overcome:
                    return -1
        self.__map[h][w].insert(0, unit)
        self._redraw = True
        return 0

    def get_color(self, h, w):
        assert h < self._h, "Invalid height coordinate"
        assert w < self._w, "Invalid width coordinate"
        if not self.__map[h][w]:
            return None
        else:
            return self.__map[h][w][0]._color

    def redraw_success(self):
        self._redraw = True

class WorldUnit(object):
    _is_not_overcome = False
    _is_organic = False
    # color - str with format "#ffffff"
    _color = None
    _iterations = 0

    def __init__(self, hex_color):
        self._color = hex_color

    def _iterate_start(self):
        pass

    def _iterate_end(self, result):
        pass

    def iterate_start(self):
        self._iterations += 1
        return self._iterate_start()

    def iterate_end(self, result):
        return self._iterate_end(result)