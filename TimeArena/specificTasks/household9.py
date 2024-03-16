import sys
sys.path.append("..")
from ..object import *
from ..actions import *


class household9:
    def __init__(self):
        self.name = 'Enjoy a cozy morning with the latest news and entertainment.'


    def add_actions(self):
        self.actions = [
            MetaAction('find','find OBJ',True),
            MetaAction('read','read OBJ',True),
            MetaAction('activate','activate OBJ',False),
            MetaAction('fold','fold OBJ',True)
        ]
        return self.actions


    def add_objects(self):
        self.objects = [
            MetaObject("newspaper",{"find":3,"read":5}, {"read":"find"}),
            MetaObject("radio",{"activate":7}, {}),
            MetaObject("quilt",{"fold":3}, {})
        ]
        return self.objects