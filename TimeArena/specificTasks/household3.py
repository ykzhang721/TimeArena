import sys
sys.path.append("..")
from ..object import *
from ..actions import *


class household3:
    def __init__(self):
        self.name = 'Wash and hang laundry.'


    def add_actions(self):
        self.actions = [
            MetaAction('gather','gather OBJ',True),
            MetaAction('add to','add OBJ1 to OBJ2',True),
            MetaAction('place into','place OBJ1 into OBJ2',True),
            MetaAction('activate','activate OBJ',False),
            MetaAction('hanging','hanging OBJ',True),
        ]
        return self.actions


    def add_objects(self):
        self.objects = [
            MetaObject("clothes",{"gather":2,"place_into_1":2,"hanging":5}, {"place_into_1":"gather","hanging":{"washing_machine":"activate"}}),
            MetaObject("detergent",{"add_to_1":2}, {}),
            MetaObject("washing_machine",{"place_into_2":0,"add_to_2":0,"activate":4}, {"activate":{"detergent":"add_to_1","clothes":"place_into_1"}})
        ]
        return self.objects