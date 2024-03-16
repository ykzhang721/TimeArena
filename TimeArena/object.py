
class MetaObject():
    def __init__(self, name, required_actions, dependency):
        self.properties = {}
        self.properties['name'] = name
        self.properties['occupy'] = False
        self.properties['todo'] = required_actions
        self.properties['dependency'] = dependency