import argparse
import json
import pdb
from collections import deque
import itertools

def all_permutations(lst):
    return list(itertools.permutations(lst))


with open("dependencygraph.json","r") as f:
    dependencygraph = json.load(f)


def comma_separated_strings(string):
    return string.split(',')

def bfs(action, dependencies):
    visited = set()
    queue = deque([action])
    result = []
    while queue:
        current = queue.popleft()
        if current in visited:
            continue
        visited.add(current)
        if current in dependencies:
            for parent in dependencies[current]:
                if parent not in visited:
                    queue.append(parent)
        result.append(current)
    return result[::-1]

def check_dependencies(action, current_time, action_schedule, dependencies):
    if action not in dependencies:
        return True
    return all(action_schedule.get(dep, (100, 100))[1] < current_time for dep in dependencies[action])

def cal_oracle(task):
    actions = task[0]
    dependencies = task[1]
    pre_sorted_actions = sorted((k for k in actions.keys() if "*" in k), key=lambda x: actions[x], reverse=True)
    all_sorted_actions = all_permutations(pre_sorted_actions)

    final_min = 100
    final_schedule = {}

    for sorted_actions in all_sorted_actions:
        final_sequence = []
        processed_actions = set()
        for action in sorted_actions:
            req = []
            prerequisites = bfs(action, dependencies)
            for pre in prerequisites:
                if pre not in processed_actions:
                    req.append(pre)
                    processed_actions.add(pre)
            final_sequence.append(req)


        for action in actions.keys():
            req = []
            if action not in processed_actions:
                prerequisites = bfs(action, dependencies)
                for pre in prerequisites:
                    if pre not in processed_actions:
                        req.append(pre)
                final_sequence.append(req)
                processed_actions.add(pre)

        actionlist = final_sequence
        action_schedule = {}

        current_time = 0
        occupy_actions = {k: v for k, v in actions.items() if "*" not in k}
        non_occupy_actions = {k: v for k, v in actions.items() if "*" in k}

        while occupy_actions or non_occupy_actions:
            action_broken = False
            for l in actionlist:
                for act in l:
                    if check_dependencies(act, current_time, action_schedule, dependencies):
                        if act in non_occupy_actions:
                            duration = actions[act]
                            action_schedule[act] = (current_time, current_time  + (duration-1))
                            current_time += 1
                            non_occupy_actions.pop(act)
                            action_broken = True
                            break 
                        if act in occupy_actions:
                            start_time = current_time
                            current_time += occupy_actions[act]
                            action_schedule[act] = (start_time, current_time -1)
                            occupy_actions.pop(act)
                            action_broken = True
                            break
                if action_broken:
                    break
            if not action_broken:
                current_time += 1
        maxNum = 0
        for action, times in sorted(action_schedule.items(), key=lambda x: x[1]):
            maxNum = max(maxNum, times[1])
        if maxNum+1 < final_min:
            final_min = maxNum+1
            final_schedule = action_schedule
    return final_min


def process_data(data):
    new_data = {}
    num = len(data.keys())

    new_name = ",".join(list(data.keys()))
    for n, (task, content) in enumerate(data.items()):
        act_time = content[0]
        act_den = content[1]
        new1 = {}
        new2 = {}
        for k, v in act_time.items():
            new1[f"{k}<<{n}>>"] = v
        for k, v in act_den.items():
            new_v = [f"{i}<<{n}>>" for i in v]
            new2[f"{k}<<{n}>>"] = new_v
        new_data[task] = [new1,new2]
    value1 = {}
    value2 = {}
    final = {}
    for k, v in new_data.items():
        value1 = {**value1, **v[0]}
        value2 = {**value2, **v[1]}
    final[new_name] = [value1, value2]
    return final


def get_pracle_performance(tasks):
    data = {}
    for task in tasks:
        data[task] = dependencygraph[task]
    
    if len(tasks) == 1:
        task_name, task = list(data.items())[0]
        return task_name, cal_oracle(task)
    new_data = process_data(data)
    task_name, task = list(new_data.items())[0]
    return task_name, cal_oracle(task)




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--tasks", nargs='+', type=comma_separated_strings, help='input tasks splited by comma')
    args = parser.parse_args()
    avg_oracle = 0
    for task in args.tasks:
        task_name, oracle = get_pracle_performance(task)
        avg_oracle += oracle
        print(f"Task: {task_name} ; Oracle Completion Time: {oracle} ; Oracle Completion Speed: {round(100/oracle,2)}")
    print(f"Avg Oracle Completion Time: {round(avg_oracle/len(args.tasks),2)} ; Avg Oracle Completion Speed: {round(100/round(avg_oracle/len(args.tasks),2),2)}")