import os
import requests
import zipfile
import socket
import re
from tkinter import Tk, Label, Button, messagebox

class Application:
    def __init__(self, master=None):
        self.master = master
        self.label = Label(text="请选择一个操作")
        self.label.pack()
        self.download_button = Button(text="获取zipbaipiao", command=self.download_and_unzip)
        self.download_button.pack()
        self.get_webpage_button = Button(text="获取ipdb", command=self.get_webpage)
        self.get_webpage_button.pack()
        self.get_fdips_button = Button(text="获取反代域名IP", command=self.get_fdips)
        self.get_fdips_button.pack()
        self.get_gfips_button = Button(text="获取官方域名IP", command=self.get_gfips)
        self.get_gfips_button.pack()

    def download_and_unzip(self):
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

    messagebox.showinfo("信息", "下载并解压完成")

    def get_webpage(self):
        import os
import requests
import re

# 检测网络是否正常访问网页
def check_network(url):
    try:
        response = requests.get(url)
        return True
    except requests.exceptions.RequestException:
        return False

def get_ips_from_url(url, use_proxy=False):
    if use_proxy:
        proxies = {
            'http': 'socks5://127.0.0.1:7897',
            'https': 'socks5://127.0.0.1:7897'
        }
    else:
        proxies = None

    # 发送请求获取页面内容
    response = requests.get(url, proxies=proxies)
    ip_addresses = re.findall(r'\d+\.\d+\.\d+\.\d+', response.text)

    return ip_addresses

def update_ip_file(ip_addresses, file_path):
    print("最新的IP地址：", ip_addresses)

    # 检查文件是否存在，如果不存在，则创建
    if not os.path.exists(file_path):
        print("文件不存在，创建文件...")
        with open(file_path, 'w'):
            pass
    else:
        print("文件已存在，检查是否有重复的IP地址...")

    # 打开文件并读取已有的IP地址
    existing_ips = set()
    with open(file_path, 'r') as file:
        for line in file:
            existing_ip = line.strip()
            print("已有IP地址：", existing_ip)
            existing_ips.add(existing_ip)

    # 检查最新的IP地址是否与已有的IP地址重复，如果不重复则追加到文件中
    new_ips = set(ip_addresses)
    with open(file_path, 'a') as file:
        for ip in new_ips:
            if ip not in existing_ips:
                file.write(ip + '\n')
                print("追加新的IP地址到文件中：", ip)
            else:
                print("IP地址已存在，跳过：", ip)

if __name__ == "__main__":
    url = 'https://ipdb.api.030101.xyz/?type=proxy'
    
    if check_network(url):
        print("当前网络可以正常访问该网页，不需要走代理获取IP地址。")
        ip_addresses = get_ips_from_url(url, use_proxy=False)
    else:
        print("当前网络无法访问该网页，将使用代理获取IP地址。")
        ip_addresses = get_ips_from_url(url, use_proxy=True)

    update_ip_file(ip_addresses, 'ipdb.txt')

    messagebox.showinfo("信息", "获取ipdb完成")

    def get_fdips(self):
        import socket
import os

# 函数用于检查是否为IPv4地址
def is_ipv4(address):
    try:
        socket.inet_pton(socket.AF_INET, address)
        return True
    except socket.error:
        return False

# 获取脚本文件名（不包含扩展名）
script_name = os.path.splitext(os.path.basename(__file__))[0]

# 要查询的域名列表，每个域名占据一行
domains = '''
acjp2.cloudflarest.link
bestproxy.onecf.eu.org
acsg.cloudflarest.link
acsg3.cloudflarest.link
acjp.cloudflarest.link
cdn.shanggan.pp.ua
best.cdn.sqeven.cn
proxy.xxxxxxxx.tk
jp.anxray.top
jpcdn.raises.top
achk2.cloudflarest.link
yx.blessbai.tech
'''

domains = domains.strip().split('\n')  # 将字符串按换行符分割成列表

# 打开文件准备追加新的IPv4地址
file_path = 'FDYMIP.txt'

# 读取已有的IP地址
existing_ips = set()
if os.path.exists(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            existing_ips.add(line.strip())

# 打开文件准备追加新的IPv4地址，如果文件不存在则创建
with open(file_path, 'a+') as file:
    for domain in domains:
        try:
            # 获取完整的DNS解析结果
            result = socket.getaddrinfo(domain, None)
            ips = set([x[-1][0] for x in result if is_ipv4(x[-1][0])])  # 提取IPv4地址并去重

            for ip in ips:
                if ip not in existing_ips:
                    file.write(ip + '\n')
                    print(f'{domain} - {ip} added to file')
        except (socket.gaierror, socket.herror) as e:
            print(f'Failed to resolve {domain}: {e}')

print('新的IPv4地址追加完成。')

messagebox.showinfo("信息", "获取反代域名IP完成")

def get_gfips(self):
        import socket
import os

# 函数用于检查是否为IPv4地址
def is_ipv4(address):
    try:
        socket.inet_pton(socket.AF_INET, address)
        return True
    except socket.error:
        return False

# 函数用于检查是否为IPv6地址
def is_ipv6(address):
    try:
        socket.inet_pton(socket.AF_INET6, address)
        return True
    except socket.error:
        return False

# 获取脚本文件名（不包含扩展名）
script_name = os.path.splitext(os.path.basename(__file__))[0]

# 要查询的域名列表，每个域名占据一行
domains = '''
icook.hk
ip.sb
japan.com
skk.moe
www.visa.com
www.visa.co.jp
www.visakorea.com
www.gco.gov.qa
www.csgo.com
www.whatismyip.com
gamer.com.tw
steamdb.info
toy-people.com
silkbook.com
cdn.anycast.eu.org
shopify.com
www.visa.com.tw
time.is
www.hugedomains.com
www.visa.com.sg
www.whoer.net
www.visa.com.hk
malaysia.com
www.ipget.net
icook.tw
www.gov.ua
www.udacity.com
www.shopify.com
singapore.com
russia.com
www.4chan.org
www.glassdoor.com
xn--b6gac.eu.org
www.digitalocean.com
www.udemy.com
cdn-all.xn--b6gac.eu.org
dnschecker.org
tasteatlas.com
pixiv.net
comicabc.com
cfip.xxxxxxxx.tk
'''

domains = domains.strip().split('\n')  # 将字符串按换行符分割成列表

# 打开文件准备追加新的IPv4地址
ipv4_file_path = 'GFYMIP.txt'

# 打开文件准备追加新的IPv6地址
ipv6_file_path = 'GFYMIP-IPv6.txt'

# 读取已有的IPv4地址
existing_ipsv4 = set()
if os.path.exists(ipv4_file_path):
    with open(ipv4_file_path, 'r') as ipv4_file:
        for line in ipv4_file:
            existing_ipsv4.add(line.strip())

# 读取已有的IPv6地址
existing_ipsv6 = set()
if os.path.exists(ipv6_file_path):
    with open(ipv6_file_path, 'r') as ipv6_file:
        for line in ipv6_file:
            existing_ipsv6.add(line.strip())

# 打开文件准备追加新的IPv4地址，如果文件不存在则创建
with open(ipv4_file_path, 'a+') as ipv4_file:
    for domain in domains:
        try:
            # 获取完整的DNS解析结果
            result = socket.getaddrinfo(domain, None)
            ipsv4 = set([x[-1][0] for x in result if is_ipv4(x[-1][0])])  # 提取IPv4地址并去重
            ipsv6 = set([x[-1][0] for x in result if is_ipv6(x[-1][0])])  # 提取IPv6地址并去重

            for ip in ipsv4:
                if ip not in existing_ipsv4:
                    ipv4_file.write(ip + '\n')
                    print(f'{domain} - {ip} added to IPv4 file')

            for ip in ipsv6:
                if ip not in existing_ipsv6:
                    with open(ipv6_file_path, 'a+') as ipv6_file:
                        ipv6_file.write(ip + '\n')
                        print(f'{domain} - {ip} added to IPv6 file')
        except (socket.gaierror, socket.herror) as e:
            print(f'Failed to resolve {domain}: {e}')

print('新的IPv4地址追加完成。')
print('新的IPv6地址追加完成。')

messagebox.showinfo("信息", "获取官方域名IP完成")

root = Tk()
app = Application(root)
root.mainloop()
