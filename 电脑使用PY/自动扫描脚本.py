import subprocess
import time

# 定义 PowerShell 命令
powershell_command_1 = "powershell.exe -Command \"ed iptest -a 45102 -c SIN -e=false\""
powershell_command_2 = "powershell.exe -Command \"ed iptest -a 45102 -c NRT -e=false\""
powershell_command_3 = "powershell.exe -Command \"ed iptest -a 45102 -c HKG -e=false\""
powershell_command_4 = "powershell.exe -Command \"ed iptest -a 31898 -c NRT -e=false\""
powershell_command_5 = "powershell.exe -Command \"ed iptest -a 31898 -c ICN -e=false\""
powershell_command_6 = "powershell.exe -Command \"ed iptest -a 40065 -e=false\""
powershell_command_7 = "powershell.exe -Command \"ed iptest -a 906 -e=false\""
powershell_command_8 = "powershell.exe -Command \"ed iptest -a 21887 -e=false\""
powershell_command_9 = "powershell.exe -Command \"ed iptest -a 9312 -e=false\""
powershell_command_10 = "powershell.exe -Command \"ed iptest -a 932 -e=false\""
powershell_command_11 = "powershell.exe -Command \"ed iptest -a 967 -e=false\""
powershell_command_12 = "powershell.exe -Command \"ed iptest -a 396982 -e=false\""
powershell_command_13 = "powershell.exe -Command \"ed iptest -a 3258 -e=false\""
powershell_command_14 = "powershell.exe -Command \"ed iptest -a 8075 -e=false\""
powershell_command_15 = "powershell.exe -Command \"ed iptest -a 9808 -e=false\""
powershell_command_16 = "powershell.exe -Command \"ed iptest -a 16509 -e=false\""

# 执行第一个 PowerShell 命令
try:
    subprocess.run(powershell_command_1, shell=True, check=True)
    print("第一个 PowerShell 程序执行成功！")
except subprocess.CalledProcessError as e:
    print("第一个 PowerShell 程序执行失败：", e)

# 等待 10 秒钟
print("等待 10 秒钟...")
time.sleep(10)

# 执行第二个 PowerShell 命令
try:
    subprocess.run(powershell_command_2, shell=True, check=True)
    print("第二个 PowerShell 程序执行成功！")
except subprocess.CalledProcessError as e:
    print("第二个 PowerShell 程序执行失败：", e)

# 等待 10 秒钟
print("等待 10 秒钟...")
time.sleep(10)

# 执行第三个 PowerShell 命令
try:
    subprocess.run(powershell_command_3, shell=True, check=True)
    print("第三个 PowerShell 程序执行成功！")
except subprocess.CalledProcessError as e:
    print("第三个 PowerShell 程序执行失败：", e)

# 等待 10 秒钟
print("等待 10 秒钟...")
time.sleep(10)

# 执行第四个 PowerShell 命令
try:
    subprocess.run(powershell_command_4, shell=True, check=True)
    print("第四个 PowerShell 程序执行成功！")
except subprocess.CalledProcessError as e:
    print("第四个 PowerShell 程序执行失败：", e)

# 等待 10 秒钟
print("等待 10 秒钟...")
time.sleep(10)

# 执行第五个 PowerShell 命令
try:
    subprocess.run(powershell_command_5, shell=True, check=True)
    print("第五个 PowerShell 程序执行成功！")
except subprocess.CalledProcessError as e:
    print("第五个 PowerShell 程序执行失败：", e)

# 等待 10 秒钟
print("等待 10 秒钟...")
time.sleep(10)

# 执行第六个 PowerShell 命令
try:
    subprocess.run(powershell_command_6, shell=True, check=True)
    print("第六个 PowerShell 程序执行成功！")
except subprocess.CalledProcessError as e:
    print("第六个 PowerShell 程序执行失败：", e)

# 等待 10 秒钟
print("等待 10 秒钟...")
time.sleep(10)

# 执行第七个 PowerShell 命令
try:
    subprocess.run(powershell_command_7, shell=True, check=True)
    print("第七个 PowerShell 程序执行成功！")
except subprocess.CalledProcessError as e:
    print("第七个 PowerShell 程序执行失败：", e)

# 等待 10 秒钟
print("等待 10 秒钟...")
time.sleep(10)

# 执行第八个 PowerShell 命令
try:
    subprocess.run(powershell_command_8, shell=True, check=True)
    print("第八个 PowerShell 程序执行成功！")
except subprocess.CalledProcessError as e:
    print("第八个 PowerShell 程序执行失败：", e)

# 等待 10 秒钟
print("等待 10 秒钟...")
time.sleep(10)

# 执行第九个 PowerShell 命令
try:
    subprocess.run(powershell_command_9, shell=True, check=True)
    print("第九个 PowerShell 程序执行成功！")
except subprocess.CalledProcessError as e:
    print("第九个 PowerShell 程序执行失败：", e)

# 等待 10 秒钟
print("等待 10 秒钟...")
time.sleep(10)

# 执行第十个 PowerShell 命令
try:
    subprocess.run(powershell_command_10, shell=True, check=True)
    print("第十个 PowerShell 程序执行成功！")
except subprocess.CalledProcessError as e:
    print("第十个 PowerShell 程序执行失败：", e)

# 等待 10 秒钟
print("等待 10 秒钟...")
time.sleep(10)

# 执行第十一个 PowerShell 命令
try:
    subprocess.run(powershell_command_11, shell=True, check=True)
    print("第十一个 PowerShell 程序执行成功！")
except subprocess.CalledProcessError as e:
    print("第十一个 PowerShell 程序执行失败：", e)

# 等待 10 秒钟
print("等待 10 秒钟...")
time.sleep(10)

# 执行第十二个 PowerShell 命令
try:
    subprocess.run(powershell_command_12, shell=True, check=True)
    print("第十二个 PowerShell 程序执行成功！")
except subprocess.CalledProcessError as e:
    print("第十二个 PowerShell 程序执行失败：", e)

# 等待 10 秒钟
print("等待 10 秒钟...")
time.sleep(10)

# 执行第十三个 PowerShell 命令
try:
    subprocess.run(powershell_command_13, shell=True, check=True)
    print("第十三个 PowerShell 程序执行成功！")
except subprocess.CalledProcessError as e:
    print("第十三个 PowerShell 程序执行失败：", e)

# 等待 10 秒钟
print("等待 10 秒钟...")
time.sleep(10)

# 执行第十四个 PowerShell 命令
try:
    subprocess.run(powershell_command_14, shell=True, check=True)
    print("第十四个 PowerShell 程序执行成功！")
except subprocess.CalledProcessError as e:
    print("第十四个 PowerShell 程序执行失败：", e)

# 等待 10 秒钟
print("等待 10 秒钟...")
time.sleep(10)

# 执行第十五个 PowerShell 命令
try:
    subprocess.run(powershell_command_15, shell=True, check=True)
    print("第十五个 PowerShell 程序执行成功！")
except subprocess.CalledProcessError as e:
    print("第十五个 PowerShell 程序执行失败：", e)

# 等待 10 秒钟
print("等待 10 秒钟...")
time.sleep(10)

# 执行第十六个 PowerShell 命令
try:
    subprocess.run(powershell_command_16, shell=True, check=True)
    print("第十六个 PowerShell 程序执行成功！")
except subprocess.CalledProcessError as e:
    print("第十六个 PowerShell 程序执行失败：", e)

import os
import shutil

# 获取桌面路径
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# 创建IP文件夹路径
ip_folder_path = os.path.join(desktop_path, "IP")

# 确保IP文件夹存在，如果不存在则创建
if not os.path.exists(ip_folder_path):
    os.makedirs(ip_folder_path)

# 获取桌面上所有.csv文件的列表
csv_files = [f for f in os.listdir(desktop_path) if f.endswith('.csv')]

# 将所有.csv文件移动到IP文件夹内
for csv_file in csv_files:
    src_path = os.path.join(desktop_path, csv_file)
    dest_path = os.path.join(ip_folder_path, csv_file)
    shutil.move(src_path, dest_path)

