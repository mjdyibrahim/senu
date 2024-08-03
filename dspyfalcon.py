import dspy
from ai71 import AI71

# Load Falcon LLM API key from environment variables
import os
from dotenv import load_dotenv

load_dotenv()

FALCON_LLM_API_KEY = os.getenv("AI71_API_KEY")

# Initialize Falcon LLM client
client = AI71(FALCON_LLM_API_KEY)

# Create a DSPy compatible LM class (assuming you need to wrap Falcon)
class FalconLM(dspy.LMBase):
    def __init__(self, client, model="tiiuae/falcon-180B-chat", max_tokens=300):
        self.client = client
        self.model = model
        self.max_tokens = max_tokens

    def call(self, prompt, **kwargs):
        messages = [{"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}]
        response = self.client.chat.completions.create(
            messages=messages,
            model=self.model,
            stream=False,  # Assuming we want a non-streamed response here
            max_tokens=self.max_tokens,
            **kwargs
        )
        return response.choices[0].text.strip()

# Initialize the Falcon LLM within DSPy
falcon_lm = FalconLM(client)
dspy.configure(lm=falcon_lm)

# Define a DSPy module
qa = dspy.ChainOfThought('question -> answer')

# Example usage
response = qa(question="How strong is the team described in the uploaded pitch deck?")
print(response.answer)