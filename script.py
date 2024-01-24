import tkinter as tk
import openai
import keyboard
import pyperclip
import logging

from dotenv import load_dotenv
import os

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Retrieve API key from environment variables
API_KEY = os.getenv('OPENAI_API_KEY')
MODEL_NAME = "gpt-4-1106-preview"
HOTKEY = 'ctrl+shift+z'
OK_WINDOW_COLOR = "green"
ERROR_WINDOW_COLOR = "red"
WINDOW_SIZE = "10x10+0+0"


class ChatBot:
    def __init__(self, api_key, model_name):
        self.client = openai.OpenAI(api_key=api_key)
        self.model_name = model_name
        self.conversation_history = []

    def chat(self, user_input):
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })

        try:
            chat_completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=self.conversation_history
            )
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return show_window(ERROR_WINDOW_COLOR, WINDOW_SIZE)

        self.conversation_history.append({
            "role": "assistant",
            "content": chat_completion.choices[0].message.content
        })

        return chat_completion


chat_bot = ChatBot(API_KEY, MODEL_NAME)


def show_window(color, size):
    root = tk.Tk()
    root.attributes('-topmost', True)
    root.attributes('-alpha', 0.5)
    root.overrideredirect(True)
    root.geometry(size)
    root.configure(background=color)
    root.after(500, root.destroy)
    root.mainloop()


def on_hotkey_press():
    global chat_bot
    logging.info(f"{HOTKEY} pressed")
    selected_text = pyperclip.paste()
    logging.info(selected_text)
    chat_completion = chat_bot.chat(selected_text)
    logging.info(chat_completion.choices[0].message.content)

    pyperclip.copy(chat_completion.choices[0].message.content)
    show_window(OK_WINDOW_COLOR, WINDOW_SIZE)


keyboard.add_hotkey(HOTKEY, on_hotkey_press)
keyboard.wait()
