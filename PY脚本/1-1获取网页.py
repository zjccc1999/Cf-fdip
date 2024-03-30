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
