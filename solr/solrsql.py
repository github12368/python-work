#coding=utf-8
import solr,MySQLdb

#SOLR
s = solr.Solr("http://192.168.5.220:8080/solr")
#MySQL
# db_conn = MySQLdb.connect(host="192.168.5.121", db="yuqing", user="root",
#                            passwd="root", charset="utf8")
def Query():
    response=s.select('japan,',fields='id,post_time,title,content',highlight=True)
    while len(response.results)!= 0:
                for hit in response.results:
                    d=hit['id'].encode("utf-8")
                    print hit
                    # sql =("update post set choice=1 where id='%s'"%d)
                    # try:
                    #     conn.ping()
                    # except:
                    #     cur = conn.cursor()
                    # cur.execute(sql)
                    # conn.commit()
Query()




