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
