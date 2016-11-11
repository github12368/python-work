# -*- coding: utf-8 -*-
import time,pymysql,urllib,urllib2,sys
from lxml import etree
# from langconv import *
reload(sys)
sys.setdefaultencoding('utf-8')
mysqldbip = "192.168.5.168"
mysqldbuser = "root"
mysqldbpsw = "ibm18911029778"
dbname = "twitter151110"
UserTable='user_profile'
MessageTable="title_message"
MessageColuName='title'
UserClouName="screenname"
SouceUserColuName="origin_user_name"
UserCloueEnName="user_name"
UserClouCnName2="user_aliasname"
TweetNumColuName="tweet"
FollowerNumColuName="follower"
struct =[]
User=[]
follower=[]
tweetnumber=[]
UserDV=[]
UserCnName=[]
SortUser=[]
UserWeight=[]

def QueryinMySQL():
    # Save the Register user's Information to MySQL
    global User,follower,tweetnumber,UserDV,UserCnName,SortUser
    i=0
    KeyWord=raw_input("Plesase Input Theme:")
    # KeyWord="新疆"
    try:
        conn = pymysql.connect(host=mysqldbip,user=mysqldbuser,passwd=mysqldbpsw,db=dbname,port=3306,charset='utf8')
        if(conn != None):
            now = time.strftime("%Y-%m-%d %H:%M:%S")
            print now + "  MySQL Connecting OK!"
            cur = conn.cursor()

            cur.execute('select * from title_message')
            resultall = cur.fetchall()
            for result in resultall:
                if KeyWord in result[4]:
                    i+= 1
                    print result[4],result[6],result[11]
                    User.append(result[6])
                    if result[11] !=None:
                        User.append(result[11])
            conn.commit()
            print User
            cur.close()
            conn.close()
            User=set(User)
            UserNum = len(User)
            print ("Message Number is %d ." % i)
            print ("User Number is %d ." % UserNum)
        else:
            now = time.strftime("%Y-%m-%d %H:%M:%S")  # ？？
            print now + "  MySQL Connection Exception!"
            return False

        conn2 = pymysql.connect(host=mysqldbip, user=mysqldbuser, passwd=mysqldbpsw, db=dbname, port=3306,  charset='utf8')
        if (conn2 != None):
            cur2 = conn2.cursor()
            cur2.execute('select * from user_profile')
            result2all= cur2.fetchall()
            for result2 in result2all:
                    if result2[2] in User:
                            SortUser.append(result2[2])
                            tweetnumber.append(result2[6])
                            follower.append(result2[8])
                            UserCnName.append(result2[3])
                            UserDV.append(result2[17])
            conn2.commit()
            cur2.close()
            conn2.close()
            SortUserNum=len(SortUser)
            print ("SortUser Number is %d ." % SortUserNum)
            # for m in range(SortUserNum):
            #     print SortUser[m],UserCnName[m],tweetnumber[m],follower[m],UserDV[m]

        else:
            now = time.strftime("%Y-%m-%d %H:%M:%S")  # ？？
            print now + "  MySQL Connection Exception!"
            return False

    except pymysql.Error,e:
        print now + "  Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False





def ScoreWeight(weight,score):
    weightscore=[]
    num=len(weight)
    Max=max(weight)
    Min=min(weight)
    for i in range(num):
        Weightscore=score*0.6+score*0.4*(weight[i]-Min)/(Max-Min)
        weightscore.append(Weightscore)
    return weightscore


def SortUserFun():
    global SortUser, follower, tweetnumber, UserDV, UserCnName,UserWeight
    num = len(SortUser)
    followerScore=ScoreWeight(follower,50)
    tweetnumberScore=ScoreWeight(tweetnumber,25)
    for i in range (num):
        UserWeight.append(followerScore[i]+tweetnumberScore[i]+UserDV[i]*50)
        if(UserCnName[i]!=None):
            SortUser[i]=UserCnName[i]
    DICT=dict(zip(SortUser, UserWeight))
    newdict=sorted(DICT.iteritems(), key=lambda d: d[1], reverse=True)
    num=raw_input("Plesase Input The Number of Display User:")
    for i in range(int(num)):
       print i+1,newdict[i][0],newdict[i][1]



QueryinMySQL()
SortUserFun()
# weight=[1,100,50,4000,700,800]
# a=ScoreWeight(weight,50)
# print a

