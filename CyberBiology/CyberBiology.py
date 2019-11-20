import time
import sys
import random
from PyQt5.QtWidgets import QApplication

sys.path.insert(0, ".")
from WorldMap import WorldMap, WorldUnit, WorldCmd, WorldCmdRes
from WorldUI import WorldUI
from WorldStaticUnits import UnitOrganic, UnitInorganic

class UnitProto(UnitOrganic):
    __commands = None

    def __init__(self, color):
        super().__init__()
        self._color = color
        self.__commands = []

    def _iterate_start(self):
        if len(self.__commands) == 0:
            rnd = random.randint(1,8)
            if rnd == 1:
                self.__commands.append(WorldCmd.STEP_TO | WorldCmd.RIGHT)
            elif rnd == 2:
                self.__commands.append(WorldCmd.STEP_TO | WorldCmd.RIGHT | WorldCmd.DOWN)
            elif rnd == 3:
                self.__commands.append(WorldCmd.STEP_TO | WorldCmd.DOWN)
            elif rnd == 4:
                self.__commands.append(WorldCmd.STEP_TO | WorldCmd.LEFT | WorldCmd.DOWN)
            elif rnd == 5:
                self.__commands.append(WorldCmd.STEP_TO | WorldCmd.LEFT)
            elif rnd == 6:
                self.__commands.append(WorldCmd.STEP_TO | WorldCmd.LEFT | WorldCmd.UP)
            elif rnd == 7:
                self.__commands.append(WorldCmd.STEP_TO | WorldCmd.UP)
            elif rnd == 8:
                self.__commands.append(WorldCmd.STEP_TO | WorldCmd.RIGHT | WorldCmd.UP)
            self.__commands.append(WorldCmd.EAT_TO)
        return self.__commands.pop(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    wmap = WorldMap(6, 6)
    wmap.insert_unit(UnitProto("#d30000"), 0, 0)
    wmap.insert_unit(UnitProto("#086788"), 4, 4)

    wmap.insert_unit(UnitOrganic(), 1, 1)
    wmap.insert_unit(UnitOrganic(), 1, 3)
    wmap.insert_unit(UnitOrganic(), 3, 1)
    wmap.insert_unit(UnitOrganic(), 3, 3)

    for i in range(0, 6):
        wmap.insert_unit(UnitInorganic(), 5, i)
        wmap.insert_unit(UnitInorganic(), i, 5)

    wui = WorldUI(wmap)
    app.exec_()
