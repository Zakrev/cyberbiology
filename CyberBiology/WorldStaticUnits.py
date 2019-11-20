import sys

sys.path.insert(0, ".")
from WorldMap import WorldUnit

class UnitOrganic(WorldUnit):
    def __init__(self):
        self._is_organic = True

        super().__init__("#86bd46")

class UnitInorganic(WorldUnit):
    def __init__(self):
        self._is_not_overcome = True

        super().__init__("#583922")