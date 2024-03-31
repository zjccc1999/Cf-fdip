# Function to process IP addresses and save them to country-specific files
process_ip() {
    if [ -f "$file" ]; then
        while IFS= read -r ip; do
            # Query IP address information using an online service
            country=$(curl -s https://ipinfo.io/$ip/country)
            echo "IP地址: $ip, 国家 (ipinfo.io): $country"
            
  
            
            # Create directory based on the file name if it doesn't exist
            if [ ! -d "${file%%.*}" ]; then
                mkdir -p "${file%%.*}"
            fi
            
            # Append IP to the country-specific file
            echo $ip >> "${file%%.*}/$country.txt"
            echo $ip >> "${file%%.*}/$new_country.txt"
        done < "$file"
    else
        echo "文件 $file 不存在或是一个目录！"
    fi
}

# Global variable to store the file name
file=""

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
            process_ip
            ;;
        2)
            file="GFYMIP.txt"
            process_ip
            ;;
        3)
            file="ipdb.txt"
            process_ip
            ;;
        4)
            file="zipbaipiao.txt"
            process_ip
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
