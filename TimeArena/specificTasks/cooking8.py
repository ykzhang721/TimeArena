import sys
sys.path.append("..")
from ..object import *
from ..actions import *


class cooking8:
    def __init__(self):
        self.name = 'Prepare beef stir-fried noodle, which consists of cooked noodle and fried beef.'


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
            MetaObject("noodle",{"pick":1,"cook_in_1":6,"add_to_1":2}, {"cook_in_1":"pick","add_to_1":"cook_in_1"}),
            MetaObject("beef",{"pick":1,"chop":3,"fry_in_1":6,"add_to_1":2}, {"chop":"pick","fry_in_1":"chop","add_to_1":"fry_in_1"}),
            MetaObject("fryer",{"fry_in_2":0}, {}),
            MetaObject("pot",{"cook_in_2":0}, {}),
            MetaObject("dish",{"wash":3, "add_to_2":0}, {"add_to_2":"wash"})
        ]
        return self.objects