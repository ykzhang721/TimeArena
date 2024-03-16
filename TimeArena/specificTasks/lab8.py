import sys
sys.path.append("..")
from ..object import *
from ..actions import *


class lab8:
    def __init__(self):
        self.name = 'Perform a pH test on salt solution and label the salt.'


    def add_actions(self):
        self.actions = [
            MetaAction('pick','pick OBJ',True),
            MetaAction('wash','wash OBJ',True),
            MetaAction('dissolve in','dissolve OBJ1 in OBJ2',False),
            MetaAction('put in','put OBJ1 in OBJ2',True),
            MetaAction('label','label OBJ',True)
        ]
        return self.actions


    def add_objects(self):
        self.objects = [
            MetaObject("salt",{"pick":1,"dissolve_in_1":8,"label":1}, {"dissolve_in_1":"pick","label":{"ph_paper":"put_in_1"}}),
            MetaObject("test_tube",{"wash":3,"dissolve_in_2":0,"put_in_2":0}, {"dissolve_in_2":"wash","put_in_2":{"salt":"dissolve_in_1"}}),
            MetaObject("ph_paper",{"pick":1,"put_in_1":3}, {"put_in_1":"pick"})
        ]
        return self.objects