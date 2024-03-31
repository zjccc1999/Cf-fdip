#!/bin/bash

# 检查是否提供了输入文件参数
if [ ! -f "cf-vless.txt" ]; then
    echo "Error: File cf-vless.txt does not exist in the current directory."
    exit 1
fi

# 使用awk读取每一行并提取第二个和第四个字段，然后使用sort和uniq进行排序和去重
awk -F'[@?#]' '{print $2"#" $4}' cf-vless.txt | sort -t '#' -u -k1,1 > vless-ip.txt

echo "Processing completed. Results are saved in vless-ip.txt."
