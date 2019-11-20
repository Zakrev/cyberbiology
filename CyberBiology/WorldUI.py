from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtCore import QBasicTimer, QRect
import sys

sys.path.insert(0, ".")
from WorldMap import WorldMap

class WorldUI(QWidget):
    __wmap_ui = None

    def __init__(self, wmap):
        super().__init__()
        self.__wmap_ui = WorldMapUI(self, wmap)
        self.setWindowTitle("WorldMapUI")
        self.__geometry()
        self.show()

    def __geometry(self):
        self.setGeometry(0, 0, 300, 300)
        self.__wmap_ui.setGeometry(0, 0, self.width(), self.height())

    def resizeEvent(self, e):
        self.__wmap_ui.resize(self.width(), self.height())
        pass

class WorldMapUI(QWidget):
    _wmap = None
    __timer = None
    __cell_h = 0
    __cell_w = 0
    __redraw = False

    def __init__(self, parent, wmap):
        super().__init__(parent)
        self._wmap = wmap
        self.__timer = QBasicTimer()
        self.__timer.start(250, self)

    def resizeEvent(self, e):
        height = self.height()
        width = self.width()
        height = int(height / self._wmap._h)
        width = int(width / self._wmap._w)
        if height != self.__cell_h or self.__cell_w != width:
            self.__redraw = True
        self.__cell_h = height
        self.__cell_w = width

    def paintEvent(self, e):
        if not self._wmap._redraw and not self.__redraw:
            return

        qp = QPainter()
        qp.begin(self)
        # draw background
        qp.setBrush(QColor(self._wmap._space_color))
        qp.drawRect(self.frameGeometry())
        # draw cells
        for h in range(0, self._wmap._h):
            for w in range(0, self._wmap._w):
                color = self._wmap.get_color(h, w)
                if not color:
                    continue
                qp.setBrush(QColor(color))
                qp.drawRect(QRect(w * self.__cell_w, h * self.__cell_h, self.__cell_w, self.__cell_h))
        qp.end()
        self.__redraw = False
        self._wmap.redraw_success()

    def timerEvent(self, e):
        self._wmap.iterate()
        self.repaint()