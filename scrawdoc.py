#!/usr/bin/python
# -*- coding:utf-8 -*-
import os,sys,urllib,urllib2,urlparse,re
from sgmllib import SGMLParser

urlall=[]
urldoc=[]
global main_site_domain2
class URLLister(SGMLParser):
  def reset(self):
    SGMLParser.reset(self)
    self.urls=[]
    # self.imgs=[]
  def start_a(self, attrs):
    href = [ v for k,v in attrs if k=="href"]
    if href!=[]and href[0]!='':
      if not ( href[0].startswith("/javascript") or href[0].startswith("javascript")  ):
        if not href[0].startswith("http"):
          if href[0][0] == '/':
            href[0] = main_site_domain2 + href[0]
          elif  href[0].startswith("./"):
            href[0] = main_site_domain2 + href[1:]
          else:
            href[0] = main_site_domain2 + '/' + href[0]
        self.urls.append(href[0])

  def start_script(self, attr):
      self.literal = 1
          #
  # def start_img(self, attrs):
  #   src = [ v for k,v in attrs if k=="src" ]
  #   if src!=[] and src[0]!='':
  #     if src[0][0] != 'h':
  #       if src[0][0] == '/':
  #         src[0] = main_site_domain2 + src[0]
  #       else:
  #         src[0] = main_site_domain2 +'/'+ src[0]
  #     self.imgs.append(src[0])


def get_url_of_page(url):  #获取一个页面的所有url
  urls = []
  try:
    f = urllib2.urlopen(url, timeout=30).read()
    url_listen = URLLister()
    url_listen.feed(f)
    urls.extend(url_listen.urls)
  except urllib2.URLError, e:
    print e.reason
    return []
  urlall.extend(urls)
  return urls

#递归处理页面
def get_page_html(begin_url, depth, ignore_outer, main_site_domain):
  #若是设置排除外站 过滤之
  if ignore_outer:
    if not main_site_domain in begin_url:
      return
  if depth == 1:
    urls = get_url_of_page(begin_url)

  else:
    urls = get_url_of_page(begin_url)
    if urls:
      urls=set(urls)
      for url in urls:
        get_page_html(url, depth-1,ignore_outer, main_site_domain)

#下载doc
def download_doc(save_path):
  print "download begin..."
  for doc in urldoc:
    try:
      filename = doc.split("/")[-1]
      dist = os.path.join(save_path, filename)
      #此方式判断图片的大小太浪费了
      #if len(urllib2.urlopen(im).read()) < min_size:
      #  continue
      #这种方式先拉头部，应该好多了，不用再下载一次
      # connection = urllib2.build_opener().open(urllib2.Request(im))
      #if int(connection.headers.dict['content-length']) < min_size:
      #  continue
      urllib.urlretrieve(doc, dist,None)
      print "Done: ", filename
    except:
      continue
  print "download end..."


def getdoc(url, max_depth, ignore_outer, download):#抓取doc首个页面,遍历深度,是否忽略外站，是否下载

    # doc保存路径
    global main_site_domain2,urlall,urldoc
    save_path = os.path.abspath("./docdownlaod")
    if not os.path.exists(save_path):
      os.mkdir(save_path)
    main_site_domain = urlparse.urlsplit(url).netloc
    s = re.findall('(.*?)/', url)
    s = s[0] + '//'
    main_site_domain2 = s + urlparse.urlsplit(url).netloc
    get_page_html(url, max_depth, ignore_outer, main_site_domain)
    urlall = set(urlall)
    for i in urlall:
      if i.endswith('.doc') or i.endswith('.docx'):
        urldoc.append(i)
    if urldoc==[]:
      print "DocUrl Not Find !"
    else:
      print "DocUrl Find!"
      f = open('urldoc.txt', 'a+')#存储docurl文件
      for i in urldoc:
        f.write((i+'\n'))
        print i
      f.close
      if download==True:
        download_doc(save_path)

if __name__ == "__main__":
  #抓取doc首个页面
  url = "http://gs.hhu.edu.cn/"
  #doc保存路径
  save_path = os.path.abspath("./docdownlaod")
  if not os.path.exists(save_path):
    os.mkdir(save_path)
  #遍历深度
  max_depth =2
  #是否只遍历目标站内，即存在外站是否忽略
  ignore_outer = True
  main_site_domain = urlparse.urlsplit(url).netloc
  s=re.findall('(.*?)/',url)
  s=s[0]+'//'
  main_site_domain2 = s+urlparse.urlsplit(url).netloc
  get_page_html(url, max_depth, ignore_outer, main_site_domain)
  urlall = set(urlall)
  for i in urlall:
    if i.endswith('.doc') or i.endswith('.docx'):
      urldoc.append(i)
  if urldoc == []:
    print "DocUrl Not Find !"
  else:
    print "DocUrl Find!"
    f = open('urldoc.txt', 'a+')  # 存储docurl文件
    for i in urldoc:
      f.write((i + '\n'))
      print i
    f.close
    download_doc(save_path)
