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
find . -type f -name "$text_file" -exec cat {} + > "$merged_file"

# 去除重复 IP
awk '!seen[$0]++' "$merged_file" > "$merged_file.unique"
mv "$merged_file.unique" "$merged_file"

# 复制合并后的文件到脚本根目录
cp "$merged_file" .
echo "文件已复制到脚本目录：$merged_file"


# 执行测试命令
echo "开始执行测试..."
if [ $choice -eq 1 ]; then
    ./CloudflareST -tp $port -f $text_file -n 200 -dn 10 -sl 10 -tl 400 -url http://cs.notls.zjccc.onflashdrive.app/200m
else
    ./CloudflareST -tp $port -f $text_file -n 200 -dn 10 -sl 10 -tl 400 -url https://cs.notls.zjccc.onflashdrive.app/200m
fi

echo "测试完成！"

