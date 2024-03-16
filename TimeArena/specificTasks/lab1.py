import sys
sys.path.append("..")
from ..object import *
from ..actions import *


class lab1:
    def __init__(self):
        self.name = 'Prepare heated solution in test tube.'


    def add_actions(self):
        self.actions = [
            MetaAction('wash','wash OBJ',True),
            MetaAction('heat','heat OBJ',False),
            MetaAction('add to','add OBJ1 to OBJ2',True)
        ]
        return self.actions


    def add_objects(self):
        self.objects = [
            MetaObject("test_tube",{"wash":4,"add_to_2":0,"heat":5}, {"add_to_2":"wash","heat":{"solution":"add_to_1"}}),
            MetaObject("solution",{"add_to_1":4}, {}),
        ]
        return self.objects
