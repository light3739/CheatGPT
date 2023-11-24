import keyboard


def on_ctrl_c_c_press(e):
    print("Ctrl+C+C was pressed")


# Listen for the CTRL+C+C key combination
keyboard.add_hotkey('ctrl+c+c', on_ctrl_c_c_press)

# Keep the script running
keyboard.wait()
