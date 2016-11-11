#-*-coding:utf-8-*-
import time,requests,sys,os,subprocess,re
reload(sys)
sys.setdefaultencoding("utf-8")
ShadowsocksDIR=""
# ShadowsocksDIR=ShadowsocksDIR+'\\'
ShadowsocksPath=ShadowsocksDIR+"shadowsocks.exe"
ShadowsocksConfPath=ShadowsocksDIR+"gui-config.json"
hea = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'}
requests.adapters.DEFAULT_RETRIES = 5
proxies = {'http': 'http://127.0.0.1:1080',
                       'https': 'http://127.0.0.1:1080'}
#subprocess.Popen(ShadowsocksPath)
#os.system('taskkill /F /IM shadowsocks.exe')
def Ping():
    try:
        html=requests.get("https://www.google.com", proxies=proxies,headers = hea)
    except:
        return 0
    else:
        return 1

def GetServer():
    try:
        html=requests.get('http://www.feixunwangluo.com/page/testss.html',headers = hea)
        # html = requests.get('http://ss.yuvpn.com/page/testss.html', headers=hea)
        html.encoding = 'utf-8'
        html=html.text
        node=re.findall('<b>(.*?)</b>',html)
        node1=node[0][5:7]
        node2=node[1][5:7]
        ip=re.findall('<span>(.*?)</span>',html)
        ip1=repr(ip[7])[2:-1]
        ip2=repr(ip[9])[2:-1]
        ip3=''
        port=re.findall('端口：(.*?)<'.decode('utf-8'),html,re.S)
        port1=repr(port[0])[2:-1]
        port2=repr(port[1])[2:-1]
        port3=''
        password=re.findall('密码：(.*?)<'.decode('utf-8'),html,re.S)
        password1=repr(password[0])[2:-1]
        password2=repr(password[1])[2:-1]
        password3=''
        codetype=re.findall('加密方式：<span>(.*?)</span>'.decode('utf-8'),html,re.S)
        codetype1=repr(codetype[0])[2:-1]
        codetype2=repr(codetype[1])[2:-1]
        codetype3=''
        ip=[ip1,ip2,ip3]
        port=[port1,port2,port3]
        password=[password1,password2,password3]
        codetype=[codetype1,codetype2,codetype3]
    except:
        print "erro:shadowsocks website can't acess"
    else:
        return ip[0],port[0],password[0],codetype[0]

def SetServer(Param):
    time.sleep(2)
    f=open(ShadowsocksConfPath,'wb')
    ServerSting='"'+Param[0]+'"'
    Server_portSting='"'+Param[1]+'"'
    PasswordSting='"'+Param[2]+'"'
    MethodSting='"'+Param[3]+'"'
    string ='''{
"configs" : [
{
"server" :'''+ServerSting+','+'''
"server_port" :'''+Server_portSting+','+'''
"password" :'''+PasswordSting+','+'''
"method" :'''+MethodSting+','+'''
"remarks" : ""}

],
"strategy" : null,
"index" : 0,
"global" : false,
"enabled" : true,
"shareOverLan" : true,
"isDefault" : false,
"localPort" : 1080,
"pacUrl" : null,
"useOnlinePac" : false,
"availabilityStatistics" : false}
'''
    f.write(string)
    f.close()


def RunServer():
     try:
        Param=GetServer()
        SetServer(Param)
        subprocess.Popen(ShadowsocksPath)
     except:
        return 0
     else:
        return 1

RunServer()
time.sleep(3)


state=0
if Ping()==1:
    print "OK,Start Server!"
    state=1
i=1
while 1:
    if Ping()==0:
        if state==1:
            state=0
            print "error:connect again"
            os.system('taskkill /F /IM shadowsocks.exe')
            while 1:
                if RunServer()==1:
                    break
                else:
                    time.sleep(3)
        else:
            print "error:switch server"

            while 1:
                if RunServer()==1:
                    break
                else:
                    time.sleep(3)
            i+=1
    else:
        if state==0:
            print "OK,Start Server!"
            state=1
    time.sleep(10)


