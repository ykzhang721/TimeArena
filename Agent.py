from prompt import CON
import pdb



class Raw_Agent():
    def __init__(self):
        self.acting = "\nIn t={0}, your action is:"
        self.name = 'raw'

    def act(self, message, calling, current_time, historyRecording):
        message = calling.add_user_message(message, self.acting.format(current_time))
        action = calling.get_response(message).strip()
        return message, action, historyRecording
    
    def step(self, action, calling, env, historyRecording, message, current_time, score):
        observation, increment, isCompleted, agent_occupy, wrong_message = env.step(action)
        if observation != None:
            packed = {
                    'time': current_time,
                    'observation': observation,
                    'increment': increment,
                    'progress score': score,
                    'isCompleted': isCompleted,
                    'action': action,
                    }
            historyRecording.append(packed)
        return observation, increment, isCompleted, agent_occupy, wrong_message, historyRecording, message



class ReAct_Agent(Raw_Agent):
    def __init__(self):
        super().__init__()
        self.promptreact1 = CON.promptreact1
        self.promptreact2 = CON.promptreact2
        self.name = 'react'
        self.acting = "\nIn t={0}, your action is:"

    def act(self, message, calling, current_time, historyRecording):
        message = calling.add_user_message(message, self.promptreact1)
        thinking = calling.get_response(message)
        historyRecording.append({'time': current_time,
                                "thinking":thinking})
        message = calling.add_assistant_message(message, thinking)
        message = calling.add_user_message(message, self.promptreact2)
        message = calling.add_user_message(message, self.acting.format(current_time))
        action = calling.get_response(message).strip()
        return message, action, historyRecording



class Reflexion_Agent(Raw_Agent):
    def __init__(self):
        super().__init__()
        self.promptreflexion1 = CON.promptreflexion1
        self.promptreflexion2 = CON.promptreflexion2
        self.name = 'reflexion'
        self.acting = "\nIn t={0}, your action is:"

    def step(self, action, calling, env, historyRecording, message, current_time, score):
        observation, increment1, isCompleted, agent_occupy, wrong_message = env.step(action)
        if observation != None:
            packed = {
                'time': current_time,
                'observation': observation,
                'increment': increment1,
                'progress score': score,
                'isCompleted': isCompleted,
                'action': action,
                'zyk':11
                }
            historyRecording.append(packed)
        if wrong_message:
            observation, increment2, isCompleted, agent_occupy, wrong_message, historyRecording, message = self.reflexion(message, calling, current_time, historyRecording, env, observation, score)
            increment = increment1 or increment2
            if increment1 is not None and increment2 is not None:
                increment = increment1 + increment2
            return observation, increment, isCompleted, agent_occupy, wrong_message, historyRecording, message
        return observation, increment1, isCompleted, agent_occupy, wrong_message, historyRecording, message
            
    def reflexion(self, message, calling, current_time, historyRecording, env, observation, score):
        message = calling.add_assistant_message(message,observation)
        message = calling.add_user_message(message, self.promptreflexion1)
        reflexion = calling.get_response(message)
        
        historyRecording.append({
                        'time': current_time,
                        'observation': observation,
                        "reflexion":reflexion})
        message = calling.add_assistant_message(message, reflexion)
        message = calling.add_user_message(message, self.promptreflexion2)
        
        message, action, historyRecording = self.act(message, calling, current_time, historyRecording)
        
        observation, increment, isCompleted, agent_occupy, wrong_message = env.step(action)
        packed = {
            'time': current_time,
            'observation': observation,
            'increment': increment,
            'progress score': score,
            'isCompleted': isCompleted,
            'action': action,
            }
        historyRecording.append(packed)
        return observation, increment, isCompleted, agent_occupy, wrong_message, historyRecording, message


class SelfPlan_Agent(Raw_Agent):
    def __init__(self):
        super().__init__()
        self.prompt4sp1 = CON.prompt4sp1
        self.prompt4sp2 = CON.prompt4sp2
        self.prompt4sp3 = CON.prompt4sp3
        self.name = 'selfplan'

    def initialize(self, message, calling, historyRecording, current_time):
        message = calling.add_user_message(message, self.prompt4sp1)
        plan1 = calling.get_response(message)
        historyRecording.append(plan1)
        message = calling.add_assistant_message(message, plan1)
        message = calling.add_user_message(message, self.prompt4sp2)
        plan2 = calling.get_response(message)
        historyRecording.append(plan2)
        packed = {
            'time': current_time,
            "plan1": plan1,
            'plan2': plan2
            }
        historyRecording.append(packed)
        message = calling.add_assistant_message(message, plan2)
        message = calling.add_user_message(message, self.prompt4sp3)
        return message, historyRecording
    