import json
import argparse
import random
import os
from TimeArena import *
import openai
import re
import pdb



prompt4sp1 = '''
Given  the list of valid actions, available objects, and the task descriptions (goal), please perform the following steps:
- Identify and list all of the necessary actions required to accomplish the task's goal.
- For each action, determine and note the specific objects that are required and estimate a duration time (within ten minutes).
- Assess and map out any dependencies between actions, indicating which actions must precede others.
- If any action has multiple dependencies, list them in order of priority based on the task's constraints and goal.

Pay attention to:
- Some actions are non-occupied actions(Type 2), meaning you can perform other actions simultaneously. 
- You should add "*" after the action you think is non-occupied (e.g., "heat beaker*")
- Output a dictionary containing the duration of each action, and another dictionary containing the dependencies between actions.
- You must only output in a given format. Example outputs look like:\n"
"Duration: {"wash dish": 3, "pick rice": 2, "cook rice in pot*": 4}\n"
"Dependecncy: {"cook rice in pot*": ["pick rice"]}\n"'''


prompt4sp2 = '''
Please output your plan based on the dependencies and duration of actions. 
You should complete all the tasks in a minimal time.
Pay attention to:
To maximize efficiency, adhere to the following principle: try to start the non-occupied action you anticipate will be the most time-consuming as early as possible. You should perform actions during idle times as much as possible to minimize the time spent doing nothing.
You must only output in a given format instead of JSON. Example outputs look like:\n"
"chop cheese: Start at t=1min, End at t=5min"
'''

prompt4sp3 = "Based on the plan, you can start to complete the tasks."

def comma_separated_strings(string):
    return string.split(',')


def is_valid(action, env):
    action = action.strip().lower()
    split_action = action.split(" ")
    if action == 'wait':
        return True, True
    if len(split_action) in [1, 3] or len(split_action) > 4:
        return False, True
    if len(split_action) == 4:
        action_parsed = f"{split_action[0]} {split_action[2]}"
    else:
        action_parsed = f"{split_action[0]}"
    if action_parsed not in env.getActionList():
        return False, True
    objects = env.getObjectList()
    if len(split_action) == 4:
        if split_action[1] not in objects or split_action[3] not in objects:
            return True, False
    elif len(split_action) == 2:
        if split_action[1] not in objects:
            return True, False
    return True, True

def exit_action(action):
    return action.lower().strip() in ["quit", "exit"]



def Agent(args):
    # pdb.set_trace()
    env = TimeArena()
    env.load(args)
    instruction = env.getInstruction()
    print(instruction)
    historyRecording = [instruction]

    total_time = args.total_time
    current_time = 0
    calling = FuncCall(lm=args.lm,model_name=args.model_name, ip=args.ip, port=args.port)

    system_message = calling.get_system()
    message = calling.add_user_message(system_message, instruction)
    agent_occupy = False
    score = 0
    isCompleted = False
    invalid_num = 0

    if args.sp:
        message = calling.add_user_message(message, prompt4sp1)
        historyRecording.append(prompt4sp1)
        plan1 = calling.get_response(message)
        historyRecording.append(plan1)
        message = calling.add_assistant_message(message, plan1)
        message = calling.add_user_message(message, prompt4sp2)
        historyRecording.append(prompt4sp2)
        plan2 = calling.get_response(message)
        historyRecording.append(plan2)
        message = calling.add_assistant_message(message, plan2)
        message = calling.add_user_message(message, prompt4sp3)
    while total_time:
        print("----------------------------------------------------------------")
        if invalid_num >= 5:
            observation = "Exceed the invalid action limit!"
            print(observation)
            packed = {
                    'time': current_time,
                    'observation': observation,
                    'increment': 0,
                    'progress score': score,
                    'isCompleted': isCompleted,
                    'action': action,
                    }
            historyRecording.append(packed)
            break
        if not agent_occupy:
            message = calling.add_user_message(message, f"\nIn t={current_time}, your action is:")
            # action = calling.get_response(message)
            action = input()
            action = action.strip()
            message = calling.add_assistant_message(message, action)
            print(action)
        
        if exit_action(action):
            print("Exit successfully!")
            break
        action_valid, object_valid = is_valid(action, env)
        action = action.lower().strip()
        if action_valid and object_valid:
            observation, increment, isCompleted, agent_occupy, wrong_message = env.step(action)
            if wrong_message:
                invalid_num += 1
                print(observation)
                message = calling.add_user_message(message, observation)
                total_time -= 1
                current_time += 1

                packed = {
                    'time': current_time,
                    'observation': observation,
                    'increment': increment,
                    'progress score': score,
                    'isCompleted': isCompleted,
                    'action': action,
                    }
                historyRecording.append(packed)
                continue
            if observation == None and increment != None:
                total_time -= 1
                current_time += 1
            if observation != None:
                invalid_num = 0
                score += increment
                print({"observation":observation, "increment": increment, "progress score": score, "isCompleted": isCompleted})
                message = calling.add_user_message(message, observation)
                total_time -= 1
                current_time += 1
                if isCompleted:
                    print(f"Task Completed.")
                    packed = {
                        'time': current_time,
                        'observation': observation,
                        'increment': increment,
                        'progress score': score,
                        'isCompleted': isCompleted,
                        'action': action,
                        }
                    historyRecording.append(packed)
                    break                               
        else:
            invalid_num += 1 
            observation = ""
            if not action_valid:
                invalid_action_message = env.getInvalidActionMessage()
                observation += invalid_action_message
                message = calling.add_user_message(message, invalid_action_message)
                total_time -= 1
                current_time += 1  
                print(invalid_action_message)
                increment = 0
            if not object_valid:
                invalid_object_message = env.getInvalidObjectMessage()
                observation += invalid_object_message
                message = calling.add_user_message(message, invalid_object_message)
                total_time -= 1
                current_time += 1  
                print(invalid_object_message)
                increment = 0
        packed = {
            'time': current_time,
            'observation': observation,
            'increment': increment,
            'progress score': score,
            'isCompleted': isCompleted,
            'action': action,
            }
        historyRecording.append(packed)
    print(f"Task is completed in {current_time} minutes." if isCompleted else f"Task is not completed in {current_time} minutes.")
    historyRecording.append({"total_time":current_time,"total_score":score,"isCompleted":isCompleted})
    if args.save_path:
        if not os.path.exists(args.save_path):
            os.makedirs(args.save_path)
        with open(f"{args.save_path}/{args.save_name}.json",'w') as f:
            json.dump(historyRecording, f, ensure_ascii=False, indent=4)


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=42,
                        help="Seed the random generator used for sampling random actions.")
    parser.add_argument("--taskName", type=comma_separated_strings, help='input tasks splited by comma')
    parser.add_argument("--sp", default=False,action='store_true',help='Self-plan prompting method')
    parser.add_argument("--save_path", type=str, default=None,help='File path of the trajectory to be saved')
    parser.add_argument("--save_name", type=str, default=None, help='File name of the trajectory to be saved')
    parser.add_argument("--total_time", type=int, default=12, help='Total time for interaction')
    parser.add_argument("--constraint", default=False, action='store_true', help='Whether to use resource constraints')
    parser.add_argument("--ip", type=str, default=None, help='IP address of the model deployed with vllm')
    parser.add_argument("--port", type=str, default=None, help='Port of the model deployed with vllm')
    parser.add_argument("--model_name", type=str, default=None, help='Model name deployed with vllm')
    parser.add_argument("--lm", type=str, choices=['gpt4','gpt3.5','openchat','mistral','vicuna','mixtral-moe','gemini'],help='Model to evaluate')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse()
    Agent(args)