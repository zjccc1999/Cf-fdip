import os
import requests
import zipfile

# 设置代理信息
proxy_host = "127.0.0.1"
proxy_port = 7897
proxies = {
    'http': f'socks5://{proxy_host}:{proxy_port}',
    'https': f'socks5://{proxy_host}:{proxy_port}'
}

# 获取当前工作目录
current_dir = os.getcwd()

# 定义检查网络连通性的函数
def check_network_access(url):
    try:
        response = requests.get(url)
        return True
    except requests.exceptions.RequestException:
        return False

# 定义要访问的网页 URL
url = "https://zip.baipiao.eu.org/"

# 判断当前网络是否能够正常访问网页
if check_network_access(url):
    response = requests.get(url, verify=True)  # 设置verify=True进行SSL证书验证
else:
    response = requests.get(url, proxies=proxies, verify=True)  # 使用 SOCKS5 代理访问

# 将文件下载到本地
with open(os.path.join(current_dir, "txt.zip"), "wb") as file:
    file.write(response.content)

# 检查文件是否为ZIP文件
if not zipfile.is_zipfile(os.path.join(current_dir, "txt.zip")):
    print("下载的文件不是一个有效的ZIP文件。")
else:
    # 解压文件到txt文件夹
    with zipfile.ZipFile(os.path.join(current_dir, "txt.zip"), 'r') as zip_ref:
        zip_ref.extractall(os.path.join(current_dir, "txt"))

    # 合并所有文本文件为一个文件
    with open(os.path.join(current_dir, "zipbaipiao.txt"), "w") as output_file:
        for root, dirs, files in os.walk(os.path.join(current_dir, "txt")):
            for file in files:
                if file.endswith(".txt"):
                    with open(os.path.join(root, file), "r") as input_file:
                        output_file.write(input_file.read() + "\n")

    # 移动文件到脚本目录
    os.replace(os.path.join(current_dir, "zipbaipiao.txt"), os.path.join(current_dir, "zipbaipiao.txt"))

    # 删除原始压缩文件和解压后的文件夹
    os.remove(os.path.join(current_dir, "txt.zip"))
    for root, dirs, files in os.walk(os.path.join(current_dir, "txt")):
        for file in files:
            os.remove(os.path.join(root, file))
    os.rmdir(os.path.join(current_dir, "txt"))

    print("文件下载、解压、合并和移动完成。")

# 删除txt.zip文件
if os.path.exists(os.path.join(current_dir, "txt.zip")):
    os.remove(os.path.join(current_dir, "txt.zip"))
    print("已删除txt.zip文件。")
