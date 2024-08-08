import json
import argparse
import random
import os
from TimeArena import *
import openai
import re
import prompt
from Agent import *
import pdb



def comma_separated_strings(string):
    return string.split(',')



def exit_action(action):
    return action.lower().strip() in ["quit", "exit"]



def Run(args):
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


    
    if args.prompting == "selfplan":
        Agent = SelfPlan_Agent()
        message, historyRecording = Agent.initialize(message, calling, historyRecording, current_time)
    elif args.prompting == 'react':
        Agent = ReAct_Agent()
    elif args.prompting == 'reflexion':
        Agent = Reflexion_Agent()
    else:
        Agent = Raw_Agent()


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
            message, action, historyRecording = Agent.act(message, calling, current_time, historyRecording)
            message = calling.add_assistant_message(message, action)
            print(action)
        
        if exit_action(action):
            print("Exit successfully!")
            break


        observation, increment, isCompleted, agent_occupy, wrong_message, historyRecording, message = Agent.step(action, calling, env, historyRecording, message, current_time, score)

        if wrong_message:
            invalid_num += 1
            print(observation)
            message = calling.add_user_message(message, observation)
            total_time -= 1
            current_time += 1
            if increment:
                score += increment
            continue
        if observation == None:
            total_time -= 1
            current_time += 1
            if increment:
                score += increment
        if observation != None:
            invalid_num = 0
            score += increment
            print({"time": current_time,"observation":observation, "increment": increment, "progress score": score, "isCompleted": isCompleted})
            message = calling.add_user_message(message, observation)
            total_time -= 1
            current_time += 1
            if isCompleted:
                print(f"Task Completed.")
                break                               
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
    parser.add_argument("--prompting", type=str, default=None, choices=['react','reflexion','selfplan'], help='The prompting method')
    parser.add_argument("--save_path", type=str, default=None, help='File path of the trajectory to be saved')
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
    Run(args)