# -*- coding:utf-8 -*-
import scrawdoc   #爬取成功的网址 http://bs.csu.edu.cn/,http://gs.hhu.edu.cn/
try:
    scrawdoc.getdoc("http://gs.hhu.edu.cn/",2,True,True)#抓取doc首个页面,遍历深度,是否忽略外站，是否下载
except:
    print "scraw error!"
else:
    print "scraw complete!"