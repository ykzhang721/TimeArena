import sys
sys.path.append("..")
from ..object import *
from ..actions import *


class household1:
    def __init__(self):
        self.name = 'Make a cup of tea.'


    def add_actions(self):
        self.actions = [
            MetaAction('activate','activate OBJ',False),
            MetaAction('wash','wash OBJ',True),
            MetaAction('brew with','brew OBJ1 with OBJ2',False),
            MetaAction('pour into','pour OBJ1 into OBJ2',True),
        ]
        return self.actions


    def add_objects(self):
        self.objects = [
            MetaObject("tea",{"brew_with_1":3}, {}),
            MetaObject("kettle",{"activate":4, "pour_into_1":2}, {"pour_into_1":"activate"}),
            MetaObject("teapot",{"wash":1,"pour_into_1":3,"pour_into_2":0,"brew_with_2":0}, {"pour_into_2":"wash","brew_with_2":{"kettle":"pour_into_1"},"pour_into_1":{"tea":"brew_with_1"}}),
            MetaObject("cup",{"wash":3,"pour_into_2":0}, {"pour_into_2":"wash"})
        ]
        return self.objects