#-*-coding:utf-8-*-

# http://happybase.readthedocs.org/en/latest/user.html  #用户手册
from collections import OrderedDict
import happybase
connection = happybase.Connection('192.168.5.170')
print connection.tables()

# connection.create_table(   #创建表
#     'mytable',
#     {'cf1': dict(max_versions=10),
#      'cf2': dict(max_versions=1, block_cache_enabled=False),
#      'cf3': dict(),  # use defaults
#     }
# )

table = connection.table('FBMessageCert')  #连接表

#
for key, data in table.scan():  #查看表中行row
     print key, data
# for key, data in table.scan(row_start='aaa', row_stop='xyz'):
#     print key, data

# row = table.row('20151020204908-010152908725349853-0000000000www.facebook.com') #查询一行中固定列值
# print row['attribute:time']   # prints the value of cf1:col1

# row = table.row('20151020204908-010152908725349853-0000000000www.facebook.com', columns=['attribute']) #查看一行固定列族
# print row


# rows = table.rows(['20151020204908-010152908725349853-0000000000www.facebook.com'])#查询一行所有数据，可多行
# for key, data in rows:
#     print key, data

# rows = table.rows(['row-key-1', 'row-key-2'])
# for key, data in rows:
#     print key, data
# rows_as_ordered_dict = OrderedDict(table.rows(['row-key-1', 'row-key-2']))#转换成有序字典

# table.put('row-key', {'cf:col1': 'value1',  #存储数据
#                       'cf:col2': 'value2'})
# table.put('row-key', {'cf:col1': 'value1'}, timestamp=123456789)

# table.delete('row-key') #删除数据
# table.delete('row-key', columns=['cf1:col1', 'cf1:col2'])
#
# b = table.batch()   #多值操作
# b.put('row-key-1', {'cf:col1': 'value1', 'cf:col2': 'value2'})
# b.put('row-key-2', {'cf:col2': 'value2', 'cf:col3': 'value3'})
# b.put('row-key-3', {'cf:col3': 'value3', 'cf:col4': 'value4'})
# b.delete('row-key-4')
# b.send()
