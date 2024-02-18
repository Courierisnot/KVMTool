import subprocess
import time
import re

# TODO make shared drive

class imageOperations():


    def __init__(self,operation=''):

        self.operation = operation


        self.path = '/usr/share/KVMTool/'
        self.imagePath = self.path + 'tmpimages/'

        self.stored_stdout = None

        self.screenshot = f"curl --unix-socket /run/kvmd/ustreamer.sock http://localhost/snapshot"
        self.ocr        = f"tesseract -c tessedit_do_invert=0 - {self.imagePath}screen"

        self.thread()


    def thread(self):

        if self.operation == "serial":
            self.getSerial()
        if self.operation == "ocr":
            out = processOperations(self.screenshot).runProcessThread()
            processOperations(self.ocr).runProcessThread(pipe=out)


    def pixelCoordinates(self,height=100,width=100,xstart=0,ystart=0):
        return f'convert - -crop {height}x{width}+{xstart}+{ystart} +repage - '

        
    def tesseract(self,output='-'):

        ocr = f"tesseract -c tessedit_do_invert=0 - {output} "
        return ocr
        
        

    def getSerial(self):
        print("Retrieving S/N...")
        outfile = f'{self.imagePath}serialdata'
        cmd1 = self.takeScreenshot()
        cmd2 = self.pixelCoordinates(1280,30)
        cmd3 = self.tesseract(output=outfile)

        keyboardOperations('left-alt v',verbose=True).translate()

        while True:
            time.sleep(0.5)
            processOperations([[cmd1,cmd2,cmd3]]).runThread()
            with open(f"{outfile}.txt",'r') as f:
                data = f.read()
                if "Google" in data:

                    data = data.strip()
                    data = re.split('[()]{1}',data)

                    chromeVersion = data[0]
                    chromePlatform = data[1]
                    chromeSerial = data[2]
                    break
                else:
                    keyboardOperations('left-alt v',verbose=True).translate()
                    time.sleep(0.25)
                    continue
        return chromeVersion, chromePlatform ,chromeSerial


        

    

    #Keeping function in case command can be expanded on
    def takeScreenshot(self):

        snap = f"curl --unix-socket /run/kvmd/ustreamer.sock http://localhost/snapshot "
        return snap

        



    def testfunc(self):

        output = processOperations(self.screenshot).runProcessThread()
        output = processOperations(self.ocr).runProcessThread(output)
        return True



class keyboardOperations():

    def __init__(self,cmd_str,verbose=False,enter=False):
        self.enter = enter
        self.verbose = verbose
        self.cmd_str = cmd_str


    def kbcmd(self,keystroke):

        keystroke_cmd = f"echo '{keystroke}' | ./hid_gadget_test /dev/hidg0 keyboard"

        processOperations([[keystroke_cmd]]).runThread()



    def translate(self):
    
        special_chars = [
            [" ","space"],
            ['-','minus'],
            ['=','equals'],
            ['[','lbracket'],
            [']','rbracket'],
            [';','semicolon'],
            ['/','slash'],
            ['\\', 'backslash'],
            ['\'', 'quote'],
            ['#', "hash"],
            ['.', 'period'],
            [',', 'comma'],
            ['"', 'left-shift quote'],
            ['?', 'lef-shift slash']
            ]

        if self.verbose:
            self.kbcmd(self.cmd_str)
        else:

            for char in self.cmd_str:
                for list in special_chars:
                    if char in list[0]:
                        char = list[list.index(char) + 1]
                if char.isupper():
                    char = "left-shift " + char.lower()
                self.kbcmd(char)

            if self.enter:
                self.kbcmd('enter')
        

class processOperations():

    def __init__(self,cmdlist=[]):

        self.process = ''
        self.cmdlist = cmdlist
        
            
    def runThread(self):

    
        for list in self.cmdlist: 
            out = None
            for item in list:
                if out == None:
                    out = self.runProcessThread(item)
                else:
                    out = self.runProcessThread(process=item, pipe=out)
                    
                if not out:
                    break

            try:
                return out
            except AttributeError:
                print("Attribute error\n")

            
            


    def runProcessThread(self,process,pipe=''):


        with subprocess.Popen(process,
        shell=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE) as proc:
            try:
                out, err = proc.communicate(input=pipe,timeout=15)
                if proc.returncode == 0:
                    # print("Process Success")
                    return out
                else:
                    print(err.decode('utf-8'))
                    return 
            except subprocess.TimeoutExpired:
                proc.kill()
                print("Process Timed out")
                return False
            except Exception as error:
                print(f"Error:{str(error)}")

    # def __init__(self,process):

    #     self.process = process


    # def runProcessThread(self,pipe=None):

    #     with subprocess.Popen(self.process,
    #     shell=True,
    #     stdin=subprocess.PIPE,
    #     stdout=subprocess.PIPE,
    #     stderr=subprocess.PIPE) as proc:
    #         try:
    #             out, err = proc.communicate(input=pipe,timeout=15)
    #             if proc.returncode == 0:
    #                 # print("Process Success")
    #                 return out
    #             else:
    #                 print(err.decode('utf-8'))
    #                 return False
    #         except subprocess.TimeoutExpired:
    #             proc.kill()
    #             print("Process Timed out")
    #             return False
    #         except Exception as error:
    #             print(f"Error:{str(error)}")




if __name__ == "__main__":
    pass