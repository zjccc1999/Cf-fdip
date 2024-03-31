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
