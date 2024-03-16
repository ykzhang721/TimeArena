import sys
sys.path.append("..")
from ..object import *
from ..actions import *


class lab5:
    def __init__(self):
        self.name = 'Perform an experiment with disolved sodium hydroxide and heated aluminum.'


    def add_actions(self):
        self.actions = [
            MetaAction('find','find OBJ',True),
            MetaAction('dissolve in','dissolve OBJ1 in OBJ2',False),
            MetaAction('wash','wash OBJ',True),
            MetaAction('pick','pick OBJ',True),
            MetaAction('cut','cut OBJ',True),
            MetaAction('heat','heat OBJ',False),
            MetaAction('add to','add OBJ1 to OBJ2',True)
        ]
        return self.actions


    def add_objects(self):
        self.objects = [
            MetaObject("sodium_hydroxide",{"find":1,"dissolve_in_1":6}, {"dissolve_in_1":"find"}),
            MetaObject("aluminum_foil",{"pick":2,"cut":2,"heat":5,"add_to_1":2}, {"cut":"pick","heat":"cut","add_to_1":"heat"}),
            MetaObject("beaker",{"wash":1,"dissolve_in_2":0,"add_to_2":0}, {"dissolve_in_2":"wash","add_to_2":"wash"})
        ]
        return self.objects