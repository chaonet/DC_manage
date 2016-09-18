# coding:utf-8
import re
import telnetlib

logs = []

# 登陆设备

tn = telnetlib.Telnet('x.x.x.x')
tn.write('test' + '\n')
tn.read_until('Password:')
tn.write('test' + '\n')
echo = tn.read_until('>')
print echo
logs.append(echo)

sysname_user = re.findall(r"<.*>", echo)[0].strip('>').strip('<')

###
re.findall(r"<.*>", echo)

###

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

