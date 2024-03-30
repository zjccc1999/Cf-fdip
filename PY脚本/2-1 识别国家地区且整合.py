import os
import re
import geoip2.database
import tkinter as tk
from tkinter import filedialog

def process_file(file_path):
    if os.path.exists(file_path):
        process_files(file_path)
        print(f"处理文件 {os.path.basename(file_path)} 完成！")
    else:
        print(f"文件 {os.path.basename(file_path)} 不存在！")

def process_files(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
        # 使用正则表达式查找IP地址并去重处理
        ip_addresses = list(set(re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', data)))  # 去重处理

        reader = geoip2.database.Reader('GeoLite2-Country.mmdb')
        country_ip_map = {}
        for ip in ip_addresses:
            try:
                response = reader.country(ip)
                country_code = response.country.iso_code
                if country_code not in country_ip_map:
                    country_ip_map[country_code] = []
                country_ip_map[country_code].append(ip)
            except:
                pass

        folder_name = os.path.splitext(os.path.basename(file_path))[0]
        output_folder = os.path.join(os.path.dirname(file_path), folder_name)
        os.makedirs(output_folder, exist_ok=True)

        for country_code, ips in country_ip_map.items():
            output_filename = os.path.join(output_folder, f'{country_code}.txt')
            with open(output_filename, 'a') as output_file:
                for ip in ips:
                    output_file.write(f'{ip}\n')

        reader.close()

# 创建 Tkinter 窗口
root = tk.Tk()
root.title("IP 地址处理程序")

# 创建处理文件按钮
file_names = ['GFYMIP.txt', 'ipdb.txt', 'zipbaipiao.txt', 'FDYMIP.txt']

# 创建按钮处理指定文件
for file_name in file_names:
    button = tk.Button(root, text=f"处理 {file_name}", command=lambda name=file_name: process_file(os.path.join(os.getcwd(), name)))
    button.pack(pady=10)

# 创建按钮让用户自由选择文件
def select_file():
    file_path = filedialog.askopenfilename(filetypes=[('Text files', '*.txt')])
    if file_path:
        process_file(file_path)

select_file_button = tk.Button(root, text="自由选择文件", command=select_file)
select_file_button.pack(pady=10)

root.mainloop()
