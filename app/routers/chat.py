import openai
import os
from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from ..dependencies import get_db
from dotenv import load_dotenv

load_dotenv()

AI71_API_KEY = os.getenv("AI71_API_KEY")
AI71_BASE_URL = os.getenv("AI71_BASE_URL")

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/chat")
async def chat(request: Request):
    """Chat page"""
    return templates.TemplateResponse("chat.html", {"request": request})


@router.post("/chat/message")
async def chat_message(request: Request, db: Session = Depends(get_db)):
    """Chat interaction"""
    data = await request.json()
    user_message = data.get("message")

    if not user_message:
        return {"response": "No message provided."}, 400

    # Initialize conversation history if not present
    if not hasattr(request.state, "conversation_history"):
        request.state.conversation_history = []

    # Append the user message to the conversation history
    request.state.conversation_history.append({"sender": "user", "message": user_message})

    # Create context for the AI model
    conversation_history = "\n".join(
        f"{entry['sender']}: {entry['message']}"
        for entry in request.state.conversation_history
    )

    try:
        openai_client = openai.OpenAI(api_key=AI71_API_KEY,base_url=AI71_BASE_URL)
        system_prompt = """You are Senu. A Conversational AI Startup Copilot, you are in a chat window 
                            having a conversation with the user, your mission is to extract data from the user about their startup including 
                            their team, fundraising, market, business model, product and traction"""
        response = ""
        messages = [
            {"role": "system", "content": f"{system_prompt}"},
        ] + [{"role": "user", "content": f"{user_message}"}]

        # Simple invocation:
        for chunk in openai_client.chat.completions.create(
            model="tiiuae/falcon-180b-chat", messages=messages, stream=True
        ):
            if chunk.choices[0].delta.content:
                print(f"{chunk}")
                print(f"Request data: {data}")
                print(f"Conversation history: {request.state.conversation_history}")
                print(f"Messages sent to API: {messages}")
                response += chunk.choices[0].delta.content
        # # Configure DSPy
        # falcon_lm = dspy.Any(model="tiiuae/falcon-11b", base_url=AI71_BASE_URL, api_key=AI71_API_KEY)
        # dspy.configure(lm=falcon_lm)

        # # Create a prompt for the AI
        # prompt = f"User: {user_message}"
        # conversation_history = system_prompt + prompt
        # # Generate a response using DSPy
        # response =  dspy.ChainOfThought("question, context -> answer", n=5)(question=prompt, context=conversation_history)
        print(f"{response}")

        ai_response = response

        # Append the bot response to the conversation history
        request.state.conversation_history.append(
            {"sender": "assistant", "message": ai_response}
        )

        return {"response": ai_response}

    except Exception as e:
        return {"response": f"An error occurred: {str(e)}"}, 500
    