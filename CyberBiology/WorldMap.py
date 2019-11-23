import random
import time
import heapq

class WorldMap(object):
    _h_size = None
    _w_size = None
    _iterations = None
    # unit_lists - dictionary with keys format (h:w):UnitList
    # UnitList format [unit0,...,unitN], and unit0 is upper
    unit_lists = None
    # protocols - signals to WorldMap from WorldUnit in queue with priority, 'next node' is node with min priority
    __protocols = None
    # static_priority - static priority for queue nodes
    __static_priority = None
    __static_priority_range = [0, 10]
    # dynamic_priority - random priority for queue nodes
    __dynamic_priority = None
    __dynamic_priority_range = [1000, 1100]
    # back_color - background color
    _back_color = None
    # World has changed, redraw it
    _redraw = False

    def __init__(self, h, w, back_color):
        self._back_color = back_color
        self._h_size = h
        self._w_size = w
        self._iterations = 0
        self.unit_lists = dict()
        self.__protocols = []
        self.__update_priorities()

    def __update_priorities(self):
        self.__static_priority = [i for i in range(self.__static_priority_range[0], self.__static_priority_range[1])]
        self.__dynamic_priority = [i for i in range(self.__dynamic_priority_range[0], self.__dynamic_priority_range[1])]
        random.shuffle(self.__dynamic_priority)

    def iterate(self):
        self._iterations += 1
        usek_start = time.time_ns()
        #try:
        for coord,units in self.unit_lists.items():
            for unit in units:
                unit.life_process(self)
        del self.__static_priority
        del self.__dynamic_priority
        for i in range(len(self.__protocols)):
            protocol = heapq.heappop(self.__protocols)
            protocol[1].process(self)
        #except Exception as e:
        #    print("Iteration #{} failed: {}".format(self._iterations, e))
        #    return
        self.__update_priorities()
        print("Iteration #{} done, {} sec".format(self._iterations, (time.time_ns() - usek_start)/1000000000))

    def generate_color_map(self):
        color_map = []
        for coord,units in self.unit_lists.items():
            if len(units) == 0:
                continue
            unit = units[0]
            color_map.append([unit._h_pos, unit._w_pos, unit._color])
        return color_map

    def redraw_enable(self):
        self._redraw = True

    def redraw_success(self):
        self._redraw = False

    def append_protocol(self, proto, priority=None):
        if priority:
            self.__static_priority.remove(priority)
        else:
            priority = self.__dynamic_priority.pop()
        heapq.heappush(self.__protocols, [priority, proto])
