# 1. Linux / iStoreOS / N1 专用
## 🚀 iStoreOS/N1 Cloudflare 测速脚本（Linux 版）

**自动更新 cfst + 下载走代理 + 测速强制直连 + 仅延迟不带速度**

---

## ✨ 主要功能

- 自动获取最新 cfst 版本（支持 `--force-update`）
- 下载走 `proxy.txt`，测速强制直连
- 默认仅测延迟：`best_ip.txt` 格式为 `IP#地区`（如 `172.64.153.129#US`）
- `--full-speed` 可测下载速度
- 支持 GitHub 自动上传 + Telegram 通知
- heapq 性能优化，适合 N1 / OpenWrt 长期运行

---

## 📁 文件说明
cfst/

├── cfst.py                  ← 主脚本（直接运行）

├── proxy.txt                ← 代理（可选）

├── github.txt               ← GitHub 配置（可选）

├── tg.txt                   ← Telegram 配置（可选）

├── best_ip.txt              ← 最终结果

└── .cfst_cache/             ← 缓存目录



---

## ⚙️ 配置（三个 txt 文件）
## 选填 非必须
**proxy.txt**（国内用户必填）

http://127.0.0.1:7890

**github.txt**

GH_REPO=zjccc1999/Cf-fdip（用户名/仓库名）

GH_TOKEN=github_pat_xxxxxxxxxxxx（rope权限）

GH_USERNAME=zjccc1999（用户名）

GH_EMAIL=邮箱

# 推荐命令
`python3 cfst.py   `                 # 只测延迟（最快）

`python3 cfst.py --full-speed`       # 完整测速

`python3 cfst.py --force-update`     # 强制更新 cfst

📊 输出示例
仅延迟模式（默认）：

*172.64.153.129#US*

*104.16.124.96#US*


## 🪟 使用方法（超简单）

命令,含义,推荐场景
python cfst.py,默认：只测延迟（最快）,日常快速更新节点
python cfst.py --full-speed,完整测速（速度≥30MB/s，每个国家独立前10）,需要高速度节点时
python cfst.py --full-speed --httping,最推荐：完整测速 + HTTPing（地区码最准）,追求最佳效果
python cfst.py --full-speed --min-speed 15,完整测速 + 速度≥15MB/s,想多拿点IP时
python cfst.py --full-speed --force-update,强制更新 cfst 再完整测速,第一次运行或想更新工具

可选参数说明

--full-speed：开启完整测速（默认不开启）
--httping：使用 HTTPing 模式（推荐搭配 --full-speed 使用）
--min-speed 数值：完整测速时最低下载速度（MB/s），默认 30
--force-update：强制重新下载最新 cfst
运行后生成的文件

best_ip.txt → 最终结果（带详细头部注释）
result.csv → cfst 原始结果
.cfst_cache/ → 缓存文件夹（7天后自动清理）

best_ip.txt 示例（最终格式）

# Cloudflare 测速结果 - 2025-03-01 20:30:15
# 模式: 完整测速（每个国家独立前10）
# 最低速度: ≥30 MB/s | HTTPing: 是
# 共 87 条 | 每个国家最多 10 条
# 格式: IP#机场码-速度MB/s
# ===============================================

104.21.71.51#SJC-42.94MB/s
172.67.70.174#SEA-42.15MB/s
103.21.244.56#NRT-38.25MB/s
...
# 2. Windows 专用 

1. 下载 `cfst_win.py` 到任意文件夹
2. 把 `proxy.txt`、`github.txt`、`tg.txt` 放在同一文件夹
3. **双击运行** 或 在 CMD / PowerShell 执行：

```powershell
python cfst_win.py
python cfst_win.py --full-speed
python cfst_win.py --force-update
