#-*-coding:utf-8-*-
import time,requests,sys,re,os
from lxml import etree
reload(sys)
sys.setdefaultencoding("utf-8")
hea = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'}
requests.adapters.DEFAULT_RETRIES = 5
proxies = {'http': 'http://127.0.0.1:1080',
                       'https': 'http://127.0.0.1:1080'}

google='https://www.google.com'  #s?wd=就&rn=50
searchtext="inurl:php?id= site:org"
firstpage=google+"/search?q="+searchtext+'&num=100'
nextpage=""
def ScrawTarget(n):
    save_path = os.path.abspath("./GoogleUrl")  #建立文件夹
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    savefilename ="url.txt"
    Save_Path = os.path.join(save_path, savefilename)
    for i in range(n):
        i = i + 1
        openfilename = str(i) + ".html"
        Open_Path = os.path.join(save_path, openfilename)
        f = open(Open_Path, 'r')
        html=f.read()
        f.close()
        ScrawOnePage(html,Save_Path)
    print ("scraw success!")

def ScrawOnePage(html,save_path):  #爬1页里的100条结果
    selector=etree.HTML(html)

    f=open(save_path,'a+')
    for i in range(100):
        i=i+1
        xpathtext='//*[@id="rso"]/div/div['+str(i)+']/div/h3/a/@href'       #//*[@id="rso"]/div/div[1]/div/h3/a
        TrueUrl=selector.xpath(xpathtext)[0]
        f.write(TrueUrl+'\n')
    f.close()

ScrawTarget(8)