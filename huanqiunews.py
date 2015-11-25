#-*-coding:utf-8-*-
import time,requests,sys,re,os
from lxml import etree
reload(sys)
sys.setdefaultencoding("utf-8")
hea = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'}

hqurl='http://oversea.huanqiu.com/article/'

LastRecord=""
RecordFlag=False

def scraw(hqurl):  #爬30页
    global LastRecord
    LastRecord=GetRecord()
    for i in range (30):
        if i==0:
            url=hqurl+'index.html'
        else:
            url=hqurl+str(i+1)+'.html'
        ScrawOnePage(url)

def ScrawOnePage(url):  #爬1页里的60条新闻
    global RecordFlag,LastRecord
    html=requests.get(url,headers = hea)
    html.encoding = 'utf-8'
    selector=etree.HTML(html.text)
    f=open('huanqiunews.txt','a+')
    for i in range(60):
        title=selector.xpath('/html/body/div[3]/div/div[3]/ul/li['+str(i+1)+']/h3/a/text()')[0]
        newsurl=selector.xpath('/html/body/div[3]/div/div[3]/ul/li['+str(i+1)+']/h3/a/@href')[0]
        try:
            abstract=selector.xpath('/html/body/div[3]/div/div[3]/ul/li['+str(i+1)+']/h5/text()')[0]
        except :
            abstract=''
        try:
            img=selector.xpath('/html/body/div[3]/div/div[3]/ul/li['+str(i+1)+']/a/img/@src')[0]
        except :
            img=''
        time=selector.xpath('/html/body/div[3]/div/div[3]/ul/li['+str(i+1)+']/h6/text()')[0]
        if time == LastRecord:
            print "scraw complete !"
            os._exit(0)
        if RecordFlag==False: #首次爬的内容写入日志
            SetRecord(time)
            RecordFlag=True
        media,author,text,newsurl2=ScrawOneNews(newsurl)
        if media=='环球网' or media=="环球时报":
            realurl=newsurl
        else:
            realurl=newsurl2
        content=time.replace('\n','')+' '+title.replace('\n','')+' '\
                +media.replace('\n','')+' '+author.replace('\n','')+' '+abstract.replace('\n','')+' '+realurl.replace('\n','')+' '\
                +img.replace('\n','')+'\n'+text+'\n'
        print content
        f.write(content)
    f.close()

def ScrawOneNews(NewsUrl):   #获取每条新闻的内容
    html=requests.get(NewsUrl,headers = hea)
    html.encoding = 'utf-8'
    selector=etree.HTML(html.text)
    try:
        media=selector.xpath('//*[@id="source_baidu"]/a/text()')[0]
    except:
        media=''
    try:
        url=selector.xpath('//*[@id="source_baidu"]/a/@href')[0]
    except:
        url=''
    try:
        author=selector.xpath('//*[@id="author_baidu"]/text()')[0].replace(' ','').replace('\r\n','')
    except:
        author=''
    context=selector.xpath('//*[@id="text"]')[0]
    context=context.xpath('string(.)')
    context=context.replace('BAIDU_CLB_fillSlot("1028976");','').replace('\r\n','\n').replace(' ','').replace('\n\n\n\n\n','').replace('\n\n','').replace('\n\n\n\n','')[1:]#.replace('\n','')
    try:
        text=re.search('.(.*?)上一页'.decode('utf-8'),context,re.S).group(1)
    except:
        text=context
    try:
        text=re.search('.(.*?)相关新闻'.decode('utf-8'),text,re.S).group(1)
    except:
        text=text
    i=2
    nexturl=[]
    while 1 :
        nextxpath='//*[@id="pages"]/a['+str(i)+']/@href'
        try :
            nextpage=selector.xpath(nextxpath)[0]
            nexturl.append(nextpage)
        except:
            break
        i+=1
    nexturl= nexturl[:-1]
    for next in nexturl:
        html=requests.get(next,headers = hea)
        html.encoding = 'utf-8'
        selector2=etree.HTML(html.text)
        context2=selector2.xpath('//*[@id="text"]')[0]
        context2=context2.xpath('string(.)')
        context2=context2.replace('BAIDU_CLB_fillSlot("1028976");','').replace('\r\n','\n').replace(' ','').replace('\n\n\n\n\n','').replace('\n\n','').replace('\n\n\n\n','')[1:]#.replace('\n','')
        try:
            context2=re.search('(.*?)上一页'.decode('utf-8'),context2,re.S).group(1)
        except:
            context2=context2
        try:
            context2=re.search('(.*?)相关新闻'.decode('utf-8'),context2,re.S).group(1)
        except:
            context2=context2
        text+=context2
    return media,author,text,url

def GetRecord():
    f=open("huanqiunewslog.txt","r")
    Lastrecord=f.read()
    f.close()
    print Lastrecord
    return Lastrecord

def SetRecord(record):
    f=open("huanqiunewslog.txt","w")
    f.write(record)
    print record
    f.close()

scraw(hqurl)