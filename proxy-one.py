#-*-coding:utf-8-*-
import win32api,win32con,win32gui,time,requests,sys
from ctypes import *
from lxml import etree
reload(sys)
sys.setdefaultencoding("utf-8")
hea = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'
,"Connection": "close"}
requests.adapters.DEFAULT_RETRIES = 5
proxies = {'http': 'http://127.0.0.1:1080',
                       'https': 'http://127.0.0.1:1080'}
fa=win32api.GetSystemMetrics(0)/2
fb=win32api.GetSystemMetrics(1)/2

def Ping():
    try:
        html=requests.get("https://www.google.com", proxies=proxies,headers = hea)
    except:
        return 0
    else:
        return 1

def GetServer(i):
    #try:
        html=requests.get('http://www.ishadowsocks.com',headers = hea)
        html.encoding = 'utf-8'
        selector=etree.HTML(html.text)
        ip1=repr(selector.xpath('//*[@id="free"]/div/div[2]/div[1]/h4[1]/text()')).split(":")[1][:-2]
        ip2=repr(selector.xpath('//*[@id="free"]/div/div[2]/div[2]/h4[1]/text()')).split(":")[1][:-2]
        ip3=repr(selector.xpath('//*[@id="free"]/div/div[2]/div[3]/h4[1]/text()')).split(":")[1][:-2]
        port1=repr(selector.xpath('//*[@id="free"]/div/div[2]/div[1]/h4[2]/text()')).split(":")[1][:-2]
        port2=repr(selector.xpath('//*[@id="free"]/div/div[2]/div[2]/h4[2]/text()')).split(":")[1][:-2]
        port3=repr(selector.xpath('//*[@id="free"]/div/div[2]/div[3]/h4[2]/text()')).split(":")[1][:-2]
        password1=repr(selector.xpath('//*[@id="free"]/div/div[2]/div[1]/h4[3]/text()')).split(":")[1][:-2]
        password2=repr(selector.xpath('//*[@id="free"]/div/div[2]/div[2]/h4[3]/text()')).split(":")[1][:-2]
        password3=repr(selector.xpath('//*[@id="free"]/div/div[2]/div[3]/h4[3]/text()')).split(":")[1][:-2]
        ip=[ip1,ip2,ip3]
        port=[port1,port2,port3]
        password=[password1,password2,password3]
    #except:
        #print "错误：ishadowsocks无法访问"
    #else:
        return ip[i-1],port[i-1],password[i-1]

def GetPos():
    ht=win32gui.FindWindow("Shell_TrayWnd",None)   #获取托盘句柄
    ht=win32gui.FindWindowEx(ht,None,'TrayNotifyWnd',None)
    ht=win32gui.FindWindowEx(ht,None,'SysPager',None)
    ht=win32gui.FindWindowEx(ht,None,'ToolbarWindow32',None)
    size=win32gui.GetWindowRect(ht)
    y=(size[1]+size[3])/2  #shadowsocks坐标y
    dify=int((size[3]-size[1])/2/1.58)
    x=size[2]-dify
    return x,y


def mouse_dclick(x=None,y=None):   #模拟鼠标双击
    if not x is None and not y is None:
        windll.user32.SetCursorPos(x, y)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    windll.user32.SetCursorPos(fa, fb)


def GetEdit():
    hn=win32gui.FindWindow(None,'编辑服务器')    #主窗口
    ClassName=win32gui.GetClassName(hn)
    last=ClassName[-15:]
    ClassButton='WindowsForms10.BUTTON.app.0.'+last
    ClassEdit='WindowsForms10.EDIT.app.0.'+last
    win32gui.ShowWindow(hn,win32con.SW_SHOWNORMAL)    #正常显示这个窗口
    hn1=win32gui.FindWindowEx(hn,None,ClassName,None) #第一层
    hn2=win32gui.FindWindowEx(hn1,None,ClassName,None)#第二层第一个

    for i in range(1,4):
        hn2=win32gui.FindWindowEx(hn1,hn2,ClassName,None)
        if i==2: #确认按钮
            confirmFather=hn2

    confirmBro=win32gui.FindWindowEx(confirmFather,0,ClassButton,None)#到了服务器层
    confirm=win32gui.FindWindowEx(confirmFather,confirmBro,ClassButton,None)
    hn3=win32gui.FindWindowEx(hn2,None,ClassName,None)#第三层


    edit=win32gui.FindWindowEx(hn3,None,ClassEdit,None)#第四层
    IpEdit=win32gui.FindWindowEx(hn3,edit,ClassEdit,None)
    PortEdit=win32gui.FindWindowEx(hn3,IpEdit,ClassEdit,None)
    PassWordEdit=win32gui.FindWindowEx(hn3,PortEdit,ClassEdit,None)  #找到密码层
    return IpEdit,PortEdit,PassWordEdit,confirm

def SetServer(Edit,Param):
    win32gui.SendMessage(Edit[0],win32con.WM_SETTEXT,None,Param[0])
    win32gui.SendMessage(Edit[1],win32con.WM_SETTEXT,None,Param[1])
    win32gui.SendMessage(Edit[2],win32con.WM_SETTEXT,None,Param[2]) #发密码
    win32gui.PostMessage(Edit[3], win32con.WM_LBUTTONDOWN, 0, 0)
    win32gui.PostMessage(Edit[3], win32con.WM_LBUTTONUP, 0, 0)


def RunServer(i):
     pos=GetPos()
     time.sleep(5)
     try:
        mouse_dclick(pos[0],pos[1])
        time.sleep(0.1)
        Param=GetServer(i)
        Edit=GetEdit()
        SetServer(Edit,Param)
        time.sleep(2)
     except:
        print "parm setting error!"
        return 0
     else:
        return 1

def StartServer():
    while 1:
        if Ping()==1:
            print "Start Server!"
            break
        else:
            while 1:
                if RunServer(1)==1:
                    print "Setting Ok!"
                    break
    return 1
StartServer()
