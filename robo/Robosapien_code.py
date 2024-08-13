import socket
import robo

# Define constants for the messages and their corresponding codes
BUTTON_PRESS_11 = "BUTTON_PRESS:11"
BUTTON_STOP_FORWARD = "BUTTON_RELEASE:11"
BUTTON_PRESS_12 = "BUTTON_PRESS:12"
BUTTON_STOP_BACK = "BUTTON_RELEASE:12"
BUTTON_PRESS_14 = "BUTTON_PRESS:14"
BUTTON_STOP_LEFT = "BUTTON_RELEASE:14"
BUTTON_PRESS_13 = "BUTTON_PRESS:13"
BUTTON_STOP_RIGHT = "BUTTON_RELEASE:13"
TRIGGER_SPECIAL_ACTION = "TRIGGER_SPECIAL_ACTION"

WALK_FORWARD_CODE = 0x86
WALK_BACKWARD_CODE = 0x87
Turn_LEFT_CODE = 0xA0
Turn_right_CODE = 0xA8
STOP_CODE = 0x8E

# Initialize Robo and socket
rs = robo.Robo(21)
SERVER_IP = '0.0.0.0'
SERVER_PORT = 12345
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((SERVER_IP, SERVER_PORT))

print("Listening for messages...")

# Dictionary to map messages to actions
actions = {
    BUTTON_PRESS_11: WALK_FORWARD_CODE,
    BUTTON_PRESS_12: WALK_BACKWARD_CODE,
    BUTTON_PRESS_14: Turn_LEFT_CODE,
    BUTTON_PRESS_13: Turn_right_CODE,
    BUTTON_STOP_BACK: STOP_CODE,
    BUTTON_STOP_FORWARD: STOP_CODE,
    BUTTON_STOP_LEFT: STOP_CODE,
    BUTTON_STOP_RIGHT: STOP_CODE,
    TRIGGER_SPECIAL_ACTION: None,  # This could trigger a special function
}

def handle_special_trigger():
    print("Special trigger activated!")
    rs.send_code(WALK_FORWARD_CODE)  # Example action for the special trigger
    # Add more actions if needed

try:
    while True:
        data, addr = sock.recvfrom(1024)  # Buffer size is 1024 bytes
        message = data.decode()
        print(f"Received message: {message}")

        if message in actions:
            action_code = actions[message]

            if action_code is None:
                # Handle the special trigger
                handle_special_trigger()
            else:
                # Perform the action
                rs.send_code(action_code)
        else:
            print(f"Unrecognized message: {message}")

except KeyboardInterrupt:
    print("Exiting...")
finally:
    sock.close()
