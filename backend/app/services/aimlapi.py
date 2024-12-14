import requests
import os
import dspy
from dotenv import load_dotenv
from dsp.modules.lm import LM

from openinference.instrumentation.dspy import DSPyInstrumentor
from opentelemetry import trace as trace_api
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk import trace as trace_sdk
from opentelemetry.sdk.trace.export import SimpleSpanProcessor

# Initialize DSPy auto-instrumentation
DSPyInstrumentor().instrument()

tracer_provider = trace_sdk.TracerProvider()
span_exporter = OTLPSpanExporter("http://localhost:6006/v1/traces")
span_processor = SimpleSpanProcessor(span_exporter)
tracer_provider.add_span_processor(span_processor)
trace_api.set_tracer_provider(tracer_provider)

# Get the tracer object
tracer = trace_api.get_tracer(__name__)

class AIMLAPI(LM):
    def __init__(self, model, api_key, **kwargs):
        super().__init__(model)
        self.api_key = api_key
        self.base_url = "https://api.aimlapi.com/chat/completions"
        self.kwargs.update(kwargs)
        self.provider = "AIMLAPI"

    def basic_request(self, prompt: str, **kwargs):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}',
        }

        data = {
            "model": self.kwargs["model"],
            "messages": [{"role": "user", "content": prompt}],
            **{k: v for k, v in kwargs.items() if k in self.kwargs}
        }
        # Start a new span for the HTTP request
        with tracer.start_as_current_span("AIMLAPI basic_request") as span:
            # Optionally add some attributes to the span
            span.set_attribute("api.model", self.kwargs["model"])
            span.set_attribute("api.prompt", prompt)
            
            response = requests.post(self.base_url, headers=headers, json=data)
            # Trace the full raw HTTP response content
            span.set_attribute("http.full_response_body", response.text)  # Warning: large bodies can be problematic

            response.raise_for_status()
        
             # Record the response status code
            span.set_attribute("http.status_code", response.status_code)
        
            response_json = response.json()
            

        self.history.append({
            "prompt": prompt,
            "response": response_json,
            "kwargs": kwargs,
        })

        return response_json

    def __call__(self, prompt, only_completed=True, return_sorted=False, **kwargs):
        response = self.basic_request(prompt, **kwargs)
        if 'choices' in response and len(response['choices']) > 0:
            return [choice['message']['content'] for choice in response['choices']]
        return "No valid response found"

if __name__ == "__main__":
    
    # Load environment variables
    load_dotenv()

    # Set your API key and endpoint
    AIML_API_KEY = os.getenv("AIML_API_KEY")
    model = "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo"

    llama_lm = AIMLAPI(
        model=model,
        api_key=AIML_API_KEY,
        temperature=0.7,
        max_tokens=100,
        n=1
    )

    dspy.settings.configure(lm=llama_lm, temperature=0.7, max_tokens=1000, n=1)

    prompt = "I want to ask about the universe"

    # Process with Predict
    processed_response = dspy.ChainOfThought("question -> answer", n=1)(question=prompt)
    answer = processed_response.answer

    # Debugging 3: Print the full processed response: Bad response [returning the first character]
    print("Answer: ", answer)