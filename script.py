import openai
import keyboard
import pyperclip
import logging

# Configure the logging module
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize the OpenAI client
client = openai.OpenAI(api_key="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")

# Initialize an empty list to hold the conversation history
conversation_history = []


def chat_with_model(user_input):
    global conversation_history
    # Add the user's message to the conversation history
    conversation_history.append({
        "role": "user",
        "content": user_input
    })

    chat_completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=conversation_history
    )

    # Add the model's response to the conversation history
    conversation_history.append({
        "role": "assistant",
        "content": chat_completion.choices[0].message.content
    })

    return chat_completion


def on_ctrl_c_c_press():
    # Get the selected text
    logging.info("Ctrl+shift+z pressed")
    selected_text = pyperclip.paste()
    logging.info(selected_text)
    # Call the chat function
    chat_completion = chat_with_model(selected_text)
    logging.info(chat_completion.choices[0].message.content)


# Listen for the CTRL+C+C key combination
keyboard.add_hotkey('ctrl+shift+z', on_ctrl_c_c_press)

# Keep the script running
keyboard.wait()
