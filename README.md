# ChatBot Application

## Description

This ChatBot application is designed to interact with users by capturing their selected text and generating responses
using OpenAI’s GPT-4 model. It uses a hotkey-triggered mechanism (`ctrl+shift+z`by default), allowing users to select
text anywhere in their system, activate the chatbot with a hotkey, and receive an AI-generated response based on the
selected text.

## Features

- Hotkey activation (`ctrl+shift+z`by default) for ease of use.
- Utilizes OpenAI’s powerful GPT-4 model for generating responses.
- Simple UI feedback for successful or erroneous processing.
- Text is automatically copied to the clipboard for quick use.

## Requirements

- Python 3.x
- OpenAI API Key
- Dependencies listed in`requirements.txt`

## Installation

First, clone the repository to your local machine:

```
git clone https://github.com/light3739/CheatGPT
cd CheatGPT
```

Then, install the required Python packages:

```
pip install -r requirements.txt
```

## Configuration

1. Add your OpenAI API key to the`script.py`file as follows:

    ```
    OPENAI_API_KEY=your_api_key_here
    ```

## Usage

Run the script with the following command:

```
python script.py
```

After selecting text, use the hotkey (`ctrl+shift+z`by default) to activate the ChatBot:

1. CTRL + C on selected text
2. CTRL + SHIFT + Z to activate the ChatBot
3. You will see green square in top left corner of your screen for 1 second
4. CTRL + V to paste the response

## Building the Application as an Executable

To build this application as an executable for Windows, follow these steps:

1. Install PyInstaller using pip:

    ```
    pip install pyinstaller==5.13.2
    ```

2. Run PyInstaller with your script:

    ```
    pyinstaller --noconfirm --onefile --hidden-import=keyboard --windowed script.py
    ```

    - `--onefile`: Packs everything into a single executable.
    - `--hidden-import=keyboard`: Ensures the`keyboard`module is included.
    - `--windowed`: Prevents a console window from opening when the executable is run.

3. Find the resulting`.exe`file in the`dist`folder after the build process completes.

## Notes

- The executable may have a longer startup time compared to the Python script.
- The executable’s first run might trigger antivirus software due to its behavior (keyboard monitoring). This is
  commonly a false positive, but users should use their discretion and assess security risks individually.