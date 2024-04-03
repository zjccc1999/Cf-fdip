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

# 第一个功能：https://zip.baipiao.eu.org下载文件并处理
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
    address="$1"
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
    result=$(nslookup -querytype=A "$domain" | awk '/^Address: / { print $2 }')
    ips=($(echo "$result" | grep -E '([0-9]{1,3}\.){3}[0-9]{1,3}'))

    for ip in "${ips[@]}"; do
        if ! [[ " ${existing_ips[@]} " =~ " $ip " ]]; then
            echo "$ip"
            existing_ips+=("$ip")
        fi
    done
done >> "$file_path"

echo "新的IPv4地址追加完成。"


}

# 第四个功能：查询官方域名的IPv4地址并追加到文件
function4() {
    # 第四个脚本内容
    # 函数用于检查是否为IPv4地址
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
}

# 第五个功能：API识别国家地区
function5() {
    # 函数5的内容
    # Function to process IP addresses and save them to country-specific files
process_ip() {
    local ip=$1
    local file=$2
    local api=$3
    local country
    
    # Check if IP address has already been processed
    if grep -q "$ip" "${file%%.*}/processed_ips.txt"; then
        echo "IP地址 $ip 已经处理过，跳过处理。"
        return
    fi
    
    # Query IP address information using ipinfo.io
    if [ "$api" == "ipinfo" ]; then
        country=$(curl -s https://ipinfo.io/$ip/country)
    # Query IP address information using ipapi.com
    else
        # Get country code from ipapi.com response and convert it to abbreviation
        country_code=$(curl -s "https://ipapi.com/ip_api.php?ip=$ip" | jq -r '.country_code')
        country=$(curl -s "https://restcountries.com/v3.1/alpha?codes=$country_code" | jq -r '.[0].cca2')
    fi
    
    # Check if country information is valid
    if [ -z "$country" ]; then
        echo "查询 $ip 失败，尝试使用另一个API进行查询。"
        process_ip "$ip" "$file" "ipapi"  # Try the other API
        return
    fi
    
    echo "IP地址: $ip, 国家 ($api): $country"
    echo $ip >> "${file%%.*}/processed_ips.txt"
    echo $ip >> "${file%%.*}/$country.txt"
}

# Remove duplicate IP addresses from a file
remove_duplicates() {
    local file=$1
    awk '!seen[$0]++' "$file" > "$file.tmp" && mv "$file.tmp" "$file"
}

# Main function to process IP addresses
process_ip_concurrently() {
    local file=$1
    local api1="ipinfo"
    local api2="ipapi"
    local current_api=$api1
    local ips=( $(<"$file") )
    local ip
    local index=0
    
    mkdir -p "${file%%.*}"
    touch "${file%%.*}/processed_ips.txt"

    while [ $index -lt ${#ips[@]} ]; do
        for (( i=0; i<5 && index<${#ips[@]}; i++ )); do
            ip="${ips[index]}"
            
            # Check if IP address has already been processed
            if grep -q "$ip" "${file%%.*}/processed_ips.txt"; then
                echo "IP地址 $ip 已经处理过，跳过处理。"
                ((index++))
                continue
            fi
            
            process_ip "$ip" "$file" "$current_api" &
            ((index++))
        done
        
        if [ "$current_api" == "$api1" ]; then
            current_api=$api2
        else
            current_api=$api1
        fi
    done
    
    wait
    
    echo "查询完成！"
    
    # Remove processed_ips.txt file
    rm "${file%%.*}/processed_ips.txt"
    
    # Remove duplicate IP addresses
    remove_duplicates "$file"
}

# Main menu
while true; do
    echo "----- 选择一个选项 -----"
    echo "1. 读取zipbaipiao.txt"
    echo "2. 读取ipdb.txt"
    echo "3. 读取FDYMIP.txt"
    echo "4. 读取GFYMIP.txt"
    echo "5. 退出"
    
    read -p "请选择一个选项: " choice
    
    case $choice in
        1)
            file="zipbaipiao.txt"
            process_ip_concurrently "$file"
            ;;
        2)
            file="ipdb.txt"
            process_ip_concurrently "$file"
            ;;
        3)
            file="FDYMIP.txt"
            process_ip_concurrently "$file"
            ;;
        4)
            file="GFYMIP.txt"
            process_ip_concurrently "$file"
            ;;
        5)
            echo "退出程序."
            break
            ;;
        *)
            echo "无效选项，请重新选择."
            ;;
    esac
done

}

# 第六个功能
function6() {
    # Function to process IP addresses and save them to country-specific files
process_ip() {
    local ip=$1
    local file=$2
    local country
    
    # Check if IP address has already been processed
    if grep -q "$ip" "${file%%.*}/processed_ips.txt"; then
        echo "IP地址 $ip 已经处理过，跳过处理。"
        return
    fi
    
    # Query IP address information using GeoLite2-Country.mmdb
    country=$(mmdblookup --file ~/GeoLite2-Country.mmdb --ip "$ip" country iso_code)
    
    # Extract country code from the response
    country=$(echo "$country" | sed -n 's/^.*"\(.*\)".*$/\1/p')
    
    # Check if country information is valid
    if [ -z "$country" ]; then
        echo "查询 $ip 失败，跳过处理。"
        return
    fi
    
    echo "IP地址: $ip, 国家: $country"
    echo "$ip" >> "${file%%.*}/processed_ips.txt"
    echo "$ip" >> "${file%%.*}/$country.txt"
}

# Remove duplicate IP addresses from a file
remove_duplicates() {
    local file=$1
    awk '!seen[$0]++' "$file" > "$file.tmp" && mv "$file.tmp" "$file"
}

# Main function to process IP addresses
process_ip_concurrently() {
    local file=$1
    local ips=( $(<"$file") )
    local ip
    local index=0
    
    mkdir -p "${file%%.*}"
    touch "${file%%.*}/processed_ips.txt"

    while [ $index -lt ${#ips[@]} ]; do
        for (( i=0; i<5 && index<${#ips[@]}; i++ )); do
            ip="${ips[index]}"
            
            # Check if IP address has already been processed
            if grep -q "$ip" "${file%%.*}/processed_ips.txt"; then
                echo "IP地址 $ip 已经处理过，跳过处理。"
                ((index++))
                continue
            fi
            
            process_ip "$ip" "$file" &
            ((index++))
        done
    done
    
    wait
    
    echo "查询完成！"
    
    # Remove processed_ips.txt file
    rm "${file%%.*}/processed_ips.txt"
    
    # Remove duplicate IP addresses
    remove_duplicates "$file"
}

# Main menu
while true; do
    echo "----- 选择一个选项 -----"
    echo "1. 读取zipbaipiao.txt"
    echo "2. 读取ipdb.txt"
    echo "3. 读取FDYMIP.txt"
    echo "4. 读取GFYMIP.txt"
    echo "5. 退出"
    
    read -p "请选择一个选项: " choice
    
    case $choice in
        1)
            file="zipbaipiao.txt"
            process_ip_concurrently "$file"
            ;;
        2)
            file="ipdb.txt"
            process_ip_concurrently "$file"
            ;;
        3)
            file="FDYMIP.txt"
            process_ip_concurrently "$file"
            ;;
        4)
            file="GFYMIP.txt"
            process_ip_concurrently "$file"
            ;;
        5)
            echo "退出程序."
            break
            ;;
        *)
            echo "无效选项，请重新选择."
            ;;
    esac
done
}
# 第七个功能：测速
function7() {
    # 函数7的内容
#!/bin/bash

# 清空屏幕
clear

echo "欢迎使用越测越开心脚本！"
echo "请选择要测试的协议："
echo "1. HTTP"
echo "2. HTTPS"

read -p "请输入选项: " choice

case $choice in
    1)
        echo "您选择了 HTTP 协议"
        http_ports=("80" "8080" "8880" "2052" "2082" "2086" "2095")
        ;;
    2)
        echo "您选择了 HTTPS 协议"
        https_ports=("443" "2053" "2083" "2087" "2096" "8443")
        ;;
    *)
        echo "无效选项，退出脚本"
        exit 1
        ;;
esac

# 选择端口
if [ $choice -eq 1 ]; then
    echo "请选择一个端口进行测试："
    select port in "${http_ports[@]}"; do
        if [[ " ${http_ports[@]} " =~ " $port " ]]; then
            echo "您选择的端口是: $port"
            break
        else
            echo "无效的端口，请重新选择"
        fi
    done
else
    echo "请选择一个端口进行测试："
    select port in "${https_ports[@]}"; do
        if [[ " ${https_ports[@]} " =~ " $port " ]]; then
            echo "您选择的端口是: $port"
            break
        else
            echo "无效的端口，请重新选择"
        fi
    done
fi

# 选择文本文件
echo "请选择一个文本文件进行测试："
text_files=("HK.txt" "KR.txt" "SG.txt" "GFYMIP.txt" "TW.txt" "AE.txt" "US.txt" "DE.txt" "JP.txt" "CA.txt" "CH.txt" "GB.txt" "IN.txt" "IT.txt" "NL.txt" "BG.txt" "FR.txt" "DK.txt" "PH.txt" "SE.txt" "CN.txt" "ID.txt")
select text_file in "${text_files[@]}"; do
    if [[ " ${text_files[@]} " =~ " $text_file " ]]; then
        echo "您选择的文本文件是: $text_file"
        break
    else
        echo "无效的文本文件，请重新选择"
    fi
done

# 查找并合并同一目录及子目录下的 $text_file
merged_file="${text_file}"
if [ "$text_file" != "GFYMIP.txt" ]; then
    find . -type f -name "$text_file" -exec cat {} + > "$merged_file"
fi

# 去除重复 IP
awk '!seen[$0]++' "$merged_file" > "$merged_file.unique"
mv "$merged_file.unique" "$merged_file"

# 复制合并后的文件到脚本根目录
cp "$merged_file" .
echo "文件已复制到脚本目录：$merged_file"


# 执行测试命令
echo "开始执行测试..."
if [ $choice -eq 1 ]; then
    ./CloudflareST -tp $port -f $text_file -n 200 -dn 10 -sl 10 -tl 400 -url http://cs.notls.zjccc.onflashdrive.app/200m -dd
else
    ./CloudflareST -tp $port -f $text_file -n 200 -dn 10 -sl 10 -tl 400 -url https://cs.notls.zjccc.onflashdrive.app/200m -dd
fi

echo "测试完成！"

}

# 第八个功能：转换成txt
function8() {
    # 函数8的内容
    # 提取IP地址
ips=$(cut -d',' -f1 result.csv | tail -n +2)

# 用户自定义字符
read -p "请输入自定义字符: " custom_char

# 获取当前时间
current_time=$(date +"%Y-%m-%d_%H-%M-%S")

# 生成带时间戳的文件名
file_name="${current_time}_GS.txt"

# 定义计数器
count=1

# 将内容写入带时间戳的文件
for ip in $ips
do
    echo "$ip:${custom_char}${count}" >> "$file_name"
    ((count++))
done

echo "已生成带时间戳的文件: $file_name"

}

# 主菜单
while true; do
    echo "请选择一个选项,推荐用ipdb获取ip:"
    echo "1. zipbaipiao"
    echo "2. ipdb"
    echo "3. FDYM"
    echo "4. GFYM"
    echo "5. API识别国家"
    echo "6. 离线识别国家"
    echo "7. 测速"
    echo "8. 转txt"
    echo "9. 退出"

    read -p "选择: " choice

    case $choice in
        1) function1 ;;
        2) function2 ;;
        3) function3 ;;
        4) function4 ;;
        5) function5 ;;
        6) function6 ;;
        7) function7 ;;
        8) function8 ;;
        9) echo "退出程序。再见！"; break ;;
        *) echo "无效的选择。请重新选择一个有效的选项。" ;;
    esac
done
