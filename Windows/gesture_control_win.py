from pynput import mouse, keyboard
import time
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

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
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    current_volume = volume.GetMasterVolumeLevelScalar()
    volume.SetMasterVolumeLevelScalar(min(current_volume + 0.1, 1.0), None)

def volume_down():
    print("Volume Down Commanded")
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    current_volume = volume.GetMasterVolumeLevelScalar()
    volume.SetMasterVolumeLevelScalar(max(current_volume - 0.1, 0.0), None)

def swipe_left():
    print("Three Finger Swipe Left Commanded")
    # Windows implementation can be added here
    # For example, you could simulate Windows + Ctrl + Left Arrow
    print("Swipe Left - Windows Desktop Switch")

def swipe_right():
    print("Three Finger Swipe Right Commanded")
    # Windows implementation can be added here
    # For example, you could simulate Windows + Ctrl + Right Arrow
    print("Swipe Right - Windows Desktop Switch")

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
    if middle_button_pressed and not gesture_executed:
        if start_position is None:
            start_position = (x, y)
        else:
            dx = x - start_position[0]
            dy = y - start_position[1]
            distance_threshold = 50  # Minimum distance to recognize a gesture

            if abs(dx) > distance_threshold or abs(dy) > distance_threshold:
                if abs(dx) > abs(dy):
                    if dx > 0:
                        gesture = "Right"
                    else:
                        gesture = "Left"
                else:
                    if dy > 0:
                        gesture = "Down"
                    else:
                        gesture = "Up"
                
                # Execute the action for the detected gesture
                execute_action(gesture)
                gesture_executed = True  # Mark gesture as executed
                
                # Reset start position to avoid repeated triggers
                start_position = (x, y)

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

# Set up the mouse listener
mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click)
mouse_listener.start()

# Set up the keyboard listener
with keyboard.Listener(on_press=on_press, on_release=on_release) as keyboard_listener:
    keyboard_listener.join()

# Stop the mouse listener when the keyboard listener stops
mouse_listener.stop()
