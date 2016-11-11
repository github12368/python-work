#-*-coding:utf-8-*-
import time,requests,sys,re,os
from lxml import etree
reload(sys)
sys.setdefaultencoding("utf-8")
hea = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'}

baidu='https://www.baidu.com'  #s?wd=就&rn=50
searchtext="inurl:php?id site:gov.cn"
firstpage=baidu+"/s?wd="+searchtext+'&rn=50'
nextpage=""
def ScrawTarget():
    i=0
    save_path = os.path.abspath("./BaiduUrl")  #建立文件夹
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    f=open('target.txt','r')
    Targets= f.readlines()  # 读取全部内容
    for Target in Targets:
        i = i + 1
        Target=Target.replace('\n','')
        Taegeturl=baidu+"/s?wd="+Target+'&rn=50'
        filename=str(i)+'.txt'
        Save_Path= os.path.join(save_path, filename)

        scraw(Taegeturl, Save_Path)


def scraw(Taegeturl,save_path):  #爬15页
    global nextpage
    for i in range (15):
        if i==0:
            ScrawOnePage(Taegeturl,i,save_path)
        else:
            ScrawOnePage(nextpage,i,save_path)
    print "scraw success!"

def ScrawOnePage(url,j,save_path):  #爬1页里的50条结果
    global nextpage
    html=requests.get(url,headers = hea)
    html.encoding = 'utf-8'
    selector=etree.HTML(html.text)

    f=open(save_path,'a+')
    for i in range(50):
        i=j*50+i+1
        xpathtext='//*[@id="'+str(i)+'"]/h3/a/@href'
        serachurl=selector.xpath(xpathtext)[0]

        tmpPage = requests.get(serachurl, allow_redirects=False)  #百度链接转真实链接
        if tmpPage.status_code == 200:
            TrueUrl = re.search(r'URL=\'(.*?)\'', tmpPage.text.encode('utf-8'), re.S).group(1)
        elif tmpPage.status_code == 302:
            TrueUrl = tmpPage.headers.get('location')
        else:
            TrueUrl = ''

        f.write(TrueUrl+'\n')
    if j==0:
        nextpage=baidu+selector.xpath('//*[@id="page"]/a[10]/@href')[0]
    else:
        nextpage = baidu + selector.xpath('//*[@id="page"]/a[11]/@href')[0]
    print nextpage
    f.close()
ScrawTarget()

# def GetTrueUrl(BaiduUrl):
#     tmpPage = requests.get(BaiduUrl, allow_redirects=False)
#     if tmpPage.status_code == 200:
#         TrueUrl = re.search(r'URL=\'(.*?)\'', tmpPage.text.encode('utf-8'), re.S).group(1)
#     elif tmpPage.status_code == 302:
#         TrueUrl = tmpPage.headers.get('location')
#     else:
#         TrueUrl=''
#     return TrueUrl

# scraw(firstpage)
# def GetRecord():
#     f=open("huanqiunewslog.txt","r")
#     Lastrecord=f.read()
#     f.close()
#     print Lastrecord
#     return Lastrecord
#
# def SetRecord(record):
#     f=open("huanqiunewslog.txt","w")
#     f.write(record)
#     print record
#     f.close()

# scraw()