import time
import sys
import random
from PyQt5.QtWidgets import QApplication

sys.path.insert(0, ".")
from WorldMap import WorldMap
from WorldUI import WorldUI
from WorldUnits import UnitOrganic
from WorldProtocols import CreateUnit

if __name__ == "__main__":
    app = QApplication(sys.argv)

    wmap = WorldMap(5, 5, "#000")
    wmap.append_protocol(CreateUnit(2, 2, UnitOrganic()))

    wui = WorldUI(wmap)
    app.exec_()
