1. Linux / iStoreOS / N1 专用
# 🚀 iStoreOS/N1 Cloudflare 测速脚本（Linux 版）

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

**proxy.txt**（国内用户必填）

http://127.0.0.1:7890

**github.txt**

GH_REPO=用户名/仓库名

GH_TOKEN=github_pat_xxxxxxxxxxxx

# 推荐命令
python3 cfst.py                    # 只测延迟（最快）
python3 cfst.py --full-speed       # 完整测速
python3 cfst.py --force-update     # 强制更新 cfst

📊 输出示例
仅延迟模式（默认）：

text172.64.153.129#US

104.16.124.96#US


## 🪟 使用方法（超简单）


### **2. Windows 专用 README.md**

1. 下载 `cfst_win.py` 到任意文件夹
2. 把 `proxy.txt`、`github.txt`、`tg.txt` 放在同一文件夹
3. **双击运行** 或 在 CMD / PowerShell 执行：

```powershell
python cfst_win.py
python cfst_win.py --full-speed
python cfst_win.py --force-update
