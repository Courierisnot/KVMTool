import subprocess
import threading
import time



class deviceScan():

    def __init__(self,address):

        self.address = address
        self.updateAddress()

    
    def updateAddress(self):
        out = self.checkForNewAddress()
        if not out:
            pass
        else:
            self.address = out
        

    def checkdmesg(self):
        with subprocess.Popen("dmesg -l info | tail -10 | grep -E \"new address\" | tail -1",shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
            result, errors = process.communicate()
            if errors == b'':
                return result.decode('utf-8')
            else:
                print("err" + result.decode('utf-8'))
                print("Returncode:" + str(process.returncode))
                return False
        

    def checkForNewAddress(self):

        currentAddress = self.address

        newAddress = self.checkdmesg()
        if newAddress == None:
            return 0
        newAddress = int(newAddress[newAddress.rfind(' ') + 1:])
        # Switched to != as new address is not always a larger #
        if newAddress != currentAddress:
                print(f"New Address detected\nOld Address:{currentAddress}\nNew Address:{newAddress}")
                currentAddress = newAddress
                return currentAddress
                
        time.sleep(0.25)
            
            


# if __name__ == "__main__":
#     deviceScan()
    
