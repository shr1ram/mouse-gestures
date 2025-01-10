from pynput import mouse
import time

# Variables to track the state
middle_button_pressed = False
start_position = None
last_gesture_time = 0
gesture_cooldown = 0.5  # Cooldown period in seconds
gesture_executed = False  # Flag to track if a gesture has been executed

# Define actions for each gesture
gesture_actions = {
    "Up": lambda: print("Action: Volume Up"),
    "Down": lambda: print("Action: Volume Down"),
    "Left": lambda: print("Action: Previous Track"),
    "Right": lambda: print("Action: Next Track")
}

def on_move(x, y):
    global middle_button_pressed, start_position, last_gesture_time, gesture_executed
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
                
                # Check if enough time has passed since the last gesture
                current_time = time.time()
                if current_time - last_gesture_time > gesture_cooldown:
                    # Execute the action for the detected gesture
                    if gesture in gesture_actions:
                        gesture_actions[gesture]()
                        gesture_executed = True  # Mark gesture as executed
                    last_gesture_time = current_time  # Update the last gesture time
                
                # Reset start position to avoid repeated triggers
                start_position = (x, y)

def on_click(x, y, button, pressed):
    global middle_button_pressed, start_position, gesture_executed
    if button == mouse.Button.middle:
        middle_button_pressed = pressed
        if not pressed:
            start_position = None  # Reset when the button is released
            gesture_executed = False  # Reset gesture executed flag

# Set up the listener
with mouse.Listener(on_move=on_move, on_click=on_click) as listener:
    listener.join() 