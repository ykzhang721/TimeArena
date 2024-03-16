import sys
sys.path.append("..")
from ..object import *
from ..actions import *


class household5:
    def __init__(self):
        self.name = 'Prepare a garden bed for planting flowers through weeding and hoeing.'


    def add_actions(self):
        self.actions = [
            MetaAction('add to','add OBJ1 to OBJ2',True),
            MetaAction('weed_with','weed_with OBJ',False),
            MetaAction('hoe','hoe OBJ',True),
            MetaAction('plant','plant OBJ',True),
        ]
        return self.actions


    def add_objects(self):
        self.objects = [
            MetaObject("sprinkling_can",{"add_to_2":0,"weed_with":4}, {"weed_with":{"herbicide":"add_to_1"}}),
            MetaObject("herbicide",{"add_to_1":5}, {}),
            MetaObject("land",{"hoe":4}, {}),
            MetaObject("flower",{"plant":2}, {"plant":{"land":"hoe","sprinkling_can":"weed_with"}}),
        ]
        return self.objects