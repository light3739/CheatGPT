import keyboard


def on_ctrl_c_c_press(e):
    print("Ctrl+C+C was pressed")


# Listen for the CTRL+C+C key combination
keyboard.add_hotkey('ctrl+c+c', on_ctrl_c_c_press)

# Keep the script running
keyboard.wait()

import tkinter as tk

# Create the main window
root = tk.Tk()
root.attributes('-topmost', True)  # Keep the window on top of others

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Create a white dot
dot = tk.Label(root, text="●", font=("Arial", 20), fg="white", bg="white")
dot.place(x=screen_width-20, y=screen_height-20)  # Position the dot in the lower right corner

# After two seconds, remove the dot
root.after(2000, dot.destroy)

# Run the application
root.mainloop()