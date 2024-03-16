import sys
sys.path.append("..")
from ..object import *
from ..actions import *


class household8:
    def __init__(self):
        self.name = 'Sweep and mop the floor, then store the mop and sweeper.'


    def add_actions(self):
        self.actions = [
            MetaAction('activate','activate OBJ',False),
            MetaAction('rinse','rinse OBJ',True),
            MetaAction('mop','mop OBJ',True),
            MetaAction('store','store OBJ',True)
        ]
        return self.actions


    def add_objects(self):
        self.objects = [
            MetaObject("faucet",{"activate":5}, {}),
            MetaObject("mop",{"rinse":3,"store":2}, {"rinse":{"faucet":"activate"},"store":{"floor":"mop"}}),
            MetaObject("sweeper",{"activate":4,"store":2}, {"store":"activate"}),
            MetaObject("floor",{"mop":3}, {"mop":{"mop":"rinse","sweeper":"activate"}})
        ]
        return self.objects