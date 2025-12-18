import os
import json
import datetime
from dotenv import load_dotenv
from groq import Groq

# Load environment variables 
load_dotenv()

# Get API key from env
api_key = os.getenv("GroqAPIKey")

# Function to fetch Username and Assistant name from env
def get_env_values():
    username = os.getenv("USERNAME", "User")
    assistantname = os.getenv("ASSISTANTNAME", "Assistant")
    return username, assistantname

# Assign dynamic values
Username, Assistantname = get_env_values()

# Initialize Groq client
client = Groq(api_key=api_key)

# Model
MODEL_NAME = "llama3-70b-8192"  # Updated supported model

# File path for chatlog
chatlog_path = "Data/ChatLog.json"
os.makedirs("Data", exist_ok=True)

# Ensure ChatLog file exists
if not os.path.exists(chatlog_path):
    with open(chatlog_path, "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=4)

# Load previous chatlog
def load_chat_log():
    with open(chatlog_path, "r", encoding="utf-8") as f:
        return json.load(f)

# Save updated chatlog
def save_chat_log(messages):
    with open(chatlog_path, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=4)

# Real-time info function
def RealtimeInformation():
    now = datetime.datetime.now()
    return (
        f"Please use this real-time information if needed:\n"
        f"Day: {now.strftime('%A')}\n"
        f"Date: {now.strftime('%d')}\n"
        f"Month: {now.strftime('%B')}\n"
        f"Year: {now.strftime('%Y')}\n"
        f"Time: {now.strftime('%H')} hours {now.strftime('%M')} minutes {now.strftime('%S')} seconds.\n"
    )

# Clean up long or messy output 
def AnswerModifier(answer):
    lines = answer.split('\n')
    return '\n'.join([line.strip() for line in lines if line.strip()])

# Define initial system prompt
SystemPrompt = f"""Hello, I am {Username}, You are a very accurate and advanced AI assistant for you named {Assistantname}.
*** Do not tell time until I ask, do not talk too much, just answer the question. ***
*** Reply in only English, even if the question is in Hindi, reply in English. ***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""

SystemChatBot = [{"role": "system", "content": SystemPrompt}]

# Main chatbot logic
def ChatBot(Query):
    try:
        messages = load_chat_log()
        messages.append({"role": "user", "content": Query})

        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=SystemChatBot + [{"role": "system", "content": RealtimeInformation()}] + messages,
            max_tokens=1024,
            temperature=0.7,
            top_p=1,
            stream=False
        )

        assistant_reply = completion.choices[0].message.content.strip().replace("</s>", "")
        messages.append({"role": "assistant", "content": assistant_reply})
        save_chat_log(messages)

        return AnswerModifier(assistant_reply)

    except Exception as e:
        print("Error:", e)
        save_chat_log([])  # Reset chat log on error
        return "Oops! Something went wrong. Please try again."

# Run it
if __name__ == "__main__":
    print(f"🤖 {Assistantname} is online. Type 'exit' to quit.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print(f"{Assistantname}: Goodbye! 👋")
            break
        response = ChatBot(user_input)
        print(f"{Assistantname}:", response)
