import sys
sys.path.append("..")
from ..object import *
from ..actions import *


class household7:
    def __init__(self):
        self.name = 'Make a cup of coffee.'


    def add_actions(self):
        self.actions = [
            MetaAction('add to','add OBJ1 to OBJ2',True),
            MetaAction('activate','activate OBJ',False),
            MetaAction('wash','wash OBJ',True),
            MetaAction('pour into','pour OBJ1 into OBJ2',True),
        ]
        return self.actions


    def add_objects(self):
        self.objects = [
            MetaObject("coffee_beans",{"add_to_1":3}, {}),
            MetaObject("coffee_machine",{"add_to_2":0, "activate":6, "pour_into_1":3}, {"activate":{"coffee_beans":"add_to_1","water":"add_to_1"}}),
            MetaObject("water",{"add_to_1":2}, {}),
            MetaObject("cup",{"wash":3,"pour_into_2":0}, {"pour_into_2":"wash"})
        ]
        return self.objects