from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from models import ChatHistory
from database import get_db, engine, Base

app = FastAPI()

conversation_state = "greeting"

# Input model for chat request
class ChatRequest(BaseModel):
    user: str 

@app.on_event("startup")
async def startup():
    # Create the tables when FastAPI starts
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/chat")
async def chatbot_endpoint(request: ChatRequest, db: Session = Depends(get_db)):
    global conversation_state
    user_message = request.user.lower().strip()

    # Conversation flow logic
    if conversation_state == "greeting":
        if "hello" in user_message:
            conversation_state = "ask_wellbeing"
            bot_message = "Hello! How can I help you? Are you feeling well? (yes/no)"
        else:
            bot_message = "Please say 'hello' to start the conversation."

    elif conversation_state == "ask_wellbeing":
        if "yes" in user_message:
            conversation_state = "end"
            bot_message = "Great! Let me know if you need any further assistance."
        elif "no" in user_message:
            conversation_state = "ask_symptoms"
            bot_message = "I'm sorry to hear that. What are you experiencing? Options: fever, headache, dizziness."
        else:
            bot_message = "Please respond with 'yes' or 'no'."

    elif conversation_state == "ask_symptoms":
        if "fever" in user_message:
            bot_message = "It sounds like you might have an infection. Drink plenty of fluids and get some rest."
        elif "headache" in user_message:
            bot_message = "A headache can be caused by stress or dehydration. Try relaxing and drink water."
        elif "dizziness" in user_message:
            bot_message = "Dizziness might be due to fatigue or low blood sugar. Take a break and eat something light."
        else:
            bot_message = "I didn't understand that. Please mention one of the symptoms: fever, headache, dizziness."
        conversation_state = "end"  # End the conversation after responding to symptoms

    elif conversation_state == "end":
        bot_message = "If you need further assistance, feel free to start over by saying 'hello'."

    else:
        bot_message = "I'm not sure what you're saying. Please restart the conversation by saying 'hello'."

    # Save chat history to the database
    chat_entry = ChatHistory(user_message=request.user, bot_response=bot_message)
    db.add(chat_entry)
    await db.commit()

    # Return the bot's response
    return {"bot": bot_message}

@app.get("/chat/history")
async def get_chat_history(db: Session = Depends(get_db)):
    result = await db.execute(select(ChatHistory).order_by(ChatHistory.id.desc()))
    history = result.scalars().all()
    return [
        {"user_message": chat.user_message, "bot_response": chat.bot_response, "timestamp": chat.timestamp}
        for chat in history
    ]
