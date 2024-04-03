#!/bin/sh

is_ipv4() {
    address="\$1"
    if echo "$address" | grep -Eq '^([0-9]{1,3}\.){3}[0-9]{1,3}$'; then
        return 0
    else
        return 1
    fi
}

# 要查询的域名列表，每个域名占据一行
domains="
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
qq.achen.link
cf.akaagiao.link
jp.anxray.top.cdn.cloudflare.net
cf.ts7575.top
yx.blessbai.tech
bestproxy.wcccc.fun
www.xfltd.top
1.achen.link
cf.flyff.eu.org
ak.永遠的神b.link
"

# 将字符串按换行符分割成数组
IFS=$'\n' read -r -d '' -a domains_array <<< "$domains"

# 打开文件准备追加新的IPv4地址
file_path="FDYMIP.txt"

# 读取已有的IP地址
existing_ips=()
if [ -f "$file_path" ]; then
    while IFS= read -r line; do
        existing_ips+=("$line")
    done < "$file_path"
fi

# 打开文件准备追加新的IPv4地址，如果文件不存在则创建
for domain in "${domains_array[@]}"; do
    result=$(dig +short "$domain" | grep -E '([0-9]{1,3}\.){3}[0-9]{1,3}')
    ips=($(echo "$result" | tr ' ' '\n' | sort -u))

    for ip in "${ips[@]}"; do
        if ! [[ " ${existing_ips[@]} " =~ " $ip " ]]; then
            echo "$ip"
            existing_ips+=("$ip")
        fi
    done
done >> "$file_path"

echo "新的IPv4地址追加完成。"
