import sys
import os
import subprocess

# Redirect stdout and stderr to a log file in the user's home directory
log_file_path = os.path.join(os.path.expanduser('~/middleclicksquared/Logs'), 'gesture_control_log.txt')
log_file = open(log_file_path, 'w', buffering=1)  # Line-buffered
sys.stdout = log_file
sys.stderr = log_file

from pynput import mouse, keyboard
import time
import subprocess

# Variables to track the state
middle_button_pressed = False
start_position = None
gesture_executed = False  # Flag to track if a gesture has been executed
key_pressed = {  # Track the state of each arrow key
    "Up": False,
    "Down": False,
    "Left": False,
    "Right": False
}

# Variables to track action frequency
last_action = None
action_count = 0
action_start_time = time.time()

# Add to the top with other global variables
developer_mode = False  # Default to user mode

# Define actions for each gesture
def volume_up():
    print("Volume Up Commanded")
    subprocess.run(['osascript', '-e', 'set volume output volume (output volume of (get volume settings) + 10) --100%'], capture_output=True)

def volume_down():
    print("Volume Down Commanded")
    subprocess.run(['osascript', '-e', 'set volume output volume (output volume of (get volume settings) - 10) --100%'], capture_output=True)

def swipe_left():
    print("Three Finger Swipe Left Commanded")
    subprocess.run(['osascript', '-e', 'tell application "System Events" to key code 123 using {control down}'], capture_output=True)

def swipe_right():
    print("Three Finger Swipe Right Commanded")
    subprocess.run(['osascript', '-e', 'tell application "System Events" to key code 124 using {control down}'], capture_output=True)

gesture_actions = {
    "Up": volume_up,
    "Down": volume_down,
    "Left": swipe_left,
    "Right": swipe_right
}

def execute_action(action):
    global last_action, action_count, action_start_time

    current_time = time.time()
    if last_action == action:
        if current_time - action_start_time <= 60:
            action_count += 1
            print(f"Action count for {action}: {action_count}")
            if action_count > 20:
                print("Too many repeated actions. Shutting down.")
                exit()
        else:
            action_count = 1
            action_start_time = current_time
    else:
        last_action = action
        action_count = 1
        action_start_time = current_time

    gesture_actions[action]()

def on_move(x, y):
    global middle_button_pressed, start_position, gesture_executed
    if middle_button_pressed:
        if start_position is None:
            start_position = (x, y)
        else:
            dx = x - start_position[0]
            volume_change = dx / 5  # Adjust sensitivity as needed
            current_volume = get_current_volume()
            new_volume = max(0, min(100, current_volume + volume_change))
            set_volume(new_volume)
            start_position = (x, y)

def get_current_volume():
    result = subprocess.run(['osascript', '-e', 'output volume of (get volume settings)'], capture_output=True, text=True)
    return int(result.stdout.strip())

def set_volume(volume):
    subprocess.run(['osascript', '-e', f'set volume output volume {volume}'], capture_output=True)

def on_click(x, y, button, pressed):
    global middle_button_pressed, start_position, gesture_executed
    if button == mouse.Button.middle:
        middle_button_pressed = pressed
        if not pressed:
            start_position = None  # Reset when the button is released
            gesture_executed = False  # Reset gesture executed flag

def on_press(key):
    try:
        # Check for mode toggle (Tab key)
        if key == keyboard.Key.tab:
            toggle_developer_mode()
            return

        # Only process WASD in developer mode
        if not developer_mode:
            return

        key_char = getattr(key, 'char', None)
        if key_char == 'w' and not key_pressed["Up"]:
            print("Key W Pressed")
            execute_action("Up")
            key_pressed["Up"] = True
        elif key_char == 's' and not key_pressed["Down"]:
            print("Key S Pressed")
            execute_action("Down")
            key_pressed["Down"] = True
        elif key_char == 'a' and not key_pressed["Left"]:
            print("Key A Pressed")
            execute_action("Left")
            key_pressed["Left"] = True
        elif key_char == 'd' and not key_pressed["Right"]:
            print("Key D Pressed")
            execute_action("Right")
            key_pressed["Right"] = True
    except AttributeError as e:
        print(f"Error: {e}")

def on_release(key):
    try:
        # Only process WASD in developer mode
        if not developer_mode:
            return

        key_char = getattr(key, 'char', None)
        if key_char == 'w':
            key_pressed["Up"] = False
            print("Released: W")
        elif key_char == 's':
            key_pressed["Down"] = False
            print("Released: S")
        elif key_char == 'a':
            key_pressed["Left"] = False
            print("Released: A")
        elif key_char == 'd':
            key_pressed["Right"] = False
            print("Released: D")
        else:
            #print(f"Released: {key}") # For debugging, print the actual key value
            pass
    except AttributeError as e:
        print(f"Error: {e}")

# Add new function to toggle modes
def toggle_developer_mode():
    global developer_mode
    developer_mode = not developer_mode
    print(f"Developer mode: {'ON' if developer_mode else 'OFF'}")

# At the start of your main script, after imports
print("Middle Click starting...")
print("Developer mode:", "OFF" if not developer_mode else "ON")
print("Listening for input...")

def check_accessibility_permissions():
    try:
        # Attempt to perform a simple action that requires accessibility permissions
        subprocess.run(['osascript', '-e', 'tell application "System Events" to key code 0'], check=True)
        print("Accessibility permissions are granted.")
    except subprocess.CalledProcessError:
        print("Accessibility permissions are not granted. Please enable them in System Preferences.")
        return False
    return True

def check_input_monitoring_permissions():
    try:
        # Attempt to perform a simple action that requires input monitoring permissions
        subprocess.run(['osascript', '-e', 'tell application "System Events" to key code 0'], check=True)
        print("Input monitoring permissions are granted.")
    except subprocess.CalledProcessError:
        print("Input monitoring permissions are not granted. Please enable them in System Preferences.")
        return False
    return True

# Also add a startup message in your main execution block
if __name__ == "__main__":
    if not check_accessibility_permissions():
        print("Please grant  accessibility permissions in System Preferences and restart the application.")
        exit(1)
    elif not check_input_monitoring_permissions():
        print("Please grant input monitoring permissions in System Preferences and restart the application.")
        exit(1)
    print("Initializing Middle Click...")
    try:
        # Your existing listener setup codea
        with mouse.Listener(on_click=on_click, on_move=on_move) as mouse_listener, \
             keyboard.Listener(on_press=on_press, on_release=on_release) as keyboard_listener:
            print("Middle Click is now running!")
            print("Press Tab to toggle developer mode")
            mouse_listener.join()
            keyboard_listener.join()
    except Exception as e:
        print(f"Error: {e}")
        raise