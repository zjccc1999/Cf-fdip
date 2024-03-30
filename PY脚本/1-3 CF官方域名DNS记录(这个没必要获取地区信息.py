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
file_path = 'GFYMIP.txt'

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
