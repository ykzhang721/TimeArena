import sys
sys.path.append("..")
from ..specificTasks import *
import re
import pdb

class score:
    def __init__(self, objects, totaltime):
        self.objects = objects
        self.total_time = totaltime
        self.initial = self.total_initial()


    def get_score(self):
        current_score = 0
        for obj in self.objects:
            for k, v in obj.properties['todo'].items():
                if v == 0:
                    current_score += self.initial[obj][k]
        return int(current_score * 100 / self.total_time)


    def total_initial(self):
        initial = {}
        for obj in self.objects:
            attr = {}
            for k, v in obj.properties['todo'].items():
                attr[k] = v
            initial[obj] = attr
        return initial