import sys
sys.path.append("..")
from ..object import *
from ..actions import *


class cooking7:
    def __init__(self):
        self.name = 'Make chicken fried rice, which consists of fried rice and chicken.'


    def add_actions(self):
        self.actions = [
            MetaAction('pick','pick OBJ',True),
            MetaAction('chop','chop OBJ',True),
            MetaAction('fry in','fry OBJ1 in OBJ2',False),
            MetaAction('cook in','cook OBJ1 in OBJ2',False),
            MetaAction('add to','add OBJ1 to OBJ2',True),
            MetaAction('wash','wash OBJ',True)
        ]
        return self.actions


    def add_objects(self):
        self.objects = [
            MetaObject("rice",{"pick":1,"cook_in_1":5,"fry_in_1":7,"add_to_1":1}, {"cook_in_1":"pick","fry_in_1":"cook_in_1","add_to_1":"fry_in_1"}),
            MetaObject("chicken",{"pick":1,"chop":3,"fry_in_1":4,"add_to_1":3}, {"fry_in_1":"chop","chop":"pick","add_to_1":"fry_in_1"}),
            MetaObject("fryer",{"fry_in_2":0}, {}),
            MetaObject("fryer",{"fry_in_2":0}, {}),
            MetaObject("pot",{"cook_in_2":0}, {}),
            MetaObject("dish",{"wash":3,"add_to_2":0}, {"add_to_2":"wash"})
        ]
        return self.objects