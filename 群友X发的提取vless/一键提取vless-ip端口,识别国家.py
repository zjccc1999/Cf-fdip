# 提示用户将vless节点复制保存到cf-vless.txt文件中，然后回车才能执行脚本
print("请将vless节点复制保存到cf-vless.txt文件中，按下回车键执行脚本。")
input("按下回车键继续...")

import os
import re
import geoip2.database

def process_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = file.read()

            ipv4_set = set()
            ipv6_set = set()
            domain_set = set()

            ip_pattern = r'(\[?[0-9a-fA-F:]+\]?|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|[a-zA-Z0-9.-]+):(\d{1,5})'
            matches = re.findall(ip_pattern, data)

            for match in matches:
                ip = match[0]
                port = match[1]
                if ':' in ip:  # IPv6
                    ipv6_set.add(f"{ip}:{port}")
                elif '.' in ip:  # IPv4
                    ipv4_set.add(f"{ip}:{port}")
                else:  # Domain
                    domain_set.add(f"{ip}:{port}")

            reader = geoip2.database.Reader('GeoLite2-Country.mmdb')
            country_ip_map = {}
            port_ip_map = {}

            for ip_port in ipv4_set.union(ipv6_set):
                ip = ip_port.split(':')[0]
                try:
                    response = reader.country(ip)
                    country_code = response.country.iso_code
                    if ':' in ip_port:
                        if country_code not in port_ip_map:
                            port_ip_map[country_code] = []
                        port_ip_map[country_code].append(ip_port)
                    else:
                        if country_code not in country_ip_map:
                            country_ip_map[country_code] = []
                        country_ip_map[country_code].append(ip_port)
                except:
                    pass

            output_folder = os.path.dirname(file_path)

            for country_code, ips in country_ip_map.items():
                output_filename = os.path.join(output_folder, f'{country_code}.txt')
                with open(output_filename, 'a') as output_file:
                    for ip_port in ips:
                        output_file.write(f'{ip_port}\n')

            for country_code, ips in port_ip_map.items():
                port_output_folder = os.path.join(output_folder, f'{os.path.splitext(os.path.basename(file_path))[0]}+端口版')
                os.makedirs(port_output_folder, exist_ok=True)
                output_filename = os.path.join(port_output_folder, f'{country_code}.txt')
                with open(output_filename, 'a') as output_file:
                    for ip_port in ips:
                        output_file.write(f'{ip_port}\n')

            reader.close()

        print(f"处理文件 {os.path.basename(file_path)} 完成！")
    else:
        print(f"文件 {os.path.basename(file_path)} 不存在！")

# 指定处理的文件为 cf-vless.txt
file_path = 'cf-vless.txt'
process_file(file_path)
