import sys
sys.path.append("..")
from ..object import *
from ..actions import *


class lab7:
    def __init__(self):
        self.name = 'Find all chemicals to synthesize ethyl acetate by heating, cooling and drying.'


    def add_actions(self):
        self.actions = [
            MetaAction('find','find OBJ',True),
            MetaAction('wash','wash OBJ',True),
            MetaAction('add to','add OBJ1 to OBJ2',True),
            MetaAction('heat','heat OBJ',False),
            MetaAction('cool','cool OBJ',False),
            MetaAction('dry','dry OBJ',False)
        ]
        return self.actions


    def add_objects(self):
        self.objects = [
            MetaObject("ethanol",{"find":1,"add_to_1":1}, {"add_to_1":"find"}),
            MetaObject("acetic_acid",{"find":1,"add_to_1":2}, {"add_to_1":"find"}),
            MetaObject("catalyst",{"find":1,"add_to_1":2}, {"add_to_1":"find"}),
            MetaObject("beaker",{"wash":1,"add_to_2":0,"heat":6,"cool":5,"dry":4}, {"add_to_2":"wash","heat":{"catalyst":"add_to_1","acetic_acid":"add_to_1","ethanol":"add_to_1"},"cool":"heat","dry":"cool"}),
        ]
        return self.objects