import sys
sys.path.append("..")
from ..object import *
from ..actions import *


class lab2:
    def __init__(self):
        self.name = 'Prepare a mixture of sulfuric acid and sodium.'


    def add_actions(self):
        self.actions = [
            MetaAction('find','find OBJ',True),
            MetaAction('dilute','dilute OBJ',True),
            MetaAction('cut','cut OBJ',True),
            MetaAction('heat','heat OBJ',False),
            MetaAction('wash','wash OBJ',True),
            MetaAction('add to','add OBJ1 to OBJ2',True)
        ]
        return self.actions


    def add_objects(self):
        self.objects = [
            MetaObject("beaker",{"wash":3,"add_to_2":0}, {"add_to_2":"wash"}),
            MetaObject("sulfuric_acid",{"find":1,"dilute":3,"add_to_1":2}, {"dilute":"find","add_to_1":"dilute"}),
            MetaObject("sodium_flakes",{"find":1,"cut":2,"heat":5,"add_to_1":2}, {"cut":"find","heat":"cut","add_to_1":"heat"})
        ]
        return self.objects