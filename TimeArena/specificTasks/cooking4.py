import sys
sys.path.append("..")
from ..object import *
from ..actions import *


class cooking4:
    def __init__(self):
        self.name = 'Prepare and bake a cheese and tomato pizza.'


    def add_actions(self):
        self.actions = [
            MetaAction('pick','pick OBJ',True),
            MetaAction('chop','chop OBJ',True),
            MetaAction('wash','wash OBJ',True),
            MetaAction('add to','add OBJ1 to OBJ2',True),
            MetaAction('bake in','bake OBJ1 in OBJ2',False)
        ]
        return self.actions


    def add_objects(self):
        self.objects = [
            MetaObject("dish",{"wash":1,"add_to_2":0,"bake_in_1":10}, {"add_to_2":"wash","bake_in_1":{"dough":"add_to_1","cheese":"add_to_1","tomato":"add_to_1"}}),
            MetaObject("dough",{"pick":1,"chop":3,"add_to_1":2}, {"chop":"pick","add_to_1":"chop"}),
            MetaObject("cheese",{"pick":2,"chop":1,"add_to_1":4}, {"chop":"pick","add_to_1":"chop"}),
            MetaObject("tomato",{"pick":3,"chop":2,"add_to_1":1}, {"chop":"pick","add_to_1":"chop"}),
            MetaObject("oven",{"bake_in_2":0}, {}),
        ]
        return self.objects