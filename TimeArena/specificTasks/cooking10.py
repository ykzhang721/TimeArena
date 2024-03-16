import sys
sys.path.append("..")
from ..object import *
from ..actions import *


class cooking10:
    def __init__(self):
        self.name = 'Prepare beef and tomato stir-fry, which consists of cooked beef and fried tomato.'


    def add_actions(self):
        self.actions = [
            MetaAction('pick','pick OBJ',True),
            MetaAction('chop','chop OBJ',True),
            MetaAction('cook in','cook OBJ1 in OBJ2',False),
            MetaAction('fry in','fry OBJ1 in OBJ2',False),
            MetaAction('add to','add OBJ1 to OBJ2',True),
            MetaAction('wash','wash OBJ',True)
        ]
        return self.actions


    def add_objects(self):
        self.objects = [
            MetaObject("beef",{"pick":1,"chop":4,"cook_in_1":6,"add_to_1":2}, {"chop":"pick","cook_in_1":"chop","add_to_1":"cook_in_1"}),
            MetaObject("tomato",{"pick":2,"chop":2,"fry_in_1":5,"add_to_1":2}, {"chop":"pick","fry_in_1":"chop","add_to_1":"fry_in_1"}),
            MetaObject("pot",{"cook_in_2":0}, {}),
            MetaObject("fryer",{"fry_in_2":0}, {}),
            MetaObject("dish",{"wash":1,"add_to_2":0}, {"add_to_2":"wash"})
        ]
        return self.objects