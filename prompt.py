class Instruction(object):
    class ConstError(TypeError):
        pass

    class ConstCaseError(ConstError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("%s already exists." % name)
        self.__dict__[name] = value

CON = Instruction()

CON.prompt4sp1 = '''
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


CON.prompt4sp2 = '''
Please output your plan based on the dependencies and duration of actions. 
You should complete all the tasks in a minimal time.
Pay attention to:
To maximize efficiency, adhere to the following principle: try to start the non-occupied action you anticipate will be the most time-consuming as early as possible. You should perform actions during idle times as much as possible to minimize the time spent doing nothing.
You must only output in a given format instead of JSON. Example outputs look like:\n"
"chop cheese: Start at t=1min, End at t=5min"
'''

CON.prompt4sp3 = "Based on the plan, you can start to complete the tasks. (Explicitly output the action without adding any other symbols (e.g., wash cup)"



CON.promptreact1 = '''
Please think about the interaction history between the agent and the environment, consider the states of the agent and objects and the task instructions with the goal of minimizing all task completion time. 
Try to identify the most efficient action (i.e., parallel performing) to take next.
If there are other actions that can be executed, try not to wait.
Finally output your thoughts for the next action.
'''

CON.promptreact2 = '''Please act based on the thinking. (Explicitly output the action without adding any other symbols (e.g., wash cup)'''



CON.promptreflexion1 = '''You are an advanced reasoning agent capable of improving through self-reflection. 
Review and reflect on the historical interactions between the agent and the environment.
Please diagnose a possible reason for the failure and devise a new, concise plan that aims to mitigate the failure. 
'''




CON.promptreflexion2 = '''Please regenerate actions based on reflection. (Explicitly output the action without adding any other symbols (e.g., wash cup).)'''