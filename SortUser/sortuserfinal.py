# -*- coding: utf-8 -*-
import time,pymysql,urllib,urllib2,sys
from lxml import etree
# from langconv import *
reload(sys)
sys.setdefaultencoding('utf-8')
mysqldbip = "192.168.5.230"
mysqldbip2 = "192.168.5.168"
mysqldbuser = "root"
mysqldbpsw = "ibm18911029778"
dbname = "showcase2016"
dbname2 = "twitter151110"
XjtuTopicTable="post_topic_user"
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
UserWeight=[]
idkey=1

def GetIdList():
    # Save the Register user's Information to MySQL
    IdList=[]
    try:
        conn = pymysql.connect(host=mysqldbip,user=mysqldbuser,passwd=mysqldbpsw,db=dbname,port=3306,charset='utf8')
        if(conn != None):
            now = time.strftime("%Y-%m-%d %H:%M:%S")
            print now + "  MySQL Connecting OK!"
            cur = conn.cursor()

            cur.execute('select distinct topic_id from post_topic_user order by topic_id asc ')   # select distinct topic_id from xjtu_post_topic order by topic_id asc
            resultall = cur.fetchall()
            for result in resultall:
                if result[0]>100:
                    IdList.append(result[0])
            # print IdList
            conn.commit()
            cur.close()
            conn.close()
            return IdList
    except pymysql.Error,e:
        print now + "  Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False

def QueryinMySQL(id):
    global idkey
    User = []
    follower = []
    tweetnumber = []
    UserDV = []
    UserCnName = []
    SortUser = []
    UserLocation = []
    UserImage=[]
    UserInduction = []
    i=0
    try:
        conn = pymysql.connect(host=mysqldbip,user=mysqldbuser,passwd=mysqldbpsw,db=dbname,port=3306,charset='utf8')
        if(conn != None):
            now = time.strftime("%Y-%m-%d %H:%M:%S")
            print now + "  MySQL Connecting OK!"
            cur = conn.cursor()
            command="select distinct user_name from post_topic_user where topic_id="+id+" and title='twitter'"
            cur.execute(command)   # select distinct topic_id from xjtu_post_topic order by topic_id asc
            resultall = cur.fetchall()
            for result in resultall:
                    User.append(result[0])
            UserNum = len(User)
            if UserNum<2:
                cur.close()
                conn.close()
                return 0
            print ("User Number is %d ." % UserNum)
            # print User
            conn.commit()
            cur.close()
            conn.close()
        else:
            now = time.strftime("%Y-%m-%d %H:%M:%S")  # ？？
            print now + "  MySQL Connection Exception!"
            return False

        conn2 = pymysql.connect(host=mysqldbip2, user=mysqldbuser, passwd=mysqldbpsw, db=dbname2, port=3306,  charset='utf8')
        if (conn2 != None):
            cur2 = conn2.cursor()
                                   #SELECT  distinct poster_name FROM xjtu_post WHERE poster_id=70292819

            for user in User:
                    command='select * from user_profile where  user_name='+"'"+user+"'"
                    cur2.execute(command)
                    result2 = cur2.fetchone()
                    if result2 !=None:
                        if  result2[9]!=None and result2[9]!='':
                            SortUser.append(result2[2])
                            tweetnumber.append(result2[6])
                            follower.append(result2[8])
                            UserCnName.append(result2[3])
                            UserDV.append(result2[17])
                            UserLocation.append(result2[9])
                            UserImage.append(result2[4])
                            UserInduction.append(result2[10])
                    conn2.commit()
            UserWeight=GetUserWeight(SortUser,follower, tweetnumber, UserDV)
            SortUserNum=len(SortUser)
            # print ("SortUser Number is %d ." % SortUserNum)
            # for m in range(SortUserNum):
            #     print SortUser[m],UserCnName[m],UserWeight[m]
            # return SortUser, follower, tweetnumber, UserDV, UserCnName,UserLocation,UserImage,UserInduction
            cur2.close()
            conn2.close()

            conn = pymysql.connect(host=mysqldbip, user=mysqldbuser, passwd=mysqldbpsw, db=dbname, port=3306,
                                   charset='utf8')
            if (conn != None):
                now = time.strftime("%Y-%m-%d %H:%M:%S")
                print now + "  MySQL Connecting OK!"
                cur = conn.cursor()
                for m in range(SortUserNum):
                    if UserCnName[m]==None:
                        UserCnName[m]=''
                    UserInduction[m]=UserInduction[m].replace("'","''").replace("\\","")
                    UserLocation[m]=UserLocation[m].replace("'","''")
                    UserCnName[m]=UserCnName[m].replace("'","''")
                    SortUser[m] =SortUser[m].replace("'", "''")
                    UserImage[m]=UserImage[m].replace("'", "''")
                    # print SortUser[m],UserWeight[m],UserLocation[m],UserImage[m],UserInduction[m],UserCnName[m]
                    text=str(idkey)+","+str(id)+","+"'"+SortUser[m]+"',"+str(UserWeight[m])+","+"'"+UserLocation[m]+"',"+"'"+UserImage[m]+"',"+"'"+UserInduction[m]+"',"+"'"+UserCnName[m]+"')"
                    idkey += 1
                    command = "insert into zcff_event_propagator(id,topic_id,user_name,weight,location,user_image,user_intruction,nick_name) values("+text
                    cur.execute(command)
                    conn.commit()
                print'postID=%s have been completed'% id
                conn.commit()
                cur.close()
                conn.close()
            else:
                now = time.strftime("%Y-%m-%d %H:%M:%S")  # ？？
                print now + "  MySQL Connection Exception!"
                return False

             # sql = "insert into person(name, age, telephone) values(%s, %s, %s)"
            # tmp = (('ninini', 89, '888999'), ('koko', 900, '999999'))
            # conn.executemany(sql, tmp)


        else:
            now = time.strftime("%Y-%m-%d %H:%M:%S")  # ？？
            print now + "  MySQL Connection Exception!"
            return False

    except pymysql.Error,e:
        print now + "  Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False





def ScoreWeight(num,weight,score):
    weightscore=[]
    if weight ==[]:
        for i in range(num):
            Weightscore = score * 0.6
            weightscore.append(Weightscore)
        return weightscore
    else:
        Max=max(weight)
        Min=min(weight)
        if Max==Min:
            for i in range(num):
                Weightscore = score * 0.6
                weightscore.append(Weightscore)
            return weightscore
        else:
            for i in range(num):
                Weightscore=score*0.6+score*0.4*(weight[i]-Min)/(Max-Min)
                weightscore.append(Weightscore)
            return weightscore


def GetUserWeight(SortUser,follower, tweetnumber, UserDV):
    num=len(SortUser)
    UserWeight=[]
    followerScore=ScoreWeight(num,follower,50)
    tweetnumberScore=ScoreWeight(num,tweetnumber,25)
    for i in range (num):
        UserWeight.append(followerScore[i]+tweetnumberScore[i]+UserDV[i]*25)
    return  UserWeight



def main():
    IdList=GetIdList()
    for id in IdList:
        print id
        QueryinMySQL(str(id))

# GetIdList()
main()



# QueryinMySQL()
# SortUserFun()
# weight=[1,100,50,4000,700,800]
# a=ScoreWeight(weight,50)
# print a

