VERSION = "2025.08.29"
import webview # pip install pywebview
import sys
import json
import os
import tkinter as tk

print(f"weBox Version: {VERSION}")
def calculate_window_position(position_type, screen_width, screen_height):
    """
    Calculate window dimensions and position based on screen size and position type.

    Args:
        position_type (str): Position type ("FullScreen", "Left", "Right", "None")
        screen_width (int): Screen width
        screen_height (int): Screen height

    Returns:
        tuple: (width, height, x, y) for window positioning
    """
    if position_type == "FullScreen":
        return screen_width, screen_height, 0, 0
    elif position_type == "Left":
        width = screen_width // 2
        height = screen_height
        x = 0
        y = 0
        return width, height, x, y
    elif position_type == "Right":
        width = screen_width // 2
        height = screen_height
        x = screen_width // 2
        y = 0
        return width, height, x, y
    else:
        # Default values or keep existing config
        return app_config["width"], app_config["height"], app_config["x"], app_config["y"],

def open_webpage_in_window(url, title, width, height, x, y, frameless=False, position_type="None", resizable=False, position_type_options=None):
    """
    Opens a webpage in a dedicated window with specified dimensions and position.

    Args:
        url (str): The URL of the webpage to open.
        title (str): The title of the window.
        width (int): The width of the window.
        height (int): The height of the window.
        x (int): The x-coordinate of the window's top-left corner.
        y (int): The y-coordinate of the window's top-left corner.
        frameless (bool): Whether to create a window without a title bar.
        position_type (str): Position type ("FullScreen", "Left", "Right", "None")
    """
    try:
        # Get screen size
        if position_type == "FullScreen":
            webview.create_window(title, url, fullscreen=True)
        else:

            #screen_width, screen_height = webview.screens()[0].width, webview.screens()[0].height
            root = tk.Tk()
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            # Calculate window position based on position type
            calc_width, calc_height, calc_x, calc_y = calculate_window_position(position_type, screen_width, screen_height)
            
            # Create a pywebview window
            webview.create_window(
                title,
                url,
                width=calc_width,
                height=calc_height,
                x=calc_x,
                y=calc_y,
                resizable=resizable,  # Or False if you want a fixed-size window
                frameless=frameless
            )
        # Start the pywebview event loop
        webview.start()
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        print("Please ensure you have a compatible GUI backend installed, like PyQt5.", file=sys.stderr)
        print("You can try running: pip install pywebview[qt]", file=sys.stderr)
        sys.exit(1)

def load_config():
    """
    Loads configuration from a JSON file named after the script.
    If the file doesn't exist, it's created with default values.
    Returns a dictionary with the configuration.
    """
    # --- Default Configuration ---
    default_config = {
        "url": "https://www.ydreams.global",
        "title": "Frameless Window Example",
        "width": 1024,
        "height": 768,
        "x": 50,
        "y": 50,
        "frameless": False,
        "position_type": "FullScreen",  # New option: "FullScreen", "Left", "Right", "None"
        "position_type_options" : "FullScreen, Left, Right, None"
    }

    try:
        # Determine config file path based on the script's name (e.g., main.py -> main.json)
        script_path = os.path.abspath(__file__)
        config_path = os.path.splitext(script_path)[0] + '.json'
    except NameError:
        # Fallback if __file__ is not defined (e.g., in an interactive interpreter)
        config_path = 'main.json'

    config = default_config.copy()

    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                user_config = json.load(f)
                config.update(user_config) # Overrides defaults with settings from file
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error reading config file '{config_path}': {e}", file=sys.stderr)
            print("Using default settings.", file=sys.stderr)
    else:
        print(f"Configuration file '{config_path}' not found. Creating with default settings.")
        try:
            with open(config_path, 'w') as f:
                json.dump(default_config, f, indent=4)
        except IOError as e:
            print(f"Error creating config file '{config_path}': {e}", file=sys.stderr)

    return config

if __name__ == '__main__':
    # Load configuration from JSON file or use/create defaults
    app_config = load_config()

    open_webpage_in_window(**app_config)
    print("Window closed.")
