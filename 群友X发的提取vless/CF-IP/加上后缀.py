import os
import tkinter as tk
from tkinter import filedialog

def add_comment(file_path, file_name):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open(file_path, 'w') as file:
        for i, line in enumerate(lines):
            line = line.strip()
            line += f'#{file_name}_{i+1}\n'
            file.write(line)

def create_buttons():
    file_list = [file for file in os.listdir() if file.endswith('.txt')]
    for file_name in file_list:
        file_path = os.path.join(os.getcwd(), file_name)
        button = tk.Button(root, text=file_name, command=lambda path=file_path, name=file_name[:-4]: add_comment(path, name))
        button.pack()

root = tk.Tk()
root.title("自动添加注释")
root.geometry("300x200")

create_buttons()

root.mainloop()
