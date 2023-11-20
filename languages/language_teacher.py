'''
    About: Chatbot for helping improve users speaking abilities
'''

import os
import time

from openai import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)

# API Key
from constants import OPENAPI_KEY

# AI Assistants
from constants import SPANISH_TEACHER

# Prompts
SPANISH_TEACHER_PROMPT = '''I want you to act as a spoken Spanish teacher and improver.
I will speak to you in Spanish and you will reply to me in Spanish to practice my spoken Spanish.
I want you to keep your reply neat, limiting the reply to 100 words.
I want you to strictly correct my grammar mistakes, typos, and factual errors.
I want you to ask me a question in your reply.
Now let's start practicing, you could ask me a question first.
Remember, I want you to strictly correct my grammar mistakes, typos, and factual errors.
'''


# LLM
llm = ChatOpenAI()

# Prompt
prompt = ChatPromptTemplate(
    messages=[
        SystemMessagePromptTemplate.from_template(SPANISH_TEACHER_PROMPT),
        # The `variable_name` here is what must align with memory
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{question}"),
    ]
)

# Notice that we `return_messages=True` to fit into the MessagesPlaceholder
# Notice that `"chat_history"` aligns with the MessagesPlaceholder name
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
conversation = LLMChain(llm=llm, prompt=prompt, verbose=True, memory=memory)

# Notice that we just pass in the `question` variables - `chat_history` gets populated by memory
conversation({"question": "hi"})

# Notice that we just pass in the `question` variables - `chat_history` gets populated by memory
conversation({"question": "Quiero practicar mi espanol."})

conversation({"question": "End!"})



class ChatAI:
    def __init__(self, assistant: str, transcript_path: str = ''):
        self.client = OpenAI(api_key=OPENAPI_KEY)
        self.assistant = assistant
        self.transcript = f'{transcript_path}/transcript.txt'
        self.thread = self.client.beta.threads.create()
        
    
    def update_transcript(self, role: str, text: str):
        new_transcript_text = f'{role}: {text}\n\n'
        
        with open(self.transcript, 'a+') as file:
            file.write(new_transcript_text)
            
    
    def start_chat(self):
        # Generate Initial Text
        message = self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content="Start Conversation"
        )
        
        run = self.client.beta.threads.runs.create(
            thread_id=self.thread.id,
            assistant_id=self.assistant
        )
        
        time.sleep(3)
        
        run = self.client.beta.threads.runs.retrieve(
            thread_id=self.thread.id,
            run_id=run.id
        )
        
        messages = self.client.beta.threads.messages.list(
            thread_id=self.thread.id
        )
        
        message = messages.data[0].content[0].text.value
        print('Message', message)
    

def main():
    # spanish_teacher = ChatAI(SPANISH_TEACHER)
    # spanish_teacher.start_chat()
    pass
    


if __name__ == "__main__":
    main()