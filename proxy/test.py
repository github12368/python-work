# -*- coding: utf-8 -*-
import  socket
print "11"
socket.setdefaulttimeout(25)
s=socket.socket()
s.connect(("124.119.81.14",80))
ans=s.recv(1024)
print ans

#
# for i in range(1,255):
#     print '192.168.5.'+str(i)
