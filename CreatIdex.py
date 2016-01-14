import solr
import MySQLdb
import time
import setting1
s = setting1.s
conn = setting1.db_conn
cursor = conn.cursor()
def main():
    query = "SELECT id,post_time,title,content from post where language_type=0"
#query = "SELECT id,post_time,title,content from post where language_type=1 limit 280000,280000"
#query = "SELECT id,post_time,title,content from post where language_type=2 limit 0,300000"
##print '11'
    cursor.execute(query)
    all_text=cursor.fetchall()
    for i in all_text:
        print type(i[0])
        time1=str(i[1])
        time1=time1.replace('::',':')
        secs= time.mktime(time.strptime(time1, '%Y-%m-%d %H:%M:%S'))
##    print i[0]
##    print i[1]
##    print i[2]
##    print i[3]
        try:
            doc = dict(id=i[0], post_time=long(secs), title=i[2], content=i[3])
        except Exception,e:
            print Exception
        try:
            s.add(doc, commit=False)
        except Exception:
            print("A doc add failed,id:%s" % \
                doc["id"])
    s.commit()
    s.close()

main()

