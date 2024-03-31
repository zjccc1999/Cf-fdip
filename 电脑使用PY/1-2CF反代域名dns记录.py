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
