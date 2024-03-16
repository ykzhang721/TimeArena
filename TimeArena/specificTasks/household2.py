import sys
sys.path.append("..")
from ..object import *
from ..actions import *


class household2:
    def __init__(self):
        self.name = 'Clean the dishes using the dishwasher and dispose trash.'


    def add_actions(self):
        self.actions = [
            MetaAction('gather','gather OBJ',True),
            MetaAction('scrape into','scrape OBJ1 into OBJ2',True),
            MetaAction('place into','place OBJ1 into OBJ2',True),
            MetaAction('activate','activate OBJ',False),
            MetaAction('empty','empty OBJ',True),
        ]
        return self.actions


    def add_objects(self):
        self.objects = [
            MetaObject("dishes",{"gather":3,"scrape_into_1":2,"place_into_1":4}, {"scrape_into_1":"gather","place_into_1":"scrape_into_1"}),
            MetaObject("dishwasher",{"place_into_2":0,"activate":4}, {"activate":{"dishes":"place_into_1"}}),
            MetaObject("trash",{"scrape_into_2":0,"empty":4}, {"empty":{"dishes": "scrape_into_1"}})
        ]
        return self.objects