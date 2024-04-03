#!/bin/bash

is_ipv4() {
    local address="$1"
    if [[ $address =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        return 0
    else
        return 1
    fi
}

is_ipv6() {
    local address="$1"
    if [[ $address =~ ^[0-9a-fA-F:]+$ ]]; then
        return 0
    else
        return 1
    fi
}

# 要查询的域名列表，每个域名占据一行
domains='
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
'

# 将字符串按换行符分割成数组
IFS=$'\n' read -r -d '' -a domains_array <<< "$domains"

# 打开文件准备追加新的IPv4和IPv6地址，如果文件不存在则创建
file_path="GFYMIP.txt"
existing_ips=()

if [ -f "$file_path" ]; then
    while IFS= read -r line; do
        existing_ips+=("$line")
    done < "$file_path"
fi

# 查询域名并将新的IPv4和IPv6地址追加到文件
for domain in "${domains_array[@]}"; do
    result=$(nslookup -querytype=A "$domain" | awk '/^Address: / { print $2 }')
    ipv4s=($(echo "$result" | grep -E '([0-9]{1,3}\.){3}[0-9]{1,3}'))

    for ip in "${ipv4s[@]}"; do
        if ! [[ " ${existing_ips[@]} " =~ " $ip " ]]; then
            echo "$ip" >> "$file_path"
            echo "$domain - $ip (IPv4) added to file"
        fi
    done

    result=$(nslookup -querytype=AAAA "$domain" | awk '/^Address: / { print $2 }')
    ipv6s=($(echo "$result" | grep -E '([0-9a-fA-F:]+)' | grep -v '^$'))

    for ip in "${ipv6s[@]}"; do
        if ! [[ " ${existing_ips[@]} " =~ " $ip " ]]; then
            echo "$ip" >> "$file_path"
            echo "$domain - $ip (IPv6) added to file"
        fi
    done
done

echo "新的IPv4和IPv6地址追加完成。"
