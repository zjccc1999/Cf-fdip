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
    echo "1. 读取FDYMIP.txt"
    echo "2. 读取GFYMIP.txt"
    echo "3. 读取ipdb.txt"
    echo "4. 读取zipbaipiao.txt"
    echo "5. 退出"
    
    read -p "请选择一个选项: " choice
    
    case $choice in
        1)
            file="FDYMIP.txt"
            process_ip_concurrently "$file"
            ;;
        2)
            file="GFYMIP.txt"
            process_ip_concurrently "$file"
            ;;
        3)
            file="ipdb.txt"
            process_ip_concurrently "$file"
            ;;
        4)
            file="zipbaipiao.txt"
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
