import logging
from flask import Blueprint, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from multiprocessing import Process, Queue
import requests
from pydub import AudioSegment
from openai import OpenAI
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from langchain.memory import AgentTokenBufferMemory
from langchain.prompts import SystemMessage, MessagesPlaceholder
from langchain.chat_models import ChatOpenAI
from config import Config  # Assuming you have a config file

# Blueprint for main routes
main = Blueprint('main', __name__)

def receive_txt(sender_number, msg):
    # Get the singleton instance of the message queue
    msg_queue = MessageQueueSingleton()
    # Put the message and sender number in the message queue
    msg_queue.put((msg, sender_number))
    return

def receive_audio(sender_number, media):
    audio_queue = AudioQueueSingleton()
    audio_queue.put((media, sender_number))
    return

# Route to handle SMS messages received from Twilio
@main.route('/sms', methods=['POST'])
def sms_reply():
    # Extract sender number and message content from the request
    sender_number = request.form.get('From')
    msg = request.form.get('Body')
    media = request.form.get("MediaUrl0")
    media_type = request.form.get("MediaContentType0", "")

    if media and ("audio" in media_type or "mp3" in media_type):
        logging.info(f'MEDIA URL {media_type} - ' + media)
        receive_audio(sender_number, media)
    else:
        receive_txt(sender_number, msg)

    # Return a Twilio messaging response
    return str(MessagingResponse().message("Received"))

class MessageQueueSingleton:
    """
    MessageQueueSingleton class for managing message queues using Singleton design pattern
    """
    _instance = None

    def __init__(self):
        # Init Twilio Client
        account_sid = Config.TWILIO_ACCOUNT_ID
        auth_token = Config.TWILIO_AUTH_TOKEN
        self.client = Client(account_sid, auth_token)

        # Init LLM agent
        self.agent = Agent()

        # Create the message queue
        self.msg_queue = Queue()
        p = Process(target=self.responder, args=(self.msg_queue,))
        p.start()

    def __new__(cls, *args, **kwargs):
        """Singleton instance creation logic"""
        if not cls._instance:
            cls._instance = super(MessageQueueSingleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def put(self, object_):
        """Method to add objects to the queue"""
        self.msg_queue.put(object_)

    def responder(self, q: Queue):
        """Responder function to process messages"""
        while True:
            if not q.empty():
                message, sender = q.get()

                # Obtain response
                response = self.agent.run_query(message)

                # Send message back
                self.send_response(sender, response)

    def send_response(self, sender_number, message):
        """Method to send messages back to the sender"""
        # Split the message into blocks of 1500 characters
        for i in range(0, len(message), 1500):
            message_response = self.client.messages.create(
                from_=f'whatsapp:{Config.TWILIO_NUMBER}',
                to=f'''{sender_number.strip()}''',
                body=message[i: i + 1500]
            )

            print(message_response.sid)
            
class Agent:
    """Agent class for AI model interaction"""

    def __init__(self):
        """Setup for the language model and memory"""
        self.llm = ChatOpenAI(
            openai_api_base=Config.OPENAI_API_BASE,
            openai_api_key=Config.OPENAI_API_KEY
        )
        self.memory_key = "history"
        self.memory = AgentTokenBufferMemory(memory_key=self.memory_key, llm=self.llm)
        self.agent = self.create_agent()

    def create_agent(self):
        # Define the agents to be used
        agents_info = [
            # Add your agent information here
            # Example: {"name": "agent1", "description": "Description of agent1"},
            # Example: {"name": "agent2", "description": "Description of agent2"},
        ]
        tools = [
            Agent.create_tool_agent(source)
            for source in agents_info
        ]

        # Define the main agent
        prompt = OpenAIFunctionsAgent.create_prompt(
            system_message=SystemMessage(content=Config.PROMPT),
            extra_prompt_messages=[MessagesPlaceholder(variable_name=self.memory_key)]
        )
        agent = OpenAIFunctionsAgent(llm=self.llm, tools=tools, prompt=prompt)
        agent = AgentExecutor(agent=agent, tools=tools, memory=self.memory, verbose=True,
                              return_intermediate_steps=True)

        return agent

    def run_query(self, question):
        """Runs a query against the agent"""
        return self.agent.run(question)
    
class AudioQueueSingleton:
    """
    AudioQueueSingleton class for managing audio message queues using Singleton design pattern
    """
    _instance = None

    def __init__(self):
        # Written message queue
        self.msg_queue = MessageQueueSingleton()

        # Create the message queue
        self.audio_queue = Queue()
        p = Process(target=self.responder, args=(self.audio_queue,))
        p.start()

    def __new__(cls, *args, **kwargs):
        """Singleton instance creation logic"""
        if not cls._instance:
            cls._instance = super(AudioQueueSingleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def put(self, object_):
        """Method to add objects to the queue"""
        self.audio_queue.put(object_)

    def responder(self, q: Queue):
        """Responder function to process messages"""
        while True:
            if not q.empty():
                media_url, sender = q.get()
                mp3_file_path = self.ogg2mp3(audio_url=media_url)
                transcription = self.transcribe(mp3_file_path)

                self.msg_queue.put((transcription, sender))

    def ogg2mp3(self, audio_url):
        # Get the response of the OGG file
        response = requests.get(audio_url, auth=(Config.TWILIO_ACCOUNT_ID, Config.TWILIO_AUTH_TOKEN))

        with open("/tmp/audio.ogg", 'wb') as file:
            file.write(response.content)

        # Load the OGG file
        audio_file = AudioSegment.from_ogg("/tmp/audio.ogg")
        # Export the file as MP3
        audio_file.export("/tmp/audio.mp3", format="mp3")
        return "/tmp/audio.mp3"

    def transcribe(self, mp3_file_path):
        # Use OpenAI's Whisper to transcribe the audio
        result = (
            OpenAI().audio.transcriptions.create(
                file=open(mp3_file_path, "rb"),
                model="whisper-1",
                response_format='text'
            )
        )
        return result            