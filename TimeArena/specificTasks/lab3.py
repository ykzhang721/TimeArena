import sys
sys.path.append("..")
from ..object import *
from ..actions import *


class lab3:
    def __init__(self):
        self.name = 'Prepare a ferrous sulfate solution using a magnetic stirrer.'


    def add_actions(self):
        self.actions = [
            MetaAction('pick','pick OBJ',True),
            MetaAction('dissolve in','dissolve OBJ1 in OBJ2',False),
            MetaAction('stir with','stir OBJ1 with OBJ2',True),
            MetaAction('wash','wash OBJ',True)
        ]
        return self.actions


    def add_objects(self):
        self.objects = [
            MetaObject("magnetic_stirrer",{"pick":4,"stir_with_2":0}, {"stir_with_2":"pick"}),
            MetaObject("ferrous_sulfate",{"pick":2,"dissolve_in_1":6}, {"dissolve_in_1":"pick"}),
            MetaObject("beaker",{"wash":1,"dissolve_in_2":0,"stir_with_1":3}, {"dissolve_in_2":"wash","stir_with_1":{"ferrous_sulfate":"dissolve_in_1"}})
        ]
        return self.objects