
import sys
sys.path.append("..")
from ..object import *
from ..actions import *


class cooking6:
    def __init__(self):
        self.name = 'Prepare a baked dish with dough, cheese, tomato, and fried beef.'


    def add_actions(self):
        self.actions = [
            MetaAction('pick','pick OBJ',True),
            MetaAction('chop','chop OBJ',True),
            MetaAction('fry in','fry OBJ1 in OBJ2',False),
            MetaAction('add to','add OBJ1 to OBJ2',True),
            MetaAction('wash','wash OBJ',True),
            MetaAction('bake in','bake OBJ1 in OBJ2',False)
        ]
        return self.actions


    def add_objects(self):
        self.objects = [
            MetaObject("dough",{"pick":1,"chop":2,"add_to_1":2}, {"chop":"pick","add_to_1":"chop"}),
            MetaObject("cheese",{"pick":2,"chop":1,"add_to_1":1}, {"chop":"pick","add_to_1":"chop"}),
            MetaObject("tomato",{"pick":1,"chop":2,"add_to_1":1}, {"chop":"pick","add_to_1":"chop"}),
            MetaObject("beef",{"pick":1,"chop":2,"fry_in_1":6,"add_to_1":2}, {"chop":"pick","fry_in_1":"chop","add_to_1":"fry_in_1"}),
            MetaObject("fryer",{"fry_in_2":0}, {}),
            MetaObject("dish",{"wash":2,"add_to_2":0,"bake_in_1":5}, {"add_to_2":"wash","bake_in_1":{"dough":"add_to_1","cheese":"add_to_1","tomato":"add_to_1"}}),
            MetaObject("oven",{"bake_in_2":0}, {})
        ]
        return self.objects