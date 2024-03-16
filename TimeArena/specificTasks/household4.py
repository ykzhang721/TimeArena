import sys
sys.path.append("..")
from ..object import *
from ..actions import *


class household4:
    def __init__(self):
        self.name = 'Maintenance of fruit trees.'


    def add_actions(self):
        self.actions = [
            MetaAction('add to','add OBJ1 to OBJ2',True),
            MetaAction('water by','water OBJ1 by OBJ2',False),
            MetaAction('trim','trim OBJ',True),
        ]
        return self.actions


    def add_objects(self):
        self.objects = [
            MetaObject("watering_can",{"add_to_2":0,"water_by_2":0}, {"water_by_2":{"water":"add_to_1"}}),
            MetaObject("water",{"add_to_1":3}, {}),
            MetaObject("fruit_tree",{"water_by_1":6,"trim":5}, {}),
        ]
        return self.objects

