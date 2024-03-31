import os
import shutil

def remove_duplicate_ips(input_file, output_file):
    unique_ips = set()

    with open(input_file, 'r') as input_f, open(output_file, 'w') as output_f:
        for line in input_f:
            ip = line.strip()
            if ip not in unique_ips:
                unique_ips.add(ip)
                output_f.write(ip + '\n')

# 要搜索的文件名列表
file_names = ['HK.txt', 'KR.txt', 'SG.txt', 'US.txt', 'TW.txt', 'AE.txt', 'US.txt', 'DE.txt', 'JP.txt', 'CA.txt', 'CH.txt', 'GB.txt', 'IN.txt', 'IT.txt', 'NL.txt']

# 创建合并文件夹前删除原有的合并文件夹
merge_folder = '合并'
if os.path.exists(merge_folder):
    shutil.rmtree(merge_folder)

# 创建新的合并文件夹
os.makedirs(merge_folder)

# 扫描当前目录及子目录
for root, dirs, files in os.walk('.'):
    for file_name in file_names:
        found_files = [f for f in files if f == file_name]
        
        if found_files:
            # 合并同名文件内容
            merged_ips = set()
            for found_file in found_files:
                with open(os.path.join(root, found_file), 'r') as f:
                    for line in f:
                        ip = line.strip()
                        merged_ips.add(ip)

            # 写入合并后的内容
            with open(os.path.join(merge_folder, file_name), 'w') as merged_file:
                for ip in merged_ips:
                    merged_file.write(ip + '\n')

            print(f"合并文件 {file_name} 完成，共有 {len(merged_ips)} 个唯一IP地址")

print("合并和去重完成！")
input("按任意键关闭程序...")
