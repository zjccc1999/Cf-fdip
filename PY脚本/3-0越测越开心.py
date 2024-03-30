import os
import tkinter as tk
from tkinter import messagebox

# 创建主窗口
root = tk.Tk()
root.title("越测越开心")
root.geometry("400x350")

selected_port = ""
selected_text = ""
selected_protocol = ""

http_button = None
https_button = None

# 检查存在的文本文件
text_files = ['HK.txt', 'KR.txt', 'SG.txt', 'US.txt', 'TW.txt', 'AE.txt', 'US.txt', 'DE.txt', 'JP.txt', 'CA.txt', 'CH.txt', 'GB.txt', 'IN.txt', 'IT.txt', 'NL.txt', 'BG.txt', 'FR.txt', 'DK.txt', 'PH.txt', 'SE.txt', 'CN.txt', 'ID.txt']
existing_files = [file for file in text_files if os.path.isfile(file)]

# 创建HTTP按钮和对应端口
def show_http_ports():
    clear_buttons()
    http_ports = ['80', '8080', '8880', '2052', '2082', '2086', '2095']
    create_buttons(http_ports, "port")
    global selected_protocol
    selected_protocol = "HTTP"

# 创建HTTPS按钮和对应端口
def show_https_ports():
    clear_buttons()
    https_ports = ['443', '2053', '2083', '2087', '2096', '8443']
    create_buttons(https_ports, "port")
    global selected_protocol
    selected_protocol = "HTTPS"

# 清空按钮
def clear_buttons():
    for widget in root.winfo_children():
        if isinstance(widget, tk.Button):
            widget.destroy()

# 创建按钮
def create_buttons(items, category):
    for item in items:
        if category == "port":
            button = tk.Button(root, text=item, command=lambda i=item: set_port(i))
        elif category == "text":
            button = tk.Button(text_frame, text=item, command=lambda i=item: run_cmd(selected_port, i, selected_protocol))
        button.pack()

# 设置选定的端口
def set_port(port):
    global selected_port
    selected_port = port
    messagebox.showinfo("提示", f"您选择的端口是: {port}")
    show_text_selection()

# 运行CMD指令
def run_cmd(port, text, protocol):
    if port and text and protocol:
        if protocol == "HTTP":
            cmd = f"CloudflareST.exe -tp {port} -f {text} -n 200 -dn 10 -sl 5 -tl 400 -url http://cs.notls.zjccc.onflashdrive.app/200m"
        elif protocol == "HTTPS":
            cmd = f"CloudflareST.exe -tp {port} -f {text} -n 200 -dn 10 -sl 5 -tl 400 -url https://cs.notls.zjccc.onflashdrive.app/200m"
        
        os.system(cmd)

        messagebox.showinfo("提示", "测试完成！")
    else:
        messagebox.showerror("错误", "请先选择端口和文本！")

# 显示文本选择按钮
def show_text_selection():
    clear_buttons()
    
    global text_frame
    text_frame = tk.Frame(root)
    text_frame.pack()

    # 显示存在的文本文件按钮
    create_buttons(existing_files, "text")

# 创建HTTP按钮
http_button = tk.Button(root, text="HTTP", command=show_http_ports)
http_button.pack()

# 创建HTTPS按钮
https_button = tk.Button(root, text="HTTPS", command=show_https_ports)
https_button.pack()

# 运行主循环
root.mainloop()
