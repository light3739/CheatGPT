import asyncio
from openai import AsyncOpenAI
import keyboard
import pyperclip

client = AsyncOpenAI(
  api_key="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",
)

# Initialize an empty list to hold the conversation history
conversation_history = []

async def chat_with_model(user_input):
  global conversation_history
  # Add the user's message to the conversation history
  conversation_history.append({
      "role": "user",
      "content": user_input
  })

  chat_completion = await client.chat.completions.create(
      messages=conversation_history,
      model="gpt-3.5-turbo",
  )

  # Add the model's response to the conversation history
  conversation_history.append({
      "role": "assistant",
      "content": chat_completion.choices[0].message.content
  })

  print(chat_completion.choices[0].message.content)

def on_ctrl_c_c_press(e):
  # Get the selected text
  selected_text = pyperclip.paste()

  # Start a new coroutine to chat with the model
  asyncio.run(chat_with_model(selected_text))

# Listen for the CTRL+C+C key combination
keyboard.add_hotkey('ctrl+c+c', on_ctrl_c_c_press)

# Keep the script running
keyboard.wait()
