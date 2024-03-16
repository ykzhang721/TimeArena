import sys
sys.path.append("..")
from ..object import *
from ..actions import *


class household6:
    def __init__(self):
        self.name = 'Iron a suit and store it.'


    def add_actions(self):
        self.actions = [
            MetaAction('set_up','set_up OBJ',True),
            MetaAction('put on','put OBJ1 on OBJ2',True),
            MetaAction('heat','heat OBJ',False),
            MetaAction('iron','iron OBJ',True),
            MetaAction('store','store OBJ',True)
        ]
        return self.actions


    def add_objects(self):
        self.objects = [
            MetaObject("ironing_board",{"set_up":2,"put_on_2":0}, {"put_on_2":"set_up"}),
            MetaObject("suit",{"put_on_1":4,"iron":3,"store":1}, {"iron":{"suit":"put_on_1","iron":"heat"},"store":"iron"}),
            MetaObject("iron",{"heat":7}, {})
        ]
        return self.objects