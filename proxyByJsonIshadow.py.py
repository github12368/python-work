#-*-coding:utf-8-*-
import time,requests,sys,os,subprocess
from lxml import etree
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

def GetServer(i):
    try:
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
        codetype1=repr(selector.xpath('//*[@id="free"]/div/div[2]/div[1]/h4[4]/text()')).split(":")[1][:-2]
        codetype2=repr(selector.xpath('//*[@id="free"]/div/div[2]/div[2]/h4[4]/text()')).split(":")[1][:-2]
        codetype3=repr(selector.xpath('//*[@id="free"]/div/div[2]/div[3]/h4[4]/text()')).split(":")[1][:-2]
        ip=[ip1,ip2,ip3]
        port=[port1,port2,port3]
        password=[password1,password2,password3]
        codetype=[codetype1,codetype2,codetype3]
    except:
        print "erro:shadowsocks website can't acess"
    else:
        return ip[i-1],port[i-1],password[i-1],codetype[i-1]

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


def RunServer(i):
     try:
        Param=GetServer(i)
        SetServer(Param)
        subprocess.Popen(ShadowsocksPath)
     except:
        return 0
     else:
        return 1
RunServer(1)
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
                if RunServer(1)==1:
                    break
                else:
                    time.sleep(3)
        else:
            print "error:switch server"
            os.system('taskkill /F /IM shadowsocks.exe')
            while 1:
                if RunServer(i%3+1)==1:
                    break
                else:
                    time.sleep(3)
            i+=1
    else:
        if state==0:
            print "OK,Start Server!"
            state=1
    time.sleep(10)


