import csv
import os

# 获取当前目录路径
current_directory = os.getcwd()

# 定义常规端口和非常规端口列表
regular_ports = ['80', '8080', '8880', '2052', '2082', '2086', '2095', '443', '2053', '2083', '2087', '2096', '8443']

# 保存匹配行的文件路径
output_directory = os.path.join(current_directory, 'IP库')
output_file_path_regular = os.path.join(output_directory, '常规端口.csv')
output_file_path_non_regular = os.path.join(output_directory, '非常规端口.csv')

# 创建输出目录
os.makedirs(output_directory, exist_ok=True)

# 定义标题行
header = ['IP地址', '端口', 'TLS', '数据中心', '国家', '地区', '城市', 'ASN', 'ORG', '延迟(ms)', '速度(MB/s)']

# 打开要写入的文件，如果文件不存在则创建
csv_file_regular = open(output_file_path_regular, 'a+', newline='', encoding='utf-8')
csv_file_non_regular = open(output_file_path_non_regular, 'a+', newline='', encoding='utf-8')
csv_writer_regular = csv.writer(csv_file_regular)
csv_writer_non_regular = csv.writer(csv_file_non_regular)

# 如果文件为空，写入标题行
if os.stat(output_file_path_regular).st_size == 0:
    csv_writer_regular.writerow(header)

if os.stat(output_file_path_non_regular).st_size == 0:
    csv_writer_non_regular.writerow(header)

# 集合用于存储已处理的行，实现去重
processed_rows = set()

# 遍历当前目录下的所有.csv文件
for file_name in os.listdir(current_directory):
    if file_name.endswith('.csv'):
        print(f"处理文件: {file_name}")
        with open(file_name, 'r', encoding='latin-1') as file:  # 尝试使用latin-1编码格式
            csv_reader = csv.reader(file)
            next(csv_reader)  # 跳过第一行
            data_rows = [row for row in csv_reader if len(row) == 11]

            # 按照 '速度(MB/s)' 从大到小排序
            # 按照 '速度(MB/s)' 从大到小排序
            sorted_data_rows = sorted([row for row in data_rows if row[10]], key=lambda x: float(x[10]), reverse=True)


            for row in sorted_data_rows:
                # 检查是否已处理过该行，避免重复写入
                row_key = tuple(row)
                if row_key not in processed_rows:
                    processed_rows.add(row_key)
                    if row[1] in regular_ports:
                        csv_writer_regular.writerow(row)
                    else:
                        csv_writer_non_regular.writerow(row)

# 关闭文件
csv_file_regular.close()
csv_file_non_regular.close()

print("处理完成。")
