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
cd "$(dirname "$0")"

# 清除之前的 txt 目录
rm -rf txt > /dev/null 2>&1

# 询问用户是否更新本地 txt.zip 数据
read -p "是否更新本地 txt.zip 数据? (0不更新、1更新(默认)): " updatezip
if [ -z "$updatezip" ]; then
    updatezip=1
fi

# 如果用户选择更新，则从指定的 URL 下载数据文件
if [[ $updatezip -eq 1 ]]; then
    echo "正在从 https://zip.baipiao.eu.org 下载数据文件"
    curl -# https://zip.baipiao.eu.org -o txt.zip
    if [ $? -ne 0 ]; then
        echo "下载失败，请检查网络连接或手动下载并放置在本目录"
        exit 1
    fi
    echo "下载完成"
fi

# 下载完成后尝试解压
if [[ -e "txt.zip" ]]; then
    echo "正在解压下载的文件"
    unzip -o txt.zip -d txt || echo "解压失败，请检查文件是否损坏或权限不足。"
    echo "解压成功，删除原压缩包"
    rm txt.zip
else
    echo "下载文件不存在，无法解压"
fi

# 合并 txt 目录中的所有文本文件，并去除重复的IP地址
if [[ -d "txt" ]]; then
    echo "正在合并 txt 目录中的所有文本文件，并去除重复的IP地址"
    cat txt/*.txt | awk '!seen[$0]++' > zipbaipiao.txt
    echo "合并成功，文件已保存为 zipbaipiao.txt"
else
    echo "txt 目录不存在，无法合并文件"
fi

# 移动文件
if [[ -e "zipbaipiao.txt" ]]; then
    echo "正在移动文件"
    mv zipbaipiao.txt "$script_dir/" || echo "移动失败，请检查目标目录是否存在并具有足够的权限。"
    echo "移动成功"
else
    echo "文件不存在，无法移动"
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
file_path="GFYMIP.txt"

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
