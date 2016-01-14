#coding=utf-8
import solr,MySQLdb


#SOLR
s = solr.Solr("http://192.168.5.220:8080/solr")
#MySQL
db_conn = MySQLdb.connect(host="192.168.5.121", db="yuqing", user="root",
                           passwd="root", charset="utf8")


