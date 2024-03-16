import matplotlib.pyplot as plt
import json
import glob
import pdb
import argparse


def Completion_Rate(list):
    n = 0
    for task in list:
        if task[-1] == 100:
            n += 1
    return round(n / len(list)*100,2)

def Average_Completion_Time(list):
    n = 0
    num = 0
    for task in list:
        if task[-1] == 100:
            n += task.index(100) + 1
            num += 1
    if num == 0:
        return 0
    return round(n / num, 2)

def Average_Progress_Score(list):
    n = 0
    for task in list:
        n += task[-1]
    return round(n / len(list), 2)

def Completion_Speed(list):
    n = 0
    time = 0
    for task in list:
        n += task[-1]
        time += task.index(task[-1]) + 1
    return round(n / time, 2)


def cal_metrics(path):
    models_result = []
    for file_path in glob.glob(f"{path}/*"):
        with open(file_path, 'r') as f:
            data = json.load(f)
        i = 0
        for index, item in enumerate(data):
            if type(item) == dict:
                i = index
                break
        scores = [entry["progress score"] for entry in data[i:-1]]
        models_result.append(scores)
    print(len(models_result))
    return Average_Progress_Score(models_result), Completion_Speed(models_result), Completion_Rate(models_result), Average_Completion_Time(models_result)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str, help='Trajectory folder path')
    args = parser.parse_args()
    AS, CS, CR, CT = cal_metrics(args.path)
    print(f"AS: {AS} ; CS: {CS} ; CR : {CR} ; CT: {CT}")