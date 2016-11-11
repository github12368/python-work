# -*- coding: utf-8 -*-
import time,pymysql,urllib,urllib2,requests,datetime
from lxml import etree
from langconv import *
reload(sys)
sys.setdefaultencoding('utf-8')
mysqldbip = "192.168.5.168"
mysqldbuser = "root"
mysqldbpsw = "ibm18911029778"
dbname = "406"
TableName='t_registerwebuser'


def AddRecord():
    # Save the Register user's Information to MySQL
    try:
        conn =pymysql.connect(host=mysqldbip,user=mysqldbuser,passwd=mysqldbpsw,db=dbname,port=3306,charset='utf8')
        if(conn != None):
            now = time.strftime("%Y-%m-%d %H:%M:%S")
            print now + "  MySQL Connecting OK!"
            cur = conn.cursor()

            ReadCommand=" SELECT * FROM "+TableName+" where UserID >9000 and UserID <9110"
            cur.execute(ReadCommand)
            conn.commit()
            resultall = cur.fetchall()
            idkey=19597
            for row in resultall:
                print row
                row1=row[13]+datetime.timedelta(180+365,44)
                row2= row[15] + datetime.timedelta(210+365,50)
                idkey=idkey+1
                # print SortUser[m],UserWeight[m],UserLocation[m],UserImage[m],UserInduction[m],UserCnName[m]
                cur.execute("insert into t_registerwebuser(UserId,UserName,UserPassword,UserEmail,UserLanguage,UserSex,UserBirthYear,UserBirthMonth,UserBirthDay,WebSiteName,LoginUrl,RegisterUrl,UserLocation,RegTime,LiveState,CheckTime) \
                      values('%d','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % \
                       (idkey,row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row1,row[14],row2)  )
                conn.commit()

            cur.close()
            conn.close()
            print "Trans Completed!"
            return True
        else:
            now = time.strftime("%Y-%m-%d %H:%M:%S")  # ？？
            print now + "  MySQL Connection Exception!"
            return False
    except pymysql.Error,e:
        print now + "  Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False


def UpdateRecord():
    # Save the Register user's Information to MySQL
    try:
        conn =pymysql.connect(host=mysqldbip,user=mysqldbuser,passwd=mysqldbpsw,db=dbname,port=3306,charset='utf8')
        if(conn != None):
            now = time.strftime("%Y-%m-%d %H:%M:%S")
            print now + "  MySQL Connecting OK!"
            cur = conn.cursor()
            ReadCommand=" SELECT * FROM t_registerwebuser where UserID > 1949"
            cur.execute(ReadCommand)
            conn.commit()
            resultall = cur.fetchall()
            for row in resultall:
                print row
                if row[15]==None:
                    row2 = row[13] + datetime.timedelta(27, 17)
                else:
                    row2= row[15] + datetime.timedelta(27,17)
                UpdateCommand = " update t_registerwebuser set  CheckTime  ='"+ str(row2)+ "' where UserID=" + str(row[0])
                cur.execute(UpdateCommand )
                conn.commit()

            cur.close()
            conn.close()
            print "Trans Completed!"
            return True
        else:
            now = time.strftime("%Y-%m-%d %H:%M:%S")  # ？？
            print now + "  MySQL Connection Exception!"
            return False
    except pymysql.Error,e:
        print now + "  Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False

UpdateRecord()



