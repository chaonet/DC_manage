# coding:utf-8
import re
import telnetlib
import xlrd
import xlwt

# 存放回显消息，保存到本地文件
logs = []

# 读取登陆地址、用户名、密码
xls_login = xlrd.open_workbook('login.xls') # 打开xls文件
table_login = xls_login.sheets()[0] # 打开第一张表
nrows_login = table_login.nrows # 获取表的行数
for i in range(nrows_login): # 循环逐行打印
    if i == 0: # 跳过第一行
        continue
    ip_addre = table_login.row_values(i)[1] # 取第二列
    print ip_addre
    username = table_login.row_values(i)[2]
    print username
    password = table_login.row_values(i)[3]
    print password

# 打开命令表格
xls_command = xlrd.open_workbook('command.xls') # 打开xls文件
table_command = xls_command.sheets()[0] # 打开第一张表
nrows_command = table_command.nrows # 获取表的行数

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

# 下发命令

for i in range(nrows_command): # 循环逐行打印
    command = table_command.row_values(i)[0] # 取第一列
    print command

    tn.write(str(command)+'\n')
    echo = tn.read_until('---- More ----',1)
    print echo
    logs.append(echo.replace('---- More ----',''))
    match = re.search(r"<.*>", echo)
    if command == 'sys':
        match = re.search(r"[.*]", echo)
    while not match:
        tn.write(' ')
        echo = tn.read_until('---- More ----',1)
        print echo.replace('---- More ----','')
        logs.append(echo.replace('---- More ----',''))
        match = re.search(r"<.*>", echo)
        if command == 'sys':
            match = re.search(r"[.*]", echo)

    with open(sysname_user+'.txt','a') as f:
        for i in logs:
            f.write(i)

# 登出

tn.close()
