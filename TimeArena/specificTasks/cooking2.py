import sys
sys.path.append("..")
from ..object import *
from ..actions import *


class cooking2:
    def __init__(self):
        self.name = 'Prepare a noodle dish, which consists of cooked noodle, fried mushrooms and shrimp.'


    def add_actions(self):
        self.actions = [
            MetaAction('pick','pick OBJ',True),
            MetaAction('cook in','cook OBJ1 in OBJ2',False),
            MetaAction('chop','chop OBJ',True),
            MetaAction('fry in','fry OBJ1 in OBJ2',False),
            MetaAction('add to','add OBJ1 to OBJ2',True),
            MetaAction('wash','wash OBJ',True)
        ]
        return self.actions


    def add_objects(self):
        self.objects = [
            MetaObject("noodle",{"pick":1,"cook_in_1":5,"add_to_1":2}, {"cook_in_1":"pick","add_to_1":"cook_in_1"}),
            MetaObject("mushroom",{"pick":2,"chop":3,"fry_in_1":2,"add_to_1":2}, {"fry_in_1":"chop","chop":"pick","add_to_1":"fry_in_1"}),
            MetaObject("shrimp",{"pick":1,"chop":2,"fry_in_1":4,"add_to_1":2}, {"fry_in_1":"chop","chop":"pick","add_to_1":"fry_in_1"}),
            MetaObject("fryer",{"fry_in_2":0}, {}),
            MetaObject("fryer",{"fry_in_2":0}, {}),
            MetaObject("pot",{"cook_in_2":0}, {}),
            MetaObject("dish",{"wash":3,"add_to_2":0}, {"add_to_2":"wash"})
        ]
        return self.objects