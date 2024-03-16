import sys
sys.path.append("..")
from ..object import *
from ..actions import *


class lab6:
    def __init__(self):
        self.name = 'Prepare a diluted nitric acid and zinc mixture.'


    def add_actions(self):
        self.actions = [
            MetaAction('find','find OBJ',True),
            MetaAction('pick','pick OBJ',True),
            MetaAction('dilute','dilute OBJ',True),
            MetaAction('crush','crush OBJ',True),
            MetaAction('heat','heat OBJ',False),
            MetaAction('add to','add OBJ1 to OBJ2',True),
            MetaAction('wash','wash OBJ',True)
        ]
        return self.actions


    def add_objects(self):
        self.objects = [
            MetaObject("beaker",{"wash":1,"add_to_2":0}, {"add_to_2":"wash"}),
            MetaObject("nitric_acid",{"find":1,"dilute":4,"add_to_1":2}, {"dilute":"find","add_to_1":"dilute"}),
            MetaObject("zinc_pellet",{"pick":1,"crush":2,"heat":5,"add_to_1":2}, {"crush":"pick","heat":"crush","add_to_1":"heat"})
        ]
        return self.objects