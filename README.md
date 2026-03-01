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


##
默认参数: -n 200 -t 4 -dn 50 -dt 8 -tl 500 -sl 30 -p 0
按需修改
win版本在468行
N1版本在502行


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
`python cfst.py   `                 # 只测延迟（最快）

`python cfst.py --full-speed`       # 完整测速

`python cfst.py --force-update`     # 强制更新 cfst

📊 输出示例
仅延迟模式（默认）：

*172.64.153.129#US*

*104.16.124.96#US*


## 🪟 使用方法（超简单）

命令,含义,推荐场景
python cfst_win.py                    # 默认只测延迟
python cfst_win.py --full-speed       # 完整测速
python cfst_win.py --force-update     # 强制更新 cfst


可选参数说明

--full-speed：开启完整测速（默认不开启）
--min-speed 数值：完整测速时最低下载速度（MB/s），默认 30
--force-update：强制重新下载最新 cfst
运行后生成的文件

best_ip.txt → 最终结果（带详细头部注释）
result.csv → cfst 原始结果
.cfst_cache/ → 缓存文件夹（7天后自动清理）

best_ip.txt 示例（最终格式）

## Cloudflare 测速结果 - 2025-03-01 20:45:12
## 模式: 完整测速
## 测速参数: -n 200 -t 4 -dn 50 -dt 8 -sl 30 -tl 500 -p 30 -o result.csv
## 最低速度: ≥30 MB/s
## 延迟上限: ≤500 ms
## 共 78 条 | 每个国家最多 10 条
## 格式: IP#机场码-速度MB/s
## ===============================================

## === JP ===
103.21.244.56#NRT-48.75MB/s
103.21.245.12#NRT-46.82MB/s
103.22.200.10#NRT-44.31MB/s
103.21.243.89#NRT-42.67MB/s
103.22.201.45#NRT-41.05MB/s
103.21.246.33#NRT-39.88MB/s
103.22.202.77#NRT-38.12MB/s
103.21.247.22#NRT-36.94MB/s
103.22.203.11#NRT-35.67MB/s
103.21.248.55#NRT-34.21MB/s

## === SG ===
103.4.31.123#SIN-52.34MB/s
103.4.30.89#SIN-50.12MB/s
103.4.29.45#SIN-48.76MB/s
103.4.28.67#SIN-47.33MB/s
103.4.27.12#SIN-45.89MB/s
103.4.26.78#SIN-44.21MB/s
103.4.25.34#SIN-42.67MB/s
103.4.24.90#SIN-41.05MB/s
103.4.23.56#SIN-39.88MB/s
103.4.22.11#SIN-38.12MB/s

## === HK ===
190.93.114.10#HKG-49.67MB/s
190.93.113.45#HKG-47.82MB/s
188.114.99.22#HKG-46.15MB/s
190.93.112.78#HKG-44.33MB/s
188.114.98.34#HKG-42.67MB/s
190.93.111.90#HKG-41.05MB/s
188.114.97.56#HKG-39.88MB/s
190.93.110.12#HKG-38.12MB/s
188.114.96.67#HKG-36.94MB/s
190.93.109.33#HKG-35.67MB/s

## === US ===
104.21.71.51#SJC-55.23MB/s
172.67.70.174#SEA-53.87MB/s
104.21.84.2#SJC-52.41MB/s
172.67.214.105#SEA-51.09MB/s
104.21.67.223#SJC-49.76MB/s
172.67.68.90#SEA-48.33MB/s
104.21.35.195#SJC-47.12MB/s
172.67.69.45#SEA-45.89MB/s
104.21.44.21#SJC-44.67MB/s
172.67.71.12#SEA-43.21MB/s

## === KR ===
103.22.200.10#ICN-46.78MB/s
103.22.201.45#ICN-45.12MB/s
...（其他国家类似分组）

# 2. Windows 专用 

1. 下载 `cfst_win.py` 到任意文件夹
2. 把 `proxy.txt`、`github.txt`、`tg.txt` 放在同一文件夹
3. **双击运行** 或 在 CMD / PowerShell 执行：

```powershell
python cfst_win.py
python cfst_win.py --full-speed
python cfst_win.py --force-update
