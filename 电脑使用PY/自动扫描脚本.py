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
powershell_command_17 = "powershell.exe -Command \"ed iptest -a 209242 -e=false\""
powershell_command_18 = "powershell.exe -Command \"ed iptest -a 13335 -e=false\""

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

# 等待 5 秒钟
print("等待 5 秒钟...")
time.sleep(10)

# 执行第七个 PowerShell 命令
try:
    subprocess.run(powershell_command_7, shell=True, check=True)
    print("第七个 PowerShell 程序执行成功！")
except subprocess.CalledProcessError as e:
    print("第七个 PowerShell 程序执行失败：", e)

# 等待 5 秒钟
print("等待 5 秒钟...")
time.sleep(10)

# 执行第八个 PowerShell 命令
try:
    subprocess.run(powershell_command_8, shell=True, check=True)
    print("第八个 PowerShell 程序执行成功！")
except subprocess.CalledProcessError as e:
    print("第八个 PowerShell 程序执行失败：", e)

# 等待 5 秒钟
print("等待 5 秒钟...")
time.sleep(10)

# 执行第九个 PowerShell 命令
try:
    subprocess.run(powershell_command_9, shell=True, check=True)
    print("第九个 PowerShell 程序执行成功！")
except subprocess.CalledProcessError as e:
    print("第九个 PowerShell 程序执行失败：", e)

# 等待 5 秒钟
print("等待 5 秒钟...")
time.sleep(10)

# 执行第十个 PowerShell 命令
try:
    subprocess.run(powershell_command_10, shell=True, check=True)
    print("第十个 PowerShell 程序执行成功！")
except subprocess.CalledProcessError as e:
    print("第十个 PowerShell 程序执行失败：", e)

# 等待 5 秒钟
print("等待 5 秒钟...")
time.sleep(10)

# 执行第十一个 PowerShell 命令
try:
    subprocess.run(powershell_command_11, shell=True, check=True)
    print("第十一个 PowerShell 程序执行成功！")
except subprocess.CalledProcessError as e:
    print("第十一个 PowerShell 程序执行失败：", e)

# 等待 5 秒钟
print("等待 5 秒钟...")
time.sleep(10)

# 执行第十二个 PowerShell 命令
try:
    subprocess.run(powershell_command_12, shell=True, check=True)
    print("第十二个 PowerShell 程序执行成功！")
except subprocess.CalledProcessError as e:
    print("第十二个 PowerShell 程序执行失败：", e)

# 等待 5 秒钟
print("等待 5 秒钟...")
time.sleep(10)

# 执行第十三个 PowerShell 命令
try:
    subprocess.run(powershell_command_13, shell=True, check=True)
    print("第十三个 PowerShell 程序执行成功！")
except subprocess.CalledProcessError as e:
    print("第十三个 PowerShell 程序执行失败：", e)

# 等待 5 秒钟
print("等待 5 秒钟...")
time.sleep(10)

# 执行第十四个 PowerShell 命令
try:
    subprocess.run(powershell_command_14, shell=True, check=True)
    print("第十四个 PowerShell 程序执行成功！")
except subprocess.CalledProcessError as e:
    print("第十四个 PowerShell 程序执行失败：", e)

# 等待 5 秒钟
print("等待 5 秒钟...")
time.sleep(10)

# 执行第十五个 PowerShell 命令
try:
    subprocess.run(powershell_command_15, shell=True, check=True)
    print("第十五个 PowerShell 程序执行成功！")
except subprocess.CalledProcessError as e:
    print("第十五个 PowerShell 程序执行失败：", e)

# 等待 5 秒钟
print("等待 5 秒钟...")
time.sleep(10)

# 执行第十六个 PowerShell 命令
try:
    subprocess.run(powershell_command_16, shell=True, check=True)
    print("第十六个 PowerShell 程序执行成功！")
except subprocess.CalledProcessError as e:
    print("第十六个 PowerShell 程序执行失败：", e)

    # 执行第十七个 PowerShell 命令
try:
    subprocess.run(powershell_command_16, shell=True, check=True)
    print("第十七个 PowerShell 程序执行成功！")
except subprocess.CalledProcessError as e:
    print("第十七个 PowerShell 程序执行失败：", e)

# 执行第十八个 PowerShell 命令
try:
    subprocess.run(powershell_command_16, shell=True, check=True)
    print("第十八个 PowerShell 程序执行成功！")
except subprocess.CalledProcessError as e:
    print("第十八个 PowerShell 程序执行失败：", e)


import os
import shutil


