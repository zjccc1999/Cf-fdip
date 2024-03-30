#!/bin/bash

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

# 定义要访问的网页 URL
url="https://zip.baipiao.eu.org/"

# 显示提示信息
echo "正在下载文件，请稍候..."

# 判断当前网络是否能够正常访问网页
if check_network_access "$url"; then
    curl -L "$url" -o "${current_dir}/txt.zip"
else
    echo "无法访问指定网页。如果无法打开，请尝试使用代理。还是不行用别的shell获取IP"
    exit 1
fi

# 检查文件是否为ZIP文件
if ! unzip -t "${current_dir}/txt.zip" &>/dev/null; then
    echo "下载的文件不是一个有效的ZIP文件。"
else
    # 解压文件到txt文件夹
    unzip -q "${current_dir}/txt.zip" -d "${current_dir}/txt"

    # 合并所有文本文件为一个文件
    cat ${current_dir}/txt/*.txt > ${current_dir}/zipbaipiao.txt

    # 移动文件到脚本目录
    mv ${current_dir}/zipbaipiao.txt ${current_dir}/zipbaipiao.txt

    # 删除原始压缩文件和解压后的文件夹
    rm ${current_dir}/txt.zip
    rm -rf ${current_dir}/txt

    echo "文件下载、解压、合并和移动完成。"
fi

# 删除txt.zip文件
if [ -f "${current_dir}/txt.zip" ]; then
    rm ${current_dir}/txt.zip
    echo "已删除txt.zip文件。"
fi
