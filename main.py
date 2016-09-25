# coding:utf-8
import re
import telnetlib
import xlrd
import xlwt

logs = []

data = xlrd.open_workbook('login.xls') # 打开xls文件
table = data.sheets()[0] # 打开第一张表
nrows = table.nrows # 获取表的行数
for i in range(nrows): # 循环逐行打印
    if i == 0: # 跳过第一行
        continue
    ip_addre = table.row_values(i)[1] # 取第二列
    print ip_addre
    username = table.row_values(i)[2]
    print username
    password = table.row_values(i)[3]
    print password


# 登陆设备

tn = telnetlib.Telnet(ip_addre)
tn.write(str(username) + '\n')
tn.read_until('Password:')
tn.write(str(password) + '\n')
echo = tn.read_until('>')
print echo
logs.append(echo)

sysname_user = re.findall(r"<.*>", echo)[0].strip('>').strip('<')

re.findall(r"<.*>", echo)

# 采集数据命令

tn.write('dis cu' + '\n')
echo = tn.read_until('---- More ----',1)
print echo
logs.append(echo.replace('---- More ----',''))
match = re.search(r"<.*>", echo)
while not match:
    tn.write(' ')
    echo = tn.read_until('---- More ----',1)
    print echo.replace('---- More ----','')
    logs.append(echo.replace('---- More ----',''))
    match = re.search(r"<.*>", echo)

with open(sysname_user+'.txt','a') as f:
    for i in logs:
        f.write(i)

# 登出

tn.close()
