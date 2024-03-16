import sys
sys.path.append("..")
from ..object import *
from ..actions import *


class lab10:
    def __init__(self):
        self.name = 'Prepare crystallized copper sulfate.'


    def add_actions(self):
        self.actions = [
            MetaAction('find','find OBJ',True),
            MetaAction('heat','heat OBJ',False),
            MetaAction('crystallize','crystallize OBJ',False),
            MetaAction('filter','filter OBJ',True),
        ]
        return self.actions


    def add_objects(self):
        self.objects = [
            MetaObject("copper_sulfate_solution",{"find":3,"heat":4,"crystallize":4,"filter":3}, {"heat":"find","crystallize":"heat","filter":"crystallize"})
        ]
        return self.objects