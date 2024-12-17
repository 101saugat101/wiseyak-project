from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ChatRequest(BaseModel):
    user: str              # User message

conversation_state = "greeting"
conversation_history = []

@app.post("/chat")
def chatbot_endpoint(request: ChatRequest):
    global conversation_state
    user_message = request.user.lower().strip()

    # Add user message to the conversation history
    conversation_history.append({"user": request.user})





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
        conversation_state = "end" 

    elif conversation_state == "end":
        bot_message = "If you need further assistance, feel free to start over by saying 'hello'."
        conversation_state = "greeting"  # Reset the conversation state

    else:
        bot_message = "I'm not sure what you're saying. Please restart the conversation by saying 'hello'."





    # Add bot message to conversation history
    conversation_history.append({"bot": bot_message})

    # Return bot response and conversation history
    return {"bot": bot_message, "history": conversation_history}
