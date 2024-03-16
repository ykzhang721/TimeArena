import sys
sys.path.append("..")
from ..object import *
from ..actions import *


class cooking9:
    def __init__(self):
        self.name = 'Prepare a dish of rice topped with Nori seaweed and cooked fish.'


    def add_actions(self):
        self.actions = [
            MetaAction('pick','pick OBJ',True),
            MetaAction('cook in','cook OBJ1 in OBJ2',False),
            MetaAction('add to','add OBJ1 to OBJ2',True),
            MetaAction('wash','wash OBJ',True)
        ]
        return self.actions


    def add_objects(self):
        self.objects = [
            MetaObject("rice",{"pick":1,"cook_in_1":5,"add_to_1":3}, {"cook_in_1":"pick","add_to_1":"cook_in_1"}),
            MetaObject("nori_seaweed",{"pick":2,"add_to_1":1}, {"add_to_1":"pick"}),
            MetaObject("fish",{"pick":1,"cook_in_1":6,"add_to_1":2}, {"cook_in_1":"pick","add_to_1":"cook_in_1"}),
            MetaObject("pot",{"cook_in_2":0}, {}),
            MetaObject("pot",{"cook_in_2":0}, {}),
            MetaObject("dish",{"wash":3,"add_to_2":0}, {"add_to_2":"wash"})
        ]
        return self.objects