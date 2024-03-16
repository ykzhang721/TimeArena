import sys
sys.path.append("..")
from ..object import *
from ..actions import *


class household10:
    def __init__(self):
        self.name = 'Clean and freshen up the living space and air.'


    def add_actions(self):
        self.actions = [
            MetaAction('wash','wash OBJ',True),
            MetaAction('wipe','wipe OBJ',True),
            MetaAction('activate','activate OBJ',False)
        ]
        return self.actions


    def add_objects(self):
        self.objects = [
            MetaObject("air_purifier",{"activate":7}, {}),
            MetaObject("rag",{"wash":5}, {}),
            MetaObject("table",{"wipe":4}, {"wipe":{"rag":"wash"}}),
            MetaObject("coffee_table",{"wipe":3}, {"wipe":{"rag":"wash"}})
        ]
        return self.objects