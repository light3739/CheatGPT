import base64
import logging
import queue
import tkinter as tk
from datetime import datetime
from typing import List, Dict

import keyboard
import mss
import mss.tools
import openai
import pyperclip


# Logging setup with custom handler
class QueueHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.log_queue = queue.Queue()
        self.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    def emit(self, record):
        self.log_queue.put(self.format(record))


# Constants

API_KEY = ""
MODEL_NAME = "gpt-4o"
TEXT_MODEL = "gpt-4o"
HOTKEY = 'ctrl+shift+z'
OK_WINDOW_COLOR = "#28a745"  # Bootstrap green
ERROR_WINDOW_COLOR = "#dc3545"  # Bootstrap red
WINDOW_SIZE = "10x10+0+0"  # Increased window size for better visibility
SCREENSHOT_HOTKEY = 'ctrl+shift+x'


class ChatBot:
    def __init__(self, api_key: str, model_name: str):
        self.client = openai.OpenAI(
            api_key=api_key,
            timeout=60.0
        )
        self.model_name = model_name
        self.text_model = TEXT_MODEL
        self.conversation_history: List[Dict[str, str]] = []
        self.cached_responses: Dict[str, str] = {}
        self.max_history = 10
        self.logger = logging.getLogger(__name__)
        self.sct = mss.mss()
        self.system_prompt = {
            "role": "system",
            "content": "You are an Assembly code expert. Provide only code solutions without explanations or comments. Focus on pure code implementation. For questions, provide direct answers without additional context."
        }
        self.conversation_history.append(self.system_prompt)

    def add_to_history(self, role: str, content: str) -> None:
        """Add a message to conversation history"""
        self.conversation_history.append({
            "role": role,
            "content": content
        })
        # Trim history if it exceeds max_history
        if len(self.conversation_history) > self.max_history:
            self.conversation_history = self.conversation_history[-self.max_history:]

    def get_cached_response(self, user_input: str) -> str:
        """Get cached response if available"""
        return self.cached_responses.get(user_input)

    def cache_response(self, user_input: str, response: str) -> None:
        """Cache a response"""
        self.cached_responses[user_input] = response
        # Limit cache size to last 100 responses
        if len(self.cached_responses) > 100:
            # Remove oldest entry
            self.cached_responses.pop(next(iter(self.cached_responses)))

    def chat(self, user_input: str):
        cached_response = self.get_cached_response(user_input)
        if cached_response:
            return cached_response

        # Assembly-specific prompt
        custom_prompt = "Provide only the code or answer without any explanations or comments: "
        formatted_input = f"{custom_prompt}{user_input}"

        self.add_to_history("user", formatted_input)

        try:
            chat_completion = self.client.chat.completions.create(
                model=self.text_model,
                messages=self.conversation_history,
                temperature=0.3,  # Lower temperature for more precise answers
                max_tokens=2000
            )

            response = chat_completion.choices[0].message.content
            self.add_to_history("assistant", response)
            self.cache_response(user_input, chat_completion)

            return chat_completion

        except Exception as e:
            raise

    def clear_history(self) -> None:
        """Clear conversation history"""
        self.conversation_history.clear()
        self.logger.info("Conversation history cleared")

    def get_history(self) -> List[Dict[str, str]]:
        """Get current conversation history"""
        return self.conversation_history

    def get_history_size(self) -> int:
        """Get current history size"""
        return len(self.conversation_history)

    def capture_screenshot_to_base64(self):
        """Capture screenshot and return as base64 string"""
        try:
            with mss.mss() as sct:
                # Capture the main monitor
                monitor = sct.monitors[1]
                screenshot = sct.grab(monitor)

                # Convert to PNG bytes without saving to disk
                png_bytes = mss.tools.to_png(screenshot.rgb, screenshot.size)

                # Convert bytes to base64
                return base64.b64encode(png_bytes).decode('utf-8')
        except Exception as e:
            self.logger.error(f"Screenshot capture error: {str(e)}")
            raise

    def chat_with_image(self, base64_image: str, prompt: str = "Provide only the code solution without explanations:"):
        try:
            messages = [
                {
                    "role": "system",
                    "content": "You are an Assembly code expert. Provide only code solutions or direct answers without explanations or comments."
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}",
                                "detail": "high"
                            }
                        }
                    ]
                }
            ]

            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                max_tokens=2000,
                temperature=0.3
            )

            return response

        except Exception as e:
            raise


# Update the on_hotkey_press function to use the new features
def on_hotkey_press(chat_bot, logger):
    try:
        logger.info(f"{HOTKEY} pressed")
        selected_text = pyperclip.paste()

        # Log history size before chat
        logger.info(f"History size before chat: {chat_bot.get_history_size()}")

        chat_completion = chat_bot.chat(selected_text)
        response = chat_completion.choices[0].message.content

        # Log history size after chat
        logger.info(f"History size after chat: {chat_bot.get_history_size()}")

        pyperclip.copy(response)
        notification = NotificationWindow(OK_WINDOW_COLOR, WINDOW_SIZE)
        notification.show()

    except Exception as e:
        logger.error(f"Error in hotkey handler: {str(e)}")
        notification = NotificationWindow(ERROR_WINDOW_COLOR, WINDOW_SIZE)
        notification.show()


def on_screenshot_hotkey(chat_bot, logger):
    try:
        logger.info(f"{SCREENSHOT_HOTKEY} pressed")
        base64_image = chat_bot.capture_screenshot_to_base64()
        logger.info("Screenshot captured and converted to base64")

        chat_completion = chat_bot.chat_with_image(base64_image)
        response = chat_completion.choices[0].message.content

        logger.info(f"Response generated: {response[:100]}...")
        pyperclip.copy(response)

        notification = NotificationWindow(OK_WINDOW_COLOR, WINDOW_SIZE)
        notification.show()

    except Exception as e:
        logger.error(f"Error in screenshot handler: {str(e)}")
        notification = NotificationWindow(ERROR_WINDOW_COLOR, WINDOW_SIZE)
        notification.show()


class NotificationWindow:
    def __init__(self, color, size):
        self.root = tk.Tk()
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 0.9)
        self.root.overrideredirect(True)
        self.root.geometry(size)

        # Create frame with border
        self.frame = tk.Frame(
            self.root,
            background=color,
            borderwidth=2,
            relief="raised"
        )
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Add status label
        self.label = tk.Label(
            self.frame,
            text="Processing..." if color == OK_WINDOW_COLOR else "Error!",
            background=color,
            foreground="white",
            font=("Arial", 12, "bold")
        )
        self.label.pack(pady=10)

    def show(self, duration=1000):
        self.root.after(duration, self.root.destroy)
        self.root.mainloop()


def setup_logging():
    queue_handler = QueueHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    queue_handler.setFormatter(formatter)

    # # Also add file handler
    # file_handler = logging.FileHandler(f'chatbot_{datetime.now().strftime("%Y%m%d")}.log')
    # file_handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(queue_handler)
    # logger.addHandler(file_handler)

    return logger


def main():
    logger = setup_logging()
    chat_bot = ChatBot(API_KEY, MODEL_NAME)

    keyboard.add_hotkey(HOTKEY, lambda: on_hotkey_press(chat_bot, logger))
    keyboard.add_hotkey(SCREENSHOT_HOTKEY, lambda: on_screenshot_hotkey(chat_bot, logger))
    keyboard.wait()


if __name__ == "__main__":
    main()
