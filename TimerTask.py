#-*-coding:utf-8-*-
import time,sys,os,subprocess
reload(sys)
sys.setdefaultencoding("utf-8")
TaskDIR=""
# ShadowsocksDIR=ShadowsocksDIR+'\\'
Task1='TranslateMysqlMessage.exe'
Task1Path=TaskDIR+Task1
Task2='TranslateMysqlTitleMessage.exe'
Task2Path=TaskDIR+Task2
Task3='TranslateMysqlUserprofile.exe'
Task3Path=TaskDIR+Task3
while 1:
    # subprocess.Popen(Task1Path)
    # subprocess.Popen(Task2Path)
    subprocess.Popen(Task3Path)
    time.sleep(600)
    # KillTask1Command='taskkill /F /IM '+Task1
    # KillTask2Command='taskkill /F /IM '+Task2
    KillTask3Command='taskkill /F /IM '+Task3
    # os.system(KillTask1Command)
    # os.system(KillTask2Command)
    os.system(KillTask3Command)