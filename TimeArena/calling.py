from openai import OpenAI
import os
import pdb
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)
import re
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI



class FuncCall:
    def __init__(self, lm, model_name=None, ip=None, port=None):
        self.lm = lm
        self.model_name = model_name
        self.ip = ip
        self.port = port

    def get_system(self):
        return [HumanMessage(content="You are a helpful assistant. ")]


    def add_user_message(self,input, message):
        if isinstance(input[-1],HumanMessage):
            input[-1].content += message
        else:
            input.append(HumanMessage(content=message))
        return input


    def add_assistant_message(self, input, message):
        if isinstance(input[-1],AIMessage):
            input[-1].content += message
        else:
            input.append(AIMessage(content=message))
        return input


    def get_info_message(self, info):
        string = ""
        for i in info:
            if isinstance(i, HumanMessage):
                string += f"Human: {i.content}\n"
            elif isinstance(i, AIMessage):
                string += f"Ai: {i.content}\n"
        return string

    @retry(wait=wait_random_exponential(min=1, max=10), stop=stop_after_attempt(10))
    def get_response(self, info):
        global client
        if self.lm == "gpt4":
            LLM = ChatOpenAI(model='gpt-4-1106-preview', temperature=0, api_key=OPENAI_API_KEY)
            response = LLM.invoke(info)
            return response.content.replace("*","")
        elif self.lm == 'gpt3.5':
            LLM = ChatOpenAI(model='gpt-3.5-turbo-1106', temperature=0, api_key=OPENAI_API_KEY)
            response = LLM.invoke(info)
            return response.content.replace("*","")
        elif self.lm == 'openchat':
            LLM = ChatOpenAI(model=self.model_name, temperature=0, api_key="EMPTY",base_url=f"{self.ip}:{self.port}/v1",model_kwargs={"stop":['<|end_of_turn|>','\n']})
            response = LLM.invoke(info)
            return response.content.replace("*","")
        elif self.lm == 'mistral':
            LLM = ChatOpenAI(model=self.model_name, temperature=0, api_key="EMPTY",base_url=f"{self.ip}:{self.port}/v1",model_kwargs={"stop":['<|im_end|>','\n',":",'(']})
            response = LLM.invoke(info)
            return response.content.replace("\_","_").replace("*","")
        elif self.lm == 'mixtral-moe':
            llm = ChatOpenAI(model=self.model_name, temperature=0, api_key="EMPTY",base_url=f"{self.ip}:{self.port}/v1",model_kwargs={"stop":['<|im_end|>','\n','.','(','>',',']})
            response = llm.invoke(info)
            return response.content.replace("\\_","_").replace("*","")
        elif self.lm == 'gemini':
            llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0, model_kwargs={"stop":['\n']}, safety_settings=[
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_NONE",
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_NONE",
                },
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_NONE",
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_NONE",
                },
            ])
            info_message = self.get_info_message(info)
            response = llm.invoke(info_message)
            if "Ai:" in response.content:
                match = response.content.split("\n")[0].split("Ai:")[1].strip()
            else:
                match = response.content
            return match.replace("*","")
        elif self.lm == 'vicuna':
            LLM = ChatOpenAI(model=self.model_name, temperature=0, api_key="EMPTY",base_url=f"{self.ip}:{self.port}/v1",model_kwargs={"stop":['<|im_end|>','\n',':']})
            response = LLM.invoke(info)
            return response.content.replace("\_","_").replace("*","")