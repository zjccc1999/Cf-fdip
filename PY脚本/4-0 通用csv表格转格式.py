import tkinter as tk
from tkinter import filedialog
import pandas as pd
import os
from datetime import datetime

def select_file():
    file_path = filedialog.askopenfilename(title="选择CSV文件", filetypes=[("CSV files", "*.csv")])
    if file_path:
        process_csv(file_path)

def process_csv(file_path):
    df = pd.read_csv(file_path, encoding='utf-8')

    if 'IP 地址' not in df.columns:
        print("CSV文件中不包含'IP 地址'列。")
        return

    ip_addresses = df['IP 地址']

    custom_text = input("请输入自定义字符: ")

    new_data = []
    for i, ip in enumerate(ip_addresses):
        new_data.append(ip + f":{custom_text}_" + str(i+1))

    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_file = os.path.join(os.path.dirname(file_path), f"{current_time}_GS.txt")
    with open(output_file, "w", encoding='utf-8') as file:
        for item in new_data:
            file.write("%s\n" % item)

    print("处理后的数据已保存到带时间戳的 GS.txt 文件中。")

# 创建Tkinter窗口
root = tk.Tk()
root.title("选择CSV文件")

# 添加选择文件按钮
select_button = tk.Button(root, text="选择CSV文件", command=select_file)
select_button.pack(pady=20)

# 添加处理result.csv文件按钮
def process_result_csv():
    process_csv("result.csv")

process_result_button = tk.Button(root, text="处理result.csv文件", command=process_result_csv)
process_result_button.pack(pady=10)

root.mainloop()
