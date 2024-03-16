import sys
sys.path.append("..")
from ..object import *
from ..actions import *


class lab9:
    def __init__(self):
        self.name = 'Add chemicals to beaker and synthesize benzaldehyde by heating, cooling and drying.'


    def add_actions(self):
        self.actions = [
            MetaAction('find','find OBJ',True),
            MetaAction('add to','add OBJ1 to OBJ2',True),
            MetaAction('heat','heat OBJ',False),
            MetaAction('cool','cool',False),
            MetaAction('dry','dry OBJ',False),
            MetaAction('wash','wash OBJ',True),
        ]
        return self.actions

# 纠正！！！！！！！！
    def add_objects(self):
        self.objects = [
            MetaObject("benzyl_alcohol",{"find":2,"add_to_1":3}, {"add_to_1":"find"}),
            MetaObject("oxidizing_agent",{"find":1,"add_to_1":3}, {"add_to_1":"find"}),
            MetaObject("beaker",{"wash":1,"add_to_2":0,"heat":5,"cool":1,"dry":4}, {"add_to_2":"wash","heat":{"benzyl_alcohol":"add_to_1","oxidizing_agent":"add_to_1"},"cool":"heat","dry":"cool"})
        ]
        return self.objects