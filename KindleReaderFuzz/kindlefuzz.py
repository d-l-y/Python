import time
import win32com.client
import SendKeys
import os
import re
import sys

'''
Fuzzer created for fuzzing Kindle Reader for PC. Uses Windbg.
Create a bunch of test cases using whatever method you like using a number naming scheme (i.e 1.azw,2.azw etc.)
opens each file if it does not crash on open it selects that file in kindle reader to try and read it to see if crash occurs.
If crash it will create crash report file.
Not very fast but did find numerous crashes.
@IamDly
Usage: python kindle_reader_fuzz.py <start of fuzz file range> <end of fuzz file range>
'''


def report(info):
    with open(".\log\crash.txt","a") as f:
        f.write(info)
        f.close()

def isresponding():
    if "Kindle.exe" in os.popen("tasklist /FI \"IMAGENAME eq Kindle.exe\" /FI \"STATUS eq running\"").read():
        return True
    else:
        return False

def getPid(task):
    proc = os.popen("tasklist /FI \"IMAGENAME eq "+task+"\" /FI \"STATUS eq running\"").read()
    pid = re.findall(r"\D(\d{3,4})\D", proc)
    return pid[0]

    
os.system("del \"C:\\Users\\IEUser\\Documents\\My Kindle Content\\*\"")
num = range(sys.argv[1],sys.argv[2])
dbgpid = getPid('windbg.exe')

for i in num:
    
    os.system("copy \"C:\\Users\\IEUser\\Desktop\\kindlefuzz\\"+str(i)+".azw\" \"C:\\Users\\IEUser\\Documents\\My Kindle Content\" >nul 2>&1")
    report("[+}current fuzz file "+str(i)+" "+time.asctime( time.localtime(time.time()) )+"\n")
    
    shell = win32com.client.Dispatch('WScript.Shell')
    shell.AppActivate(dbgpid) #activate windbg window
    time.sleep(.3)
    shell.SendKeys("{F5}", 0)
    time.sleep(20)
    shell.SendKeys("{F5}", 0)
    time.sleep(.5)
        
    if isresponding() == True:
        shell.AppActivate(getPid('Kindle.exe')) #activate kindle window
        time.sleep(.5)
        shell.SendKeys("^{ }", 0)
        shell.SendKeys("^{o}", 0)
        time.sleep(10)
        
    if isresponding() == False:
        shell.AppActivate(dbgpid)
        shell.SendKeys("{.}{l}{o}{g}{o}{p}{e}{n}{ }{/}{t}{ }{c}{:}{\}{l}{o}{g}{\}{k}{i}{n}{d}{l}{e}{ENTER}", 0)
        time.sleep(.5)
        shell.AppActivate(dbgpid)
        shell.SendKeys("{!}{a}{n}{a}{l}{y}{z}{e}{ }{-}{v}{ENTER}", 0)
        time.sleep(.5)
        shell.AppActivate(dbgpid)
        shell.SendKeys("{r}{ENTER}")
        time.sleep(.5)
        shell.SendKeys("{.}{l}{o}{g}{c}{l}{o}{s}{e}{ENTER}")
        time.sleep(.5)
        report("[!]crash with "+str(i)+" "+time.asctime( time.localtime(time.time()) )+"\n")
        os.system("copy \"C:\\Users\\IEUser\\Desktop\\kindlefuzz\\"+str(i)+".azw\" \"C:\\Users\\IEUser\\Desktop\\crash\" >nul 2>&1")
        
     
    shell.AppActivate(dbgpid)   #activate windbg window
    time.sleep(.3)
    shell.SendKeys("^{BREAK}")
    time.sleep(.3)
    shell.AppActivate(dbgpid)
    time.sleep(.3)
    shell.SendKeys("^+{F5}")   

    os.system("del \"C:\\Users\\IEUser\\Documents\\My Kindle Content\\"+str(i)+".azw\"")
time.sleep(1)
