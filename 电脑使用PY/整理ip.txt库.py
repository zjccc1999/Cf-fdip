import re
import tkinter as tk
from tkinter import filedialog

def remove_last_digit_and_underscore(text):
    # 删除每一行最后的数字和所有的下划线
    modified_lines = []
    for line in text.split('\n'):
        modified_lines.append(re.sub(r'[\d_]+$', '', line.rstrip('\n')))  
    return '\n'.join(modified_lines)

def remove_empty_lines(text):
    # 删除两行之间的空行
    modified_lines = []
    for line in text.split('\n'):
        line = line.strip()
        if line:
            modified_lines.append(line)
    return '\n'.join(modified_lines)

def add_number_after_hash(text):
    count_dict = {}
    text_dict = {}
    modified_lines = []
    for line in text.split('\n'):
        match = re.search(r'#(.+)$', line)
        if match:
            text = match.group(1).strip()
            if text in text_dict:
                text_dict[text].append(line)
            else:
                text_dict[text] = [line]
    
    for text, lines in text_dict.items():
        count_dict[text] = 0
        for line in lines:
            count_dict[text] += 1
            # 使用取余运算符确保数字在1到1000之间
            count = count_dict[text] % 1000
            if count == 0:
                count = 1000
            line = re.sub(r'#(.+)$', '#' + text + str(count), line)
            modified_lines.append(line.strip())
    
    return '\n'.join(modified_lines)

def remove_duplicate_ips(text):
    ips = set()  # 使用集合来存储IP地址，确保唯一性
    deduplicated_lines = []  # 存储去重后的行
    
    # 使用正则表达式寻找每一行中的IP地址
    for line in text.split('\n'):
        # 提取IP地址
        ip_match = re.search(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', line)
        if ip_match:
            ip = ip_match.group(0)
            # 检查IP地址是否已经出现过
            if ip not in ips:
                ips.add(ip)
                deduplicated_lines.append(line)
    
    return '\n'.join(deduplicated_lines)

def process_file(file_path):
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # 处理文本
    text = remove_last_digit_and_underscore(text)
    text = remove_empty_lines(text)
    text = remove_duplicate_ips(text)
    text = add_number_after_hash(text)

    # 将修改后的内容写回文件
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)

def browse_file():
    file_path = filedialog.askopenfilename()  # 打开文件对话框，选择文件
    if file_path:
        process_file(file_path)
        status_label.config(text="File processed successfully.")

# 创建主窗口
root = tk.Tk()
root.title("File Processor")

# 创建按钮
browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.pack(pady=10)

# 创建状态标签
status_label = tk.Label(root, text="")
status_label.pack(pady=10)

root.mainloop()
