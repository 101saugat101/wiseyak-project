def chatbot_response(user_input):
    """
    A simple decision-tree-based chatbot with symptom handling.
    Tracks conversation state to ensure the bot responds properly.
    """
    global conversation_state

    user_input = user_input.lower().strip() 

    if conversation_state == "start":
        if "hello" in user_input:
            conversation_state = "asked_feeling" 
            return "Hello, how can I assist you today? Are you feeling well?"
        else:
            return "I don't understand that. Please say 'hello' first to begin."

    elif conversation_state == "asked_feeling":
        if "yes" in user_input:
            return "Great! I'm glad to hear that. How can I assist you today?"
        elif "no" in user_input:
            conversation_state = "asked_symptoms" 
            return "I'm sorry to hear that. Can you tell me more about what's bothering you? Are you feeling feverish, dizzy, or have a headache?"
        else:
            return "I don't understand that. Can you please answer 'yes' or 'no' to how you're feeling?"

    elif conversation_state == "asked_symptoms":
        if "fever" in user_input:
            return "A fever can indicate an infection or illness. Make sure you're staying hydrated and resting. Would you like more information?"
        elif "headache" in user_input:
            return "A headache can be caused by many things. If it's persistent, it might be a good idea to see a doctor. Would you like tips to relieve it?"
        elif "dizziness" in user_input:
            return "Dizziness can happen for various reasons. Make sure you're hydrated and get enough rest. If it continues, please consult with a doctor."
        else:
            return "I don't understand that. Please mention a symptom like fever, dizziness, or headache."

    # For subsequent greetings, prompt for how the user is feeling
    elif "hello" in user_input:
        return "Hello again! Are you feeling well?"

    else:
        return "I don't understand that. Can you ask me something else?"

conversation_state = "start"  # Initial state of the conversation

