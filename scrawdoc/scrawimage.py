
#!/usr/bin/python
# -*- coding:utf-8 -*-
# author: wklken
# 2012-03-17 wklken@yeah.net
#1实现url解析 #2实现图片下载 #3优化重构
#4多线程 尚未加入

import os,sys,urllib,urllib2,urlparse
from sgmllib import SGMLParser

img = []
class URLLister(SGMLParser):
  def reset(self):
    SGMLParser.reset(self)
    self.urls=[]
    self.imgs=[]
  def start_a(self, attrs):
    href = [ v for k,v in attrs if k=="href" and v.startswith("http")]
    if href:
      self.urls.extend(href)
  def start_img(self, attrs):
    src = [ v for k,v in attrs if k=="src" and v.startswith("http") ]
    if src:
      self.imgs.extend(src)


def get_url_of_page(url, if_img = False):
  urls = []
  try:
    f = urllib2.urlopen(url, timeout=1).read()
    url_listen = URLLister()
    url_listen.feed(f)
    if if_img:
      urls.extend(url_listen.imgs)
    else:
      urls.extend(url_listen.urls)
  except urllib2.URLError, e:
    print e.reason
  return urls

#递归处理页面
def get_page_html(begin_url, depth, ignore_outer, main_site_domain):
  #若是设置排除外站 过滤之
  if ignore_outer:
    if not main_site_domain in begin_url:
      return

  if depth == 1:
    urls = get_url_of_page(begin_url, True)
    img.extend(urls)
  else:
    urls = get_url_of_page(begin_url)
    if urls:
      for url in urls:
        get_page_html(url, depth-1)

#下载图片
def download_img(save_path, min_size):
  print "download begin..."
  for im in img:
    filename = im.split("/")[-1]
    dist = os.path.join(save_path, filename)
    #此方式判断图片的大小太浪费了
    #if len(urllib2.urlopen(im).read()) < min_size:
    #  continue
    #这种方式先拉头部，应该好多了，不用再下载一次
    connection = urllib2.build_opener().open(urllib2.Request(im))
    if int(connection.headers.dict['content-length']) < min_size:
      continue
    urllib.urlretrieve(im, dist,None)
    print "Done: ", filename
  print "download end..."

if __name__ == "__main__":
  #抓取图片首个页面
  url = "http://www.baidu.com/"
  #图片保存路径
  save_path = os.path.abspath("./downlaod")
  if not os.path.exists(save_path):
    os.mkdir(save_path)
  #限制图片最小必须大于此域值  单位 B
  min_size = 92
  #遍历深度
  max_depth = 1
  #是否只遍历目标站内，即存在外站是否忽略
  ignore_outer = True
  main_site_domain = urlparse.urlsplit(url).netloc

  get_page_html(url, max_depth, ignore_outer, main_site_domain)

  download_img(save_path, min_size)