#!/bin/bash

# 欢迎语
echo "一起白嫖吧！"
# 获取当前工作目录
current_dir=$(pwd)

# 定义检查网络连通性的函数
check_network_access() {
    url=\$1
    if curl --output /dev/null --silent --head --fail "$url"; then
        return 0
    else
        return 1
    fi
}

# 第一个功能：下载文件并处理
function1() {
    url="https://zip.baipiao.eu.org/"
    echo "正在下载文件，请稍候..."

    if check_network_access "$url"; then
        curl -L "$url" -o "${current_dir}/txt.zip"

        if unzip -t "${current_dir}/txt.zip" &>/dev/null; then
            unzip -q "${current_dir}/txt.zip" -d "${current_dir}/txt"
            cat ${current_dir}/txt/*.txt > ${current_dir}/zipbaipiao.txt
            mv ${current_dir}/zipbaipiao.txt ${current_dir}/zipbaipiao.txt
            rm ${current_dir}/txt.zip
            rm -rf ${current_dir}/txt

            echo "文件下载、解压、合并和移动完成。"
        else
            echo "下载的文件不是一个有效的ZIP文件。"
        fi
    else
        echo "无法访问指定网页。如果无法打开，请尝试使用代理。还是不行用别的shell获取IP"
        exit 1
    fi
}

# 第二个功能：获取IP地址并追加到文件
function2() {
    url="https://ipdb.api.030101.xyz/?type=proxy"
    file_path="ipdb.txt"

    ip_addresses=$(curl -s "$url" | grep -oE "\b([0-9]{1,3}\.){3}[0-9]{1,3}\b")

    if [ -f "$file_path" ]; then
        echo "文件已存在，追加新的IP地址到文件中..."
    else
        echo "文件不存在，创建文件..."
        touch "$file_path"
    fi

    for ip in $ip_addresses; do
        if ! grep -q "$ip" "$file_path"; then
            echo "$ip" >> "$file_path"
            echo "追加新的IP地址到文件中： $ip"
        else
            echo "IP地址已存在，跳过： $ip"
        fi
    done

    echo "IP地址已更新到 $file_path 文件。"
}

# 第三个功能：查询反代域名的IPv4地址并追加到文件
function3() {
    # 第三个脚本内容
    # 函数用于检查是否为IPv4地址
is_ipv4() {
    address=\$1
    if [[ $address =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        return 0
    else
        return 1
    fi
}

# 要查询的域名列表，每个域名占据一行
domains='
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
ak.yydsb.link
'

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
            echo "$ip" >> "$file_path"
            echo "$domain - $ip added to file"
        fi
    done
done

echo "新的IPv4地址追加完成。"

}

# 第四个功能：查询官方域名的IPv4地址并追加到文件
function4() {
    # 第四个脚本内容
    # 函数用于检查是否为IPv4地址
is_ipv4() {
    address=\$1
    if [[ $address =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
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
            echo "$ip" >> "$file_path"
            echo "$domain - $ip added to file"
        fi
    done
done

echo "新的IPv4地址追加完成。"
}

# 主菜单
while true; do
    echo "请选择一个选项:"
    echo "1. zip.baipiao"
    echo "2. ipdb"
    echo "3. fdym"
    echo "4. gfym"
    echo "5. Exit"

    read -p "选择吧，推荐第二个: " choice

    case $choice in
        1) function1 ;;
        2) function2 ;;
        3) function3 ;;
        4) function4 ;;
       5) echo "退出程序。再见！"; break ;;
        *) echo "无效的选择。请重新选择一个有效的选项。" ;;
    esac
done
