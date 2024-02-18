import subprocess
import time
import threading
import re
from deviceScan import deviceScan
from deviceOperations import processOperations, keyboardOperations, imageOperations

# TODO Make into Class
#===============================================PATHS=============================================================

mainPath = "/usr/share/KVMTool/"
imagePath = f'{mainPath}/tmpimages/'

#==============================================COMMANDS============================================================

ocr = f"tesseract -c tessedit_do_invert=0 {imagePath}screen.jpg {imagePath}screen"
snap = f"curl --unix-socket /run/kvmd/ustreamer.sock http://localhost/snapshot -o {imagePath}screen.jpg"
crop = f"mogrify -crop 1920x30+0+0 +repage {imagePath}/screen.jpg"

cmd1 = "curl --unix-socket /run/kvmd/ustreamer.sock http://localhost/snapshot "
cmd2 = "convert - -crop 80x40+35+680 +repage - "
cmd3 = "tesseract -c tessedit_do_invert=0 - - --dpi 300 --psm 8 --oem 3"
cmd4 = "cat"

class main():

    def __init__(self):
        print("Starting script...")
        
        while True:
            if not self.screenstate():
                break
            uid = input('Please Enter UID:')
            f = imageOperations().getSerial()
            keyboardOperations("left-alt v",verbose=True).translate()
            serial = f[2]
            serial = serial.strip().lstrip("SN:")
            break
       
        print(f"\nVersion:{f[0]}\nPlatform:{f[1]}\nSerial:{serial}\nUID:{uid}\n")

        
    
    def screenstate(self):
        i = 2
        while True:
            out = processOperations([[cmd1, cmd2,cmd3,cmd4]]).runThread()
            if "shutdown" in out.decode('utf-8').strip().lower():
                print("Success")
                return True
            else:
                i += 1
                if i % 3 == 0:
                    keyboardOperations("left-ctrl f4",verbose=True).translate()
                continue
            


def probe():

    currentAddress = 0

    while True:
        newAddress = deviceScan(address=currentAddress).address
        if newAddress != currentAddress:
            currentAddress = newAddress
            print(newAddress)
            main().screenstate()
            print("Searching for new address...")
        time.sleep(1)
        continue

if __name__ == "__main__":
    t = threading.Thread(target=probe)
    t.start()
