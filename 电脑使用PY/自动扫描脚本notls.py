import subprocess
import time

# 定义 PowerShell 命令
powershell_command_1 = "powershell.exe -Command \"ed iptest -a 45102 -c SIN -e=false -t=false\""
powershell_command_2 = "powershell.exe -Command \"ed iptest -a 45102 -c NRT -e=false -t=false\""
powershell_command_3 = "powershell.exe -Command \"ed iptest -a 45102 -c HKG -e=false -t=false\""
powershell_command_4 = "powershell.exe -Command \"ed iptest -c SIN -e=false -t=false\""
powershell_command_5 = "powershell.exe -Command \"ed iptest -c NRT -e=false -t=false\""
powershell_command_6= "powershell.exe -Command \"ed iptest  -c HKG -e=false -t=false\""

# 执行第一个 PowerShell 命令
try:
    subprocess.run(powershell_command_1, shell=True, check=True)
    print("第一个 PowerShell 程序执行成功！")
except subprocess.CalledProcessError as e:
    print("第一个 PowerShell 程序执行失败：", e)

# 等待 5 秒钟
print("等待 5 秒钟...")
time.sleep(10)

# 执行第二个 PowerShell 命令
try:
    subprocess.run(powershell_command_2, shell=True, check=True)
    print("第二个 PowerShell 程序执行成功！")
except subprocess.CalledProcessError as e:
    print("第二个 PowerShell 程序执行失败：", e)

# 等待 5 秒钟
print("等待 5 秒钟...")
time.sleep(10)

# 执行第三个 PowerShell 命令
try:
    subprocess.run(powershell_command_3, shell=True, check=True)
    print("第三个 PowerShell 程序执行成功！")
except subprocess.CalledProcessError as e:
    print("第三个 PowerShell 程序执行失败：", e)

# 等待 5 秒钟
print("等待 5 秒钟...")
time.sleep(10)

# 执行第四个 PowerShell 命令
try:
    subprocess.run(powershell_command_4, shell=True, check=True)
    print("第四个 PowerShell 程序执行成功！")
except subprocess.CalledProcessError as e:
    print("第四个 PowerShell 程序执行失败：", e)

# 等待 5 秒钟
print("等待 5 秒钟...")
time.sleep(10)

# 执行第五个 PowerShell 命令
try:
    subprocess.run(powershell_command_5, shell=True, check=True)
    print("第五个 PowerShell 程序执行成功！")
except subprocess.CalledProcessError as e:
    print("第五个 PowerShell 程序执行失败：", e)

# 等待 5 秒钟
print("等待 5 秒钟...")
time.sleep(10)

# 执行第六个 PowerShell 命令
try:
    subprocess.run(powershell_command_6, shell=True, check=True)
    print("第六个 PowerShell 程序执行成功！")
except subprocess.CalledProcessError as e:
    print("第六个 PowerShell 程序执行失败：", e)


import os
import shutil


