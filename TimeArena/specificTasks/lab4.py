import sys
sys.path.append("..")
from ..object import *
from ..actions import *


class lab4:
    def __init__(self):
        self.name = 'Perform a chemical reaction between iron and copper sulfate to create a copper-coated iron nail.'


    def add_actions(self):
        self.actions = [
            MetaAction('find','find OBJ',True),
            MetaAction('pick','pick OBJ',True),
            MetaAction('dilute','dilute OBJ',True),
            MetaAction('polish','polish OBJ',True),
            MetaAction('soak in','soak OBJ1 in OBJ2',False)
        ]
        return self.actions


    def add_objects(self):
        self.objects = [
            MetaObject("copper_sulfate_solution",{"find":1,"dilute":3,"soak_in_2":0}, {"dilute":"find","soak_in_2":"dilute"}),
            MetaObject("iron_nail",{"pick":2,"polish":6,"soak_in_1":7}, {"polish":"pick","soak_in_1":"polish"})
        ]
        return self.objects

