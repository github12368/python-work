# -*- coding: utf-8 -*-
import time,pymysql,urllib,urllib2
from lxml import etree
from langconv import *
reload(sys)
sys.setdefaultencoding('utf-8')
mysqldbip = "192.168.5.230"
mysqldbuser = "root"
mysqldbpsw = "ibm18911029778"
dbname = "showcase2016"
TableName='xjtu_topic'   #
ColuName='topic_name'
language='language'
TranslateColuname='translation'
LangDit={'gu': '\xe5\x8f\xa4\xe5\x90\x89\xe6\x8b\x89\xe7\x89\xb9\xe8\xaf\xad', 'zh-TW': '\xe4\xb8\xad\xe6\x96\x87(\xe7\xb9\x81\xe4\xbd\x93)', 'gd': '\xe8\x8b\x8f\xe6\xa0\xbc\xe5\x85\xb0\xe7\x9b\x96\xe5\xb0\x94\xe8\xaf\xad', 'ga': '\xe7\x88\xb1\xe5\xb0\x94\xe5\x85\xb0\xe8\xaf\xad', 'gl': '\xe5\x8a\xa0\xe5\x88\xa9\xe8\xa5\xbf\xe4\xba\x9a\xe8\xaf\xad', 'lb': '\xe5\x8d\xa2\xe6\xa3\xae\xe5\xa0\xa1\xe8\xaf\xad', 'la': '\xe6\x8b\x89\xe4\xb8\x81\xe8\xaf\xad', 'lo': '\xe8\x80\x81\xe6\x8c\x9d\xe8\xaf\xad', 'tr': '\xe5\x9c\x9f\xe8\x80\xb3\xe5\x85\xb6\xe8\xaf\xad', 'lv': '\xe6\x8b\x89\xe8\x84\xb1\xe7\xbb\xb4\xe4\xba\x9a\xe8\xaf\xad', 'lt': '\xe7\xab\x8b\xe9\x99\xb6\xe5\xae\x9b\xe8\xaf\xad', 'th': '\xe6\xb3\xb0\xe8\xaf\xad', 'tg': '\xe5\xa1\x94\xe5\x90\x89\xe5\x85\x8b\xe8\xaf\xad', 'te': '\xe6\xb3\xb0\xe5\x8d\xa2\xe5\x9b\xba\xe8\xaf\xad', 'ta': '\xe6\xb3\xb0\xe7\xb1\xb3\xe5\xb0\x94\xe8\xaf\xad', 'yi': '\xe6\x84\x8f\xe7\xac\xac\xe7\xbb\xaa\xe8\xaf\xad', 'ceb': '\xe5\xae\xbf\xe5\x8a\xa1\xe8\xaf\xad', 'yo': '\xe7\xba\xa6\xe9\xb2\x81\xe5\xb7\xb4\xe8\xaf\xad', 'de': '\xe5\xbe\xb7\xe8\xaf\xad', 'da': '\xe4\xb8\xb9\xe9\xba\xa6\xe8\xaf\xad', 'el': '\xe5\xb8\x8c\xe8\x85\x8a\xe8\xaf\xad', 'eo': '\xe4\xb8\x96\xe7\x95\x8c\xe8\xaf\xad', 'en': '\xe8\x8b\xb1\xe8\xaf\xad', 'eu': '\xe5\xb7\xb4\xe6\x96\xaf\xe5\x85\x8b\xe8\xaf\xad', 'zu': '\xe5\x8d\x97\xe9\x9d\x9e\xe7\xa5\x96\xe9\xb2\x81\xe8\xaf\xad', 'es': '\xe8\xa5\xbf\xe7\x8f\xad\xe7\x89\x99\xe8\xaf\xad', 'ru': '\xe4\xbf\x84\xe8\xaf\xad', 'zh-CN': '\xe4\xb8\xad\xe6\x96\x87(\xe7\xae\x80\xe4\xbd\x93)', 'ro': '\xe7\xbd\x97\xe9\xa9\xac\xe5\xb0\xbc\xe4\xba\x9a\xe8\xaf\xad', 'be': '\xe7\x99\xbd\xe4\xbf\x84\xe7\xbd\x97\xe6\x96\xaf\xe8\xaf\xad', 'bg': '\xe4\xbf\x9d\xe5\x8a\xa0\xe5\x88\xa9\xe4\xba\x9a\xe8\xaf\xad', 'uk': '\xe4\xb9\x8c\xe5\x85\x8b\xe5\x85\xb0\xe8\xaf\xad', 'bn': '\xe5\xad\x9f\xe5\x8a\xa0\xe6\x8b\x89\xe8\xaf\xad', 'jw': '\xe5\x8d\xb0\xe5\xb0\xbc\xe7\x88\xaa\xe5\x93\x87\xe8\xaf\xad', 'bs': '\xe6\xb3\xa2\xe6\x96\xaf\xe5\xb0\xbc\xe4\xba\x9a\xe8\xaf\xad', 'ja': '\xe6\x97\xa5\xe8\xaf\xad', 'xh': '\xe5\x8d\x97\xe9\x9d\x9e\xe7\xa7\x91\xe8\x90\xa8\xe8\xaf\xad', 'co': '\xe7\xa7\x91\xe8\xa5\xbf\xe5\x98\x89\xe8\xaf\xad', 'ca': '\xe5\x8a\xa0\xe6\xb3\xb0\xe7\xbd\x97\xe5\xb0\xbc\xe4\xba\x9a\xe8\xaf\xad', 'cy': '\xe5\xa8\x81\xe5\xb0\x94\xe5\xa3\xab\xe8\xaf\xad', 'cs': '\xe6\x8d\xb7\xe5\x85\x8b\xe8\xaf\xad', 'ps': '\xe6\x99\xae\xe4\xbb\x80\xe5\x9b\xbe\xe8\xaf\xad', 'pt': '\xe8\x91\xa1\xe8\x90\x84\xe7\x89\x99\xe8\xaf\xad', 'tl': '\xe8\x8f\xb2\xe5\xbe\x8b\xe5\xae\xbe\xe8\xaf\xad', 'pa': '\xe6\x97\x81\xe9\x81\xae\xe6\x99\xae\xe8\xaf\xad', 'vi': '\xe8\xb6\x8a\xe5\x8d\x97\xe8\xaf\xad', 'pl': '\xe6\xb3\xa2\xe5\x85\xb0\xe8\xaf\xad', 'hy': '\xe4\xba\x9a\xe7\xbe\x8e\xe5\xb0\xbc\xe4\xba\x9a\xe8\xaf\xad', 'hr': '\xe5\x85\x8b\xe7\xbd\x97\xe5\x9c\xb0\xe4\xba\x9a\xe8\xaf\xad', 'ht': '\xe6\xb5\xb7\xe5\x9c\xb0\xe5\x85\x8b\xe9\x87\x8c\xe5\xa5\xa5\xe5\xb0\x94\xe8\xaf\xad', 'hu': '\xe5\x8c\x88\xe7\x89\x99\xe5\x88\xa9\xe8\xaf\xad', 'hmn': '\xe8\x8b\x97\xe8\xaf\xad', 'hi': '\xe5\x8d\xb0\xe5\x9c\xb0\xe8\xaf\xad', 'ha': '\xe8\xb1\xaa\xe8\x90\xa8\xe8\xaf\xad', 'mg': '\xe9\xa9\xac\xe5\xb0\x94\xe5\x8a\xa0\xe4\xbb\x80\xe8\xaf\xad', 'uz': '\xe4\xb9\x8c\xe5\x85\xb9\xe5\x88\xab\xe5\x85\x8b\xe8\xaf\xad', 'ml': '\xe9\xa9\xac\xe6\x8b\x89\xe9\x9b\x85\xe6\x8b\x89\xe5\xa7\x86\xe8\xaf\xad', 'mn': '\xe8\x92\x99\xe5\x8f\xa4\xe8\xaf\xad', 'mi': '\xe6\xaf\x9b\xe5\x88\xa9\xe8\xaf\xad', 'mk': '\xe9\xa9\xac\xe5\x85\xb6\xe9\xa1\xbf\xe8\xaf\xad', 'ur': '\xe4\xb9\x8c\xe5\xb0\x94\xe9\x83\xbd\xe8\xaf\xad', 'mt': '\xe9\xa9\xac\xe8\x80\xb3\xe4\xbb\x96\xe8\xaf\xad', 'ms': '\xe9\xa9\xac\xe6\x9d\xa5\xe8\xaf\xad', 'mr': '\xe9\xa9\xac\xe6\x8b\x89\xe5\x9c\xb0\xe8\xaf\xad', 'haw': '\xe5\xa4\x8f\xe5\xa8\x81\xe5\xa4\xb7\xe8\xaf\xad', 'my': '\xe7\xbc\x85\xe7\x94\xb8\xe8\xaf\xad', 'af': '\xe5\xb8\x83\xe5\xb0\x94\xe8\xaf\xad(\xe5\x8d\x97\xe9\x9d\x9e\xe8\x8d\xb7\xe5\x85\xb0\xe8\xaf\xad)', 'sw': '\xe6\x96\xaf\xe7\x93\xa6\xe5\xb8\x8c\xe9\x87\x8c\xe8\xaf\xad', 'is': '\xe5\x86\xb0\xe5\xb2\x9b\xe8\xaf\xad', 'am': '\xe9\x98\xbf\xe5\xa7\x86\xe5\x93\x88\xe6\x8b\x89\xe8\xaf\xad', 'it': '\xe6\x84\x8f\xe5\xa4\xa7\xe5\x88\xa9\xe8\xaf\xad', 'iw': '\xe5\xb8\x8c\xe4\xbc\xaf\xe6\x9d\xa5\xe8\xaf\xad', 'kn': '\xe5\x8d\xa1\xe7\xba\xb3\xe8\xbe\xbe\xe8\xaf\xad', 'ar': '\xe9\x98\xbf\xe6\x8b\x89\xe4\xbc\xaf\xe8\xaf\xad', 'su': '\xe5\x8d\xb0\xe5\xb0\xbc\xe5\xb7\xbd\xe4\xbb\x96\xe8\xaf\xad', 'et': '\xe7\x88\xb1\xe6\xb2\x99\xe5\xb0\xbc\xe4\xba\x9a\xe8\xaf\xad', 'az': '\xe9\x98\xbf\xe5\xa1\x9e\xe6\x8b\x9c\xe7\x96\x86\xe8\xaf\xad', 'id': '\xe5\x8d\xb0\xe5\xb0\xbc\xe8\xaf\xad', 'ig': '\xe4\xbc\x8a\xe5\x8d\x9a\xe8\xaf\xad', 'nl': '\xe8\x8d\xb7\xe5\x85\xb0\xe8\xaf\xad', 'no': '\xe6\x8c\xaa\xe5\xa8\x81\xe8\xaf\xad', 'ne': '\xe5\xb0\xbc\xe6\xb3\x8a\xe5\xb0\x94\xe8\xaf\xad', 'ny': '\xe9\xbd\x90\xe5\x88\x87\xe7\x93\xa6\xe8\xaf\xad', 'fr': '\xe6\xb3\x95\xe8\xaf\xad', 'ku': '\xe5\xba\x93\xe5\xb0\x94\xe5\xbe\xb7\xe8\xaf\xad', 'fy': '\xe5\xbc\x97\xe9\x87\x8c\xe8\xa5\xbf\xe8\xaf\xad', 'fa': '\xe6\xb3\xa2\xe6\x96\xaf\xe8\xaf\xad', 'fi': '\xe8\x8a\xac\xe5\x85\xb0\xe8\xaf\xad', 'ka': '\xe6\xa0\xbc\xe9\xb2\x81\xe5\x90\x89\xe4\xba\x9a\xe8\xaf\xad', 'kk': '\xe5\x93\x88\xe8\x90\xa8\xe5\x85\x8b\xe8\xaf\xad', 'sr': '\xe5\xa1\x9e\xe5\xb0\x94\xe7\xbb\xb4\xe4\xba\x9a\xe8\xaf\xad', 'sq': '\xe9\x98\xbf\xe5\xb0\x94\xe5\xb7\xb4\xe5\xb0\xbc\xe4\xba\x9a\xe8\xaf\xad', 'ko': '\xe9\x9f\xa9\xe8\xaf\xad', 'sv': '\xe7\x91\x9e\xe5\x85\xb8\xe8\xaf\xad', 'km': '\xe9\xab\x98\xe6\xa3\x89\xe8\xaf\xad', 'st': '\xe5\xa1\x9e\xe7\xb4\xa2\xe6\x89\x98\xe8\xaf\xad', 'sk': '\xe6\x96\xaf\xe6\xb4\x9b\xe4\xbc\x90\xe5\x85\x8b\xe8\xaf\xad', 'si': '\xe5\x83\xa7\xe4\xbc\xbd\xe7\xbd\x97\xe8\xaf\xad', 'so': '\xe7\xb4\xa2\xe9\xa9\xac\xe9\x87\x8c\xe8\xaf\xad', 'sn': '\xe4\xbf\xae\xe7\xba\xb3\xe8\xaf\xad', 'sm': '\xe8\x90\xa8\xe6\x91\xa9\xe4\xba\x9a\xe8\xaf\xad', 'sl': '\xe6\x96\xaf\xe6\xb4\x9b\xe6\x96\x87\xe5\xb0\xbc\xe4\xba\x9a\xe8\xaf\xad', 'ky': '\xe5\x90\x89\xe5\xb0\x94\xe5\x90\x89\xe6\x96\xaf\xe8\xaf\xad', 'sd': '\xe4\xbf\xa1\xe5\xbe\xb7\xe8\xaf\xad'}
def translate(text):
    '''''模拟浏览器的行为，向Google Translate的主页发送数据，然后抓取翻译结果 '''
    #text 输入要翻译的英文句子
    if (text=="")or(text==None):
        return 'NULL','NULL'
    text_1=text.replace('.',' ').replace('/',' ')
    #'langpair':'en'|'zh-CN'从自动到简体中文
    values={'hl':'zh-CN','ie':'UTF-8','text':text_1,'langpair':"'auto'|'zh-CN'"}
    url='http://translate.google.cn/'
    data = urllib.urlencode(values)
    req = urllib2.Request(url,data)
    #模拟一个浏览器
    browser='Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)'
    req.add_header('User-Agent',browser)
    #向谷歌翻译发送请求
    response = urllib2.urlopen(req)
    #读取返回页面
    html=response.read()
    #从返回页面中过滤出翻译后的文本
    #使用正则表达式匹配
    #翻译后的文本是'TRANSLATED_TEXT='等号后面的内容
    #.*? non-greedy or minimal fashion
    #(?<=...)Matches if the current position in the string is preceded
    #by a match for ... that ends at the current position
    selector=etree.HTML(html)
    Lang=selector.xpath('//*[@id="gt-otf-switch"]/@href')
    Lang=re.findall('&sl=(.*?)&',repr(Lang))
    Lang=''.join(Lang)
    result=re.findall("TRANSLATED_TEXT=\'(.*?)\';",html)#TRANSLATED_TEXT='大方的风格';INPUT
    result=''.join(result)
    res = result.replace("\\x3cbr\\x3e", "\r\n")  #换行符替换
    if LangDit[Lang]=='中文':  #繁体转简体
        res = Converter('zh-hans').convert( res.decode('utf-8'))
        res = res.encode('utf-8')
    return LangDit[Lang],res

def DeleteProperty(TableName,TranslateColuname):
    # Save the Register user's Information to MySQL
    try:
        conn = pymysql.connect(host=mysqldbip,user=mysqldbuser,passwd=mysqldbpsw,db=dbname,port=3306,charset='utf8')
        if(conn != None):
            now = time.strftime("%Y-%m-%d %H:%M:%S")
            print now + "  MySQL Connecting OK!"
            cur = conn.cursor()
            Command=" alter table "+TableName+" drop "+TranslateColuname
            cur.execute(Command)
            conn.commit()
            cur.close()
            conn.close()
            print ("Dlete property in table %s successful!"%TableName)# print("The length of %s is %d" % (s,x))
            return 1
        else:
            now = time.strftime("%Y-%m-%d %H:%M:%S")  # ？？
            print now + "  MySQL Connection Exception!"
            return False
    except MySQLdb.Error,e:
        print now + "  Mysql Error %d: %s" % (e.args[0], e.args[1])
        if e.args[0]==1060:
            return 3
        else:
            return 0

def AddProperty(TableName,language,TranslateColuname):
    # Save the Register user's Information to MySQL
    try:
        conn =pymysql.connect(host=mysqldbip,user=mysqldbuser,passwd=mysqldbpsw,db=dbname,port=3306,charset='utf8')
        if(conn != None):
            now = time.strftime("%Y-%m-%d %H:%M:%S")
            print now + "  MySQL Connecting OK!"
            cur = conn.cursor()
            Command=" alter table "+TableName+" add "+language+" varchar(30) default null,add "+TranslateColuname+" varchar (1000) default null"
            cur.execute(Command)
            cur.execute('SET @@GLOBAL.sql_mode="NO_AUTO_Create_USER,NO_ENGINE_SUBSTITUTION"')
            conn.commit()
            cur.close()
            conn.close()
            return 1
        else:
            now = time.strftime("%Y-%m-%d %H:%M:%S")  # ？？
            print now + "  MySQL Connection Exception!"
            return False
    except  pymysql.Error,e:
        print now + "  Mysql Error %d: %s" % (e.args[0], e.args[1])
        if e.args[0]==1060:
            return 3
        else:
            return 0




def TranslationinMySQL(TableName,ColuName,language,TranslateColuname):
    # Save the Register user's Information to MySQL
    try:
        conn = pymysql.connect(host=mysqldbip,user=mysqldbuser,passwd=mysqldbpsw,db=dbname,port=3306,charset='utf8')
        conn2 = pymysql.connect(host=mysqldbip,user=mysqldbuser,passwd=mysqldbpsw,db=dbname,port=3306,charset='utf8')
        if((conn != None)&(conn2!=None)):
            now = time.strftime("%Y-%m-%d %H:%M:%S")
            print now + "  MySQL Connecting OK!"
            cur = conn.cursor()
            cur2=conn2.cursor()

            ShowCommand=' Describe '+TableName#获取要翻译列名的序号
            res=cur.execute(ShowCommand)
            ColUNameDict={}
            numrows = int(cur.rowcount)
            for i in range(numrows):
                row = cur.fetchone()
                ColUNameDict[i]=row[0]
            conn.commit()
            ColUNameDict=dict((v,k) for k,v in ColUNameDict.iteritems())
            ColuNum=ColUNameDict[ColuName]

            ReadCommand=" SELECT * FROM "+TableName+" where language is null "#读取未翻译的记录
            cur.execute(ReadCommand)
            conn.commit()
            START='Translate the "'+ColuName+'" in table "'+TableName+'" start!'
            print START
            resultall = cur.fetchall()
            for row in resultall:
                translateResult=translate(row[ColuNum])
                UpdateCommand=" update "+TableName+" set "+language+'="'+translateResult[0]+'" ,'+TranslateColuname+'="'+translateResult[1]+'" where topic_id='+str(row[0])
                cur2.execute(UpdateCommand)
                conn2.commit()
                print('Id=%s have been translated!' %row[0])
                print('Language:%s Translation:%s' %(translateResult[0],translateResult[1]))
            conn2.commit()
            cur.close()
            conn.close()
            cur2.close()
            conn2.close()
            print "Translate Completed!"
            return True
        else:
            now = time.strftime("%Y-%m-%d %H:%M:%S")  # ？？
            print now + "  MySQL Connection Exception!"
            return False
    except pymysql.Error,e:
        print now + "  Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False



# insertsql = "insert into t_registerwebuser(UserName,UserPassword) values('" + username + "','" + password + "')"
# SaveOneUserToMySQL(insertsql)
AddPropertyRe=AddProperty(TableName,language,TranslateColuname)
if AddPropertyRe==1:
    print ("Add property in table %s successful!"%TableName)
elif AddPropertyRe==3:
    print ("Property have existed in table %s "%TableName)
else:
    print ("Add Property in table %s  ERROR!"%TableName)
# DeleteProperty(TableName,'translation') #删除属性
TranslationinMySQL(TableName,ColuName,language,TranslateColuname)
