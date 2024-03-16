from .object import *
from .specificTasks import *
from .goals import *
import json
import pdb


meta_prompt = '''As an AI agent, your objective is to efficiently complete a series of tasks as described. You must adhere to the specific requirements and constraints of each task, including dependencies and timing. Efficiency is key; complete all tasks in the shortest possible time. I will provide instructions regarding actions and objects.
**Action Protocol**:
 - You can perform only one action at a time.
 - After each observation from the environment, output an action based on that observation and the instructions.
 - Actions fall into two types:
    - Type 1: Action occupies you until completion (e.g., "wash OBJ").
    - Type 2: Action lets you be idle, allowing to perform other actions (e.g., "heat OBJ").
 - Follow the "Valid Actions" format for your output (e.g., "wash cup").
 - If no action is required, use "wait" to skip the current time.
 - Output the action explicitly (e.g., "wash cup").
 - Select object names (OBJ) from the list of Available Objects (e.g., use "rice" instead of "cooked rice" of "rice(Only for Task 1)").
'''


class TimeArena():
    def __init__(self):
        self.agent_occupy_state = False 
        self.agent_occupy_info = "" 
        
        self.last_score = 0 
        self.current_score = 0 
        self.isCompleted = False 
        self.last_action = ''
        self.non_occupy = {}
        self.non_occupy_conversation_info = {}
        self.object_in_task = {}
        self.task_num = {}
        self.obj_task_name = {}
        self.constraint_only_for_task_dict = {}


    def load(self, args):
        self.args = args
        tasks = self.args.taskName
        self.taskName = tasks
        self.Task = [globals()[name]() for name in self.taskName]
        self.objects, self.name2objects, self.objects_in_task = self.merge_objects(self.Task)
        self.actions, self.name2actions = self.merge_actions(self.Task) 
        self.taskdescription = [i.name for i in self.Task]
        self.total_time = self.getTotalActionTime()
        self.score = score(self.objects, self.total_time) 
        self.actions_state = MetaAction().properties['state']
        
    def step(self, action: str):
        action = action.strip()
        if action == 'wait':
            increment = None
            observation = "You wait for one minute.\n"
            self.update_non_occupy() 
            observation += self.add_non_occupy_complete_to_obervation() 
            self.current_score = self.score.get_score()
            if self.current_score == 100:
                self.isCompleted = True
            increment = self.current_score - self.last_score
            self.last_score = self.current_score
            self.last_action = action
            return observation, increment, self.isCompleted, False, False
        action_parsed, object_attribute = self.parse_action(action)
        self.agent_occupy = self.name2actions[action_parsed].properties['occupy']
        if self.action_object_valid(object_attribute,action):
            if self.subtask_denpendency(object_attribute):
                if not self.already_complete(object_attribute):
                    if self.name2actions[action_parsed].properties['occupy']: 
                        if action == self.last_action: 
                            observation = None 
                            increment = None
                            self.reduce_time(object_attribute)
                            required_time = self.get_time(object_attribute) 
                            self.update_non_occupy() 
                            if required_time == 0:
                                for k,v in object_attribute.items():
                                    if "_2" not in v:
                                        observation = f"{k} is {self.actions_state[v][1]}.\n"
                                self.current_score = self.score.get_score()
                                if self.current_score == 100:
                                    self.isCompleted = True
                                increment = self.current_score - self.last_score
                                self.agent_occupy = False
                                observation += self.add_non_occupy_complete_to_obervation() 
                        else:
                            required_time = self.get_time(object_attribute)
                            self.reduce_time(object_attribute)
                            observation = f"You are doing ``{action}``, it will take {required_time} minutes.\n"
                            increment = None
                            self.update_non_occupy()
                            observation += self.add_non_occupy_complete_to_obervation()
                            required_time = self.get_time(object_attribute)
                            if required_time == 0:
                                for k,v in object_attribute.items():
                                    if "_2" not in v:
                                        observation += f"{k} is {self.actions_state[v][1]}.\n"
                                self.current_score = self.score.get_score()
                                if self.current_score == 100:
                                    self.isCompleted = True
                                increment = self.current_score - self.last_score
                                
                                self.agent_occupy = False
                        self.current_score = self.score.get_score()
                        if self.current_score == 100:
                            self.isCompleted = True
                        increment = self.current_score - self.last_score
                        self.last_action = action
                        self.last_score = self.current_score
                        return observation, increment, self.isCompleted, self.agent_occupy, False
                    else:
                        self.add_non_occupy_info(action, object_attribute)
                        self.non_occupy = self.merge(self.non_occupy, object_attribute)
                        required_time = self.get_time(object_attribute)
                        observation = f"You are doing ``{action}``, it will take {required_time} minutes.\n"
                        self.update_non_occupy()
                        observation += self.add_non_occupy_complete_to_obervation()
                        self.current_score = self.score.get_score()
                        if self.current_score == 100:
                            self.isCompleted = True
                        increment = self.current_score - self.last_score
                        self.last_score = self.current_score
                        self.last_action = action
                        return observation, increment, self.isCompleted, self.agent_occupy, False
                else:
                    observation = f"``{action}`` has already been completed.\n"
                    increment = None
                    self.update_non_occupy()
                    observation += self.add_non_occupy_complete_to_obervation()
                    self.current_score = self.score.get_score()
                    if self.current_score == 100:
                        self.isCompleted = True
                    increment = self.current_score - self.last_score
                    return observation, increment, self.isCompleted, False, True
            else:
                for k, v in object_attribute.items():
                    if v in self.name2objects[k].properties['dependency'].keys():
                        if type(self.name2objects[k].properties['dependency'][v]) == str:
                            if not self.name2objects[k].properties['todo'][self.name2objects[k].properties['dependency'][v]] == 0:
                                observation = f"You cannot perform action ``{action_parsed}`` on object ``{self.name2objects[k].properties['name']}``.\n"
                                observation += "Because {0} is {1}.".format(k,self.actions_state[self.name2objects[k].properties['dependency'][v]][0])
                        elif type(self.name2objects[k].properties['dependency'][v]) == dict:
                            observation = f"You cannot perform action ``{action_parsed}`` on object ``{self.name2objects[k].properties['name']}``.\n"
                            for a,b in self.name2objects[k].properties['dependency'][v].items():
                                if not self.name2objects[a].properties['todo'][b] == 0:
                                    observation += "Because {0} is {1}.".format(a,self.actions_state[b][0])
                                    break
                self.update_non_occupy()
                observation += self.add_non_occupy_complete_to_obervation()
                self.current_score = self.score.get_score()
                if self.current_score == 100:
                    self.isCompleted = True
                increment = self.current_score - self.last_score
                return observation, increment, self.isCompleted, False, True
        else:
            for k, v in object_attribute.items():
                if self.name2objects[k].properties['occupy']:
                    observation = f"Object ``{k}`` is being occupied by another action.\n"
                    increment = None
                if v not in self.name2objects[k].properties['todo'].keys():
                    observation = f"You cannot perform action ``{action_parsed}`` on object ``{self.name2objects[k].properties['name']}``.\n"
                    increment = None
                elif len(action.split(" ")) == 4:
                    obj1,obj2 = action.split(" ")[1],action.split(" ")[3]
                    if obj2 in self.constraint_only_for_task_dict.keys():
                        if obj1 not in self.constraint_only_for_task_dict[obj2]:
                            observation = f"You cannot perform action ``{action_parsed}`` on object ``{obj1}`` and ``{obj2}``.\n"
                            increment = None
            self.update_non_occupy()
            observation += self.add_non_occupy_complete_to_obervation()
            self.current_score = self.score.get_score()
            if self.current_score == 100:
                self.isCompleted = True
            return observation, increment, self.isCompleted, False, True


    def subtask_denpendency(self, object_attribute):
        for k, v in object_attribute.items():
            if v in self.name2objects[k].properties['dependency'].keys():
                if type(self.name2objects[k].properties['dependency'][v]) == str: 
                        if not self.name2objects[k].properties['todo'][self.name2objects[k].properties['dependency'][v]] == 0:
                            return False
                elif type(self.name2objects[k].properties['dependency'][v]) == dict:
                    for a,b in self.name2objects[k].properties['dependency'][v].items():
                        if not self.name2objects[a].properties['todo'][b] == 0:
                            return False
        return True


    def merge_actions(self, tasks):
        unique_actions = {action for task in tasks for action in task.add_actions()}
        name_to_action_map = {action.properties['name']: action for action in unique_actions}
        
        return list(unique_actions), name_to_action_map


    def merge_lists_with_suffix(self, lists):
        output = []
        names_count = {} 
        object_in_task = {}
        for task in lists:
            for obj in task.add_objects():
                object_in_task.setdefault(task.name,[])
                object_in_task[task.name].append(obj)
                names_count.setdefault(obj.properties['name'],0)
                names_count[obj.properties['name']] += 1
        object_name_suffix = {}
        for key, value in object_in_task.items():
            for o in value:
                if names_count[o.properties['name']] > 1:
                    if o.properties['name'] not in object_name_suffix.keys():
                        object_name_suffix[o.properties['name']] = 1 
                    else:
                        object_name_suffix[o.properties['name']] += 1 
                    new_obj_name = f"{o.properties['name']}_{object_name_suffix[o.properties['name']]}"
                    if o.properties['name'] in ['pot','fryer','oven']:
                        o.properties['name'] = new_obj_name
                    else:
                        o.properties['name'] = new_obj_name
                        self.obj_task_name[new_obj_name] = key

        all_obj = {}
        for k,v in self.obj_task_name.items():
            for i in object_in_task[v]:
                for a,b in i.properties['dependency'].items():
                    if type(b) == dict:
                        replace = {}
                        for n, m in b.items():
                            if n in k:
                                replace[n] = k
                        for o, p in replace.items():
                            b[p] = b.pop(o)
        for k,v in object_in_task.items():
            all_obj[k] = []
            for i in v:
                output.append(i)
                all_obj[k].append(i.properties['name'])
        return object_in_task, output 


    def constraint_merge_lists_with_suffix(self,lists):
        constrain_objs = ["pot","fryer","oven"]
        output = []
        names_count = {}  
        object_in_task = {}
        already_add = [False, False, False]
        for task in lists:
            for obj in task.add_objects():
                if obj.properties['name'] in constrain_objs and already_add[constrain_objs.index(obj.properties['name'])]:
                    continue
                object_in_task.setdefault(task.name,[])
                object_in_task[task.name].append(obj)
                for index, i in enumerate(constrain_objs):
                    if obj.properties['name'] == i:
                        already_add[index] = True
                names_count.setdefault(obj.properties['name'],0)
                names_count[obj.properties['name']] += 1
        for i in constrain_objs:
            names_count[i] = 1
        object_name_suffix = {}
        for key, value in object_in_task.items():
            for o in value:
                if names_count[o.properties['name']] > 1:
                    if o.properties['name'] not in object_name_suffix.keys():
                        object_name_suffix[o.properties['name']] = 1  # 初始化编号
                    else:
                        object_name_suffix[o.properties['name']] += 1  # 递增编号
                    new_obj_name = f"{o.properties['name']}_{object_name_suffix[o.properties['name']]}"
                    o.properties['name'] = new_obj_name
                    self.obj_task_name[new_obj_name] = key
        all_obj = {}
        for k,v in self.obj_task_name.items():
            for i in object_in_task[v]:
                for a,b in i.properties['dependency'].items():
                    if type(b) == dict:
                        replace = {}
                        for n, m in b.items():
                            if n in k:
                                replace[n] = k
                        for o, p in replace.items():
                            b[p] = b.pop(o)
        for k,v in object_in_task.items():
            all_obj[k] = []
            for i in v:
                output.append(i)
                all_obj[k].append(i.properties['name'])
        return object_in_task, output


    def constraint_only_for_task(self, objects_in_task, name2objects):
        for object_name, task_name in self.obj_task_name.items():
            for action in name2objects[object_name].properties['todo']:
                if "_1" in action:
                    corresponding_action = action.replace("1", "2")
                    for obj in objects_in_task[task_name]:
                        if corresponding_action in obj.properties['todo']:
                            if "pot" not in obj.properties['name'] and "fryer" not in obj.properties['name'] and "oven" not in obj.properties['name']:
                                self.constraint_only_for_task_dict.setdefault(obj.properties['name'], []).append(object_name)


    def merge_objects(self, tasks):
        if self.args.constraint:
            objects_in_task, objects = self.constraint_merge_lists_with_suffix(tasks)
        else:
            objects_in_task, objects = self.merge_lists_with_suffix(tasks)
        name_to_objects = {}
        for object in objects:
            name_to_objects[object.properties['name']] = object
        self.constraint_only_for_task(objects_in_task, name_to_objects)
        return objects, name_to_objects, objects_in_task


    def parse_action(self, action):
        action_parts = action.split(" ")
        parsed_action_dict = {}
        if len(action_parts) > 2:
            parsed_action =  f"{action_parts[0]} {action_parts[2]}"
            parsed_action_dict[action_parts[1]] = f"{parsed_action.replace(' ', '_')}_1"
            parsed_action_dict[action_parts[3]] = f"{parsed_action.replace(' ', '_')}_2"
        else:
            parsed_action = f"{action_parts[0]}"
            parsed_action_dict[action_parts[1]] = f"{parsed_action}"
        return parsed_action, parsed_action_dict


    def action_object_valid(self, object_attribute, action):
        action_parts = action.split(" ")
        for object_name, action_required in object_attribute.items():
            associated_object = self.name2objects[object_name]
            if associated_object.properties['occupy']:
                return False
            if action_required not in associated_object.properties['todo']:
                return False
            if len(action_parts) == 4:
                subject, object_ = action_parts[1], action_parts[3]
                if object_ in self.constraint_only_for_task_dict:
                    if subject not in self.constraint_only_for_task_dict[object_]:
                        return False
        return True


    def already_complete(self, object_attribute):
        for k, v in object_attribute.items():
            if "_2" not in v and self.name2objects[k].properties['todo'][v] == 0:
                return True
        return False


    def get_time(self, object_attribute):
        key = next(iter(object_attribute))
        return self.name2objects[key].properties['todo'][object_attribute[key]]


    def reduce_time(self, object_attributes):
        for object_name, attribute_value in object_attributes.items():
            if "_2" not in attribute_value:
                self.name2objects[object_name].properties['todo'][attribute_value] -= 1


    def update_non_occupy(self):
        for object_name, indices in self.non_occupy.items():
            for index in indices:
                if self.name2objects[object_name].properties['todo'][index] > 0:
                    self.name2objects[object_name].properties['todo'][index] -= 1


    def add_non_occupy_info(self, action, object_attribute):
        for key, value in object_attribute.items():
            self.non_occupy_conversation_info.setdefault(key, {})
            self.non_occupy_conversation_info[key][value] = action
            # pdb.set_trace()

    def merge(self, dict_a, dict_b):
        for key, value in dict_b.items():
            dict_a.setdefault(key, [])
            if value not in dict_a[key]:
                dict_a[key].append(value)
        return dict_a


    def update_object_occupy(self):
        for obj in self.objects:
            if obj.properties['name'] in self.non_occupy_conversation_info.keys() :
                obj.properties['occupy'] = True
            else:
                obj.properties['occupy'] = False

    def add_non_occupy_complete_to_obervation(self):
        object_set = set()
        object_string = ""
        updated_occupy = {}
        updated_occupy_info = {}
        for object, property_list in self.non_occupy.items():
            for property in property_list:
                if self.name2objects[object].properties['todo'][property] > 0:
                    updated_occupy.setdefault(object, [])
                    updated_occupy[object].append(property)
                    updated_occupy_info.setdefault(object, {})
                    updated_occupy_info[object][property] = self.non_occupy_conversation_info[object][property]
                elif self.name2objects[object].properties['todo'][property] == 0 and "_2" not in property:
                    object_set.add(f"{object} is {self.actions_state[property][1]}.")
                elif self.name2objects[object].properties['todo'][property] == 0 and "_2" in property:
                    act = self.non_occupy_conversation_info[object][property]
                    # pdb.set_trace()
                    if act.split(" ")[1] in updated_occupy_info.keys():
                        updated_occupy.setdefault(object, [])
                        updated_occupy[object].append(property)
                        updated_occupy_info.setdefault(object, {})
                        updated_occupy_info[object][property] = self.non_occupy_conversation_info[object][property]
        for obj in object_set:
            object_string += f"{obj}\n"
        self.non_occupy = updated_occupy
        self.non_occupy_conversation_info = updated_occupy_info
        self.update_object_occupy()
        return object_string


    def getTaskDescription(self,Task):
        return Task.name


    def getInstruction(self):
        instruction_content = meta_prompt
        for idx, task in enumerate(self.Task):
            task_description = self.getTaskDescription(task)
            action_description = self.getActionDesc(task)
            task_information = f"**Task {idx + 1}**\n<Description>\n{task_description}\n<Valid Actions and Usages>\n{action_description}"
            instruction_content += task_information
            self.task_num[task.name] = f"Task {idx + 1}"
        available_objects = self.getObjects()
        object_information = f"**All Available Objects(OBJ)**\n{available_objects}"
        initial_states = self.getObjectsInitialState()
        states_information = f"**The Initial States of Objects**\n{initial_states}"
        instruction_content += object_information + states_information
        return instruction_content


    def getTotalActionTime(self):
        total = 0
        for obj in self.objects:
            for k, v in obj.properties['todo'].items():
                total += v
        return total


    def getActionList(self):
        return [action.properties['name'] for action in self.actions]


    def getActionDesc(self,task):
        str = ""
        for k in task.add_actions():
            str += f"- {k.properties['usage']}: {k.properties['description']}\n"
        str += f"wait: Pass without doing anything.\n"
        return str


    def getInvalidActionMessage(self):
        invalid_action_message = ""
        action_set = set()
        for action in self.actions:
            action_name = action.properties['name']
            if action_name not in action_set:
                usage_description = f"{action.properties['usage']}: {action.properties['description']}\n"
                invalid_action_message += usage_description
                action_set.add(action_name)
        invalid_action_message += "wait: pass the current time point without doing anything.\n"
        complete_message = "Invalid action! You can only choose action from valid actions.\nValid actions are: \n" + invalid_action_message
        return complete_message


    def getInvalidObjectMessage(self):
        available_object_names = "\n".join(obj.properties['name'] for obj in self.objects)
        message = (
            "Visit non-existent object! You can only choose an object from all available objects (OBJ).\n"
            "Available objects are: \n" + available_object_names
        )
        return message


    def getObjects(self):
        string = ""
        for obj in self.objects:
            if obj.properties['name'] in self.obj_task_name.keys():
                string += f"- {obj.properties['name']}(Only for {self.task_num[self.obj_task_name[obj.properties['name']]]})\n"
            else:
                string += f"- {obj.properties['name']}\n"
        return string
    
    def getObjectsInitialState(self):
        string = ""
        for obj in self.objects:
            state = self.actions_state[next(iter(obj.properties['todo']))][0]
            string += f"- {obj.properties['name']}: {state}\n"
        return string


    def getObjectList(self):
        return [obj.properties['name'].lower() for obj in self.objects]



if __name__ == "__main__":
    print(TimeArena("household1").step("activate kettle"))