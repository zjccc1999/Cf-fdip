# iStoreOS/N1 Cloudflare 测速脚本
一键自动化测速优选 Cloudflare IP，支持**仅延迟测试**和**完整速度测速**，自动生成最优IP列表，可同步GitHub、推送Telegram，适配iStoreOS/N1软路由

## ✨ 核心特性
- 双模式：默认**仅测延迟**（快速）、`--full-speed`**完整测速**（带下载速度）
- 自动匹配架构、下载最新cfst工具、更新IP段
- 优选规则：仅保留指定地区IP，按延迟/速度排序输出
- 扩展功能：支持代理、GitHub自动同步结果、Telegram通知
- 纯Python脚本，开箱即用，适配软路由轻量化运行

## 加速地址 `https://hub.glowp.xyz/https://raw.githubusercontent.com/zjccc1999/Cf-fdip/main/best_ip.txt`
## 📦 依赖安装
脚本仅需1个第三方库，执行以下命令安装：
```bash
pip3 install colorama
```
- 若软路由无`pip`，先执行：`opkg update && opkg install python3-pip`
- 离线环境：手动安装`colorama`库即可

## 🚀 使用方法
### 1. 基础运行（默认：仅延迟测试）
```bash
python3 cfst.py
```
- 自动测速并保留**前10条低延迟IP**
- 输出格式：`IP#cf-延迟ms`
- 结果保存：`best_ip.txt`

### 2. 完整测速模式（含下载速度）
```bash
python3 cfst.py --full-speed
```
- 每个优先地区最多保留**10条优质IP**
- 丢弃未识别地区IP
- 输出格式：`IP#地区码-速度MB/s`

### 3. 强制更新cfst工具
```bash
python3 cfst.py --force-update
```

### 4. 组合使用
```bash
# 完整测速 + 强制更新工具
python3 cfst.py --full-speed --force-update
```

## ⚙️ 自定义参数
直接编辑脚本中 `__init__` 函数内的 `self.default_args` 即可修改测速参数：
```python
self.default_args = [
    "-n",  "100",   # 测试IP数量
    "-t",  "2",     # 测速线程
    "-dn", "5",     # 下载测试数
    "-sl", "5",     # 最低保留速度(MB/s)
    "-tl", "400",   # 最高允许延迟(ms)
]
```

## 🔌 扩展配置
在脚本同目录创建以下文件实现高级功能：
1. `proxy.txt`：写入代理地址（如`http://192.168.1.1:7890`） 
2. `github.txt`：配置GitHub自动同步
3. `tg.txt`：配置Telegram通知推送

## 📝 输出说明
- 测速完成自动生成 `best_ip.txt` 最优IP文件
- 仅延迟模式：按延迟升序排列
- 完整测速模式：按速度降序排列，优先JP/SG/HK/US/KR等地区
