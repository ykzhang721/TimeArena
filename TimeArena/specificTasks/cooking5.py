import sys
sys.path.append("..")
from ..object import *
from ..actions import *


class cooking5:
    def __init__(self):
        self.name = 'Prepare chicken and potato stir-fry, which consists of fried chicken and fried potato.'


    def add_actions(self):
        self.actions = [
            MetaAction('pick','pick OBJ',True),
            MetaAction('chop','chop OBJ',True),
            MetaAction('fry in','fry OBJ1 in OBJ2',False),
            MetaAction('add to','add OBJ1 to OBJ2',True),
            MetaAction('wash','wash OBJ',True)
        ]
        return self.actions


    def add_objects(self):
        self.objects = [
            MetaObject("chicken",{"pick":1,"chop":5,"fry_in_1":5,"add_to_1":3}, {"chop":"pick","fry_in_1":"chop","add_to_1":"fry_in_1"}),
            MetaObject("potato",{"pick":1,"chop":3,"fry_in_1":6,"add_to_1":3}, {"fry_in_1":"chop","chop":"pick","add_to_1":"fry_in_1"}),
            MetaObject("fryer",{"fry_in_2":0}, {}),
            MetaObject("fryer",{"fry_in_2":0}, {}),
            MetaObject("dish",{"wash":1,"add_to_2":0}, {"add_to_2":"wash"})
        ]
        return self.objects



