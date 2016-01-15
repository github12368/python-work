#-*-coding:utf-8-*-
import time,sys,os,subprocess
reload(sys)
sys.setdefaultencoding("utf-8")
TaskDIR=""
# ShadowsocksDIR=ShadowsocksDIR+'\\'
Task1='TranslateHbaseMessage.exe'
Task1Path=TaskDIR+Task1
Task2='TranslateHbaseUser.exe'
Task2Path=TaskDIR+Task2
while 1:
    subprocess.Popen(Task1Path)
    # subprocess.Popen(Task2Path)
    time.sleep(300)
    KillTask1Command='taskkill /F /IM '+Task1
    # KillTask2Command='taskkill /F /IM '+Task2
    os.system(KillTask1Command)
    # os.system(KillTask2Command)