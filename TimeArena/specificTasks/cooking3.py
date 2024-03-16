import sys
sys.path.append("..")
from ..object import *
from ..actions import *


class cooking3:
    def __init__(self):
        self.name = 'Make tomato noodle stir-fry, which consists of cooked noodle and fried tomato.'


    def add_actions(self):
        self.actions = [
            MetaAction('pick','pick OBJ',True),
            MetaAction('cook in','cook OBJ1 in OBJ2',False),
            MetaAction('chop','chop OBJ',True),
            MetaAction('fry in','fry OBJ1 in OBJ2',False),
            MetaAction('wash','wash OBJ',True),
            MetaAction('add to','add OBJ1 to OBJ2',True)
        ]
        return self.actions


    def add_objects(self):
        self.objects = [
            MetaObject("noodle",{"pick":1,"cook_in_1":5,"add_to_1":3}, {"cook_in_1":"pick","add_to_1":"cook_in_1"}),
            MetaObject("tomato",{"pick":2,"chop":3,"fry_in_1":2,"add_to_1":3}, {"fry_in_1":"chop","chop":"pick","add_to_1":"fry_in_1"}),
            MetaObject("pot",{"cook_in_2":0}, {}),
            MetaObject("fryer",{"fry_in_2":0}, {}),
            MetaObject("dish",{"wash":2,"add_to_2":0}, {"add_to_2":"wash"})
        ]
        return self.objects