# Import required libraries
from AppOpener import close, open as appopen
from webbrowser import open as webopen
from pywhatkit import search, playonyt
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from rich import print
from groq import Groq
import webbrowser
import subprocess
import requests
import keyboard
import asyncio
import os


env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")

# Initialize the Groq client
client = Groq(api_key=GroqAPIKey)

# HTML class names for parsing
classes = [
    "zCubwf", "hgKElc", "LTKOO SY7ric", "ZOLCW", "gsrt vk_bk FzvWSb YwPhnf", "pclqee",
    "tw-Data-text tw-text-small tw-ta", "IZ6rdc", "05uR6d LTKOO", "vlzY6d",
    "webanswers-webanswers_table___webanswers-table", "dDoNo ikb4Bb gsrt", "sXLa0e",
    "LWkfKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"
]

useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'

# Responses
professional_responses = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
    "I'm at your service for any additional questions or support you may need - don't hesitate to ask."
]

messages = []
SystemChatBot = [{"role": "system", "content": "You're a content writer. You have to write content professionally."}]

# Functions



def GoogleSearch(topic):
    search(topic)
    return True

def Content(topic):
    def OpenNotepad(file):
        default_text_editor = 'notepad.exe'
        subprocess.Popen([default_text_editor, file])

    def ContentWriterAI(prompt):
        messages.append({"role": "user", "content": prompt})
        completion = client.chat.completions.create(
            model="llama3-8b-8192",  # Or another valid model name
            messages=SystemChatBot + messages,
            max_tokens=2048,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )
        answer = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                answer += chunk.choices[0].delta.content
        answer = answer.replace("</s>", "")
        messages.append({"role": "assistant", "content": answer})
        return answer

    topic: str = topic.replace("Content", "")
    contentByAI = ContentWriterAI(topic)

    with open(rf"Data\{topic.lower().replace('','')}.txt", "w", encoding="utf-8") as file:
        file.write(contentByAI)
        file.close()

    OpenNotepad(rf"Data\{topic.lower().replace('','')}.txt")
    return True




def YouTubeSearch(topic):
    webbrowser.open(f"https://www.youtube.com/results?search_query={topic}")
    return True

def PlayYoutube(query):
    playonyt(query)
    return True



def OpenApp(app, sess=requests.session()):
    try:
        appopen(app, match_closest=True, output=True, throw_error=True)
        return True
    except:
        print(f"App '{app}' not found locally. Searching on Google...")
        query = f"{app} download or open site"
        url = f"https://www.google.com/search?q={query}"

        # Path to Chrome (adjust if yours is different)
        chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"

        try:
            webbrowser.get(chrome_path).open(url)
            return True
        except webbrowser.Error:
            # Fallback if custom chrome path fails
            webbrowser.open(url)
            return True




#OpenApp("Camera")

def CloseApp(app):
    if 'chrome' in app:
        return False
    else:
        try:
            close(app, match_closest=True, output=True, throw_error=True)
            return True
        except:
            return False

def System(command):
    def mute():
        keyboard.press_and_release('volume mute')

    def unmute():
        keyboard.press_and_release('volume mute')

    def volume_up():
        keyboard.press_and_release('volume up')

    def volume_down():
        keyboard.press_and_release('volume down')

    if command == 'mute': mute()
    elif command == 'unmute': unmute()
    elif command == 'volume up': volume_up()
    elif command == 'volume down': volume_down()
    return True

def extract_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all('a', {'jsname': 'UWckNb'})
    return [link.get('href') for link in links]

def search_google(query):
    url = f"https://www.google.com/search?q={query}"
    headers = {"User-Agent": useragent}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    print("Failed to retrieve search results.")
    return None

# Asynchronous Functions
async def TranslateAndExecute(commands: list[str]):
    funcs = []
    for command in commands:
        if command.startswith("open "):
            if "open it" in command or "open file" in command:
                continue
            fun = asyncio.to_thread(OpenApp, command.removeprefix("open "))
            funcs.append(fun)
        elif command.startswith("close"):
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close"))
            funcs.append(fun)
        elif command.startswith("play "):
            fun = asyncio.to_thread(PlayYoutube, command.removeprefix("play "))
            funcs.append(fun)
        elif command.startswith("content"):
            fun = asyncio.to_thread(Content, command.removeprefix("content"))
            funcs.append(fun)
        elif command.startswith("google search "):
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search "))
            funcs.append(fun)
        elif command.startswith("youtube search "):
            fun = asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search "))
            funcs.append(fun)
        elif command.startswith("system "):
            fun = asyncio.to_thread(System, command.removeprefix("system "))
            funcs.append(fun)
        else:
            print(f"No Function Found for {command}")

    results = await asyncio.gather(*funcs)
    for result in results:
        yield result

async def Automation(commands: list[str]):
    async for result in TranslateAndExecute(commands):
        pass
    return True
