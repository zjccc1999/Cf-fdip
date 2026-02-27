#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows Cloudflare 测速脚本 - 最终版
"""

import os
import sys
import csv
import json
import shutil
import zipfile
import urllib.request
import subprocess
import platform
from pathlib import Path
import time
from datetime import datetime
import base64
import argparse
import heapq


class CloudflareSpeedTestWindows:
    def __init__(self):
        self.start_time = time.time()
        self.base_dir = Path(__file__).parent.resolve()
        self.work_dir = self.base_dir / ".cfst_cache"
        self.setup_directories()

        self.config = {
            'max_per_region': 10,
            'max_total': 100,
            'priority_regions': ["JP", "SG", "HK", "US", "KR", "GB", "IN"],
            'cfst_args': "-n 200 -t 4 -dd -p 0 -o result.csv",
            'ip_txt_url': "https://raw.githubusercontent.com/XIU2/CloudflareSpeedTest/master/ip.txt",
            'proxy': '',
            'GH_REPO': None,
            'GH_TOKEN': None,
            'GH_USERNAME': None,
            'GH_EMAIL': None,
            'TG_BOT_TOKEN': None,
            'TG_CHAT_ID': None
        }

        parser = argparse.ArgumentParser(description="Windows Cloudflare 测速脚本")
        parser.add_argument('--full-speed', action='store_true', help="启用完整测速（带速度）")
        parser.add_argument('--force-update', action='store_true', help="强制更新 cfst")
        args = parser.parse_args()

        self.full_speed = args.full_speed
        self.force_update = args.force_update

        if self.full_speed:
            self.config['cfst_args'] = "-n 200 -t 4 -dn 100 -dt 8 -p 0 -o result.csv"
            print("✅ 已切换为完整测速模式（只保留有速度的IP，并按速度降序）")
        else:
            print("✅ 当前模式：仅延迟测试（best_ip.txt 不带速度）")

        self.opener = self._get_urllib_opener()
        self.has_proxy = False
        self.has_github = False
        self.has_telegram = False

        self.load_proxy()
        self.load_github_config()
        self.load_telegram_config()

    # ==================== 以下方法与之前完全一致（省略重复代码）===================
    # load_proxy, load_github_config, load_telegram_config, setup_directories,
    # _get_urllib_opener, get_latest_cfst_version, get_cfst_url, download_file,
    # extract_archive, find_cfst_binary, check_cfst_executable, run_speed_test,
    # get_region_for_ip, ensure_ip_txt, prepare_cfst_binary, process_results,
    # upload_to_github, send_telegram_notification, run, print_summary

    def load_proxy(self):
        f = self.base_dir / "proxy.txt"
        if f.exists():
            p = f.read_text(encoding='utf-8').strip()
            if p:
                self.config['proxy'] = p
                self.has_proxy = True
                print(f"✅ 已加载代理: {p}")

    def load_github_config(self):
        f = self.base_dir / "github.txt"
        if f.exists():
            for line in f.read_text(encoding='utf-8').splitlines():
                line = line.strip()
                if '=' in line and not line.startswith('#'):
                    k, v = line.split('=', 1)
                    key = k.strip()
                    if key in self.config:
                        self.config[key] = v.strip()
            if self.config.get('GH_TOKEN') and self.config.get('GH_REPO'):
                self.has_github = True
                print(f"✅ GitHub 配置已加载: {self.config['GH_REPO']}")

    def load_telegram_config(self):
        f = self.base_dir / "tg.txt"
        if f.exists():
            for line in f.read_text(encoding='utf-8').splitlines():
                line = line.strip()
                if '=' in line and not line.startswith('#'):
                    k, v = line.split('=', 1)
                    key = k.strip()
                    if key in self.config:
                        self.config[key] = v.strip()
            if self.config.get('TG_BOT_TOKEN') and self.config.get('TG_CHAT_ID'):
                self.has_telegram = True
                print("✅ Telegram 配置已加载")

    def setup_directories(self):
        self.work_dir.mkdir(parents=True, exist_ok=True)
        (self.work_dir / "bin").mkdir(parents=True, exist_ok=True)

    def _get_urllib_opener(self):
        opener = urllib.request.build_opener()
        if self.config.get('proxy'):
            try:
                ph = urllib.request.ProxyHandler({'http': self.config['proxy'], 'https': self.config['proxy']})
                opener = urllib.request.build_opener(ph)
            except:
                pass
        return opener

    def get_latest_cfst_version(self):
        cache = self.work_dir / "latest_version.cache"
        if not self.force_update and cache.exists():
            try:
                v, ts = cache.read_text(encoding='utf-8').strip().split('|')
                if time.time() - float(ts) < 86400:
                    print(f"✅ 使用缓存最新版本: {v}")
                    return v
            except:
                pass
        print("🔍 检查 cfst 最新版本...")
        try:
            req = urllib.request.Request("https://api.github.com/repos/XIU2/CloudflareSpeedTest/releases/latest",
                                       headers={"User-Agent": "iStoreOS-CFST/1.0"})
            with self.opener.open(req, timeout=15) as r:
                v = json.loads(r.read().decode())['tag_name']
            cache.write_text(f"{v}|{time.time()}", encoding='utf-8')
            print(f"✅ 最新 cfst 版本: {v}")
            return v
        except:
            print("⚠️ 使用稳定版 v2.3.4")
            return "v2.3.4"

    def get_cfst_url(self):
        v = self.get_latest_cfst_version()
        url = f"https://github.com/XIU2/CloudflareSpeedTest/releases/download/{v}/cfst_windows_amd64.zip"
        print(f"📥 将使用 Windows cfst {v}")
        return url, v

    def download_file(self, url: str, dst: Path, max_retries=2) -> bool:
        print(f"正在下载: {url.split('/')[-1]}（走代理）")
        dst.parent.mkdir(parents=True, exist_ok=True)
        temp = dst.with_suffix(dst.suffix + '.part')
        for attempt in range(max_retries + 1):
            try:
                headers = {"User-Agent": "iStoreOS-CFST/1.0"}
                downloaded = temp.stat().st_size if temp.exists() else 0
                if downloaded:
                    headers['Range'] = f'bytes={downloaded}-'
                req = urllib.request.Request(url, headers=headers)
                with self.opener.open(req, timeout=80) as r:
                    with open(temp, 'ab' if downloaded else 'wb') as f:
                        shutil.copyfileobj(r, f, length=128 * 1024)
                temp.rename(dst)
                print(f"✅ 下载完成 ({dst.stat().st_size // 1024:,} KB)")
                return True
            except Exception as e:
                print(f"⚠️ 下载失败 (尝试 {attempt+1}): {e}")
                if attempt == max_retries:
                    return False
                time.sleep(2)
        return False

    def extract_archive(self, archive: Path, out_dir: Path) -> bool:
        out_dir.mkdir(parents=True, exist_ok=True)
        try:
            print(f"解压: {archive.name}")
            with zipfile.ZipFile(archive) as z:
                z.extractall(out_dir)
            print("✅ 解压完成")
            return True
        except Exception as e:
            print(f"❌ 解压失败: {e}")
            return False

    def find_cfst_binary(self, bin_dir: Path) -> Path:
        for p in bin_dir.rglob("cfst.exe"):
            if p.is_file():
                return p
        raise FileNotFoundError("未找到 cfst.exe")

    def check_cfst_executable(self, cfst_path: Path) -> bool:
        cache = self.work_dir / "cfst_verified.cache"
        if cache.exists() and (time.time() - cache.stat().st_mtime < 86400):
            print("✅ cfst 已验证（缓存）")
            return True
        try:
            r = subprocess.run([str(cfst_path), "--version"], capture_output=True, text=True, encoding='utf-8', errors='ignore', timeout=8)
            if r.returncode == 0:
                cache.touch()
                print(f"✅ cfst 验证通过: {r.stdout.strip()}")
                return True
        except:
            pass
        return False

    def run_speed_test(self, cfst_bin: Path) -> bool:
        print("🚀 开始 Cloudflare 测速...（强制直连）")
        cmd = [str(cfst_bin)] + self.config['cfst_args'].split()
        env = os.environ.copy()
        for v in ['http_proxy', 'https_proxy', 'HTTP_PROXY', 'HTTPS_PROXY', 'all_proxy', 'ALL_PROXY']:
            env.pop(v, None)
        try:
            subprocess.run(cmd, cwd=self.base_dir, env=env, check=True)
            return True
        except:
            return False

    def get_region_for_ip(self, ip: str) -> str:
        parts = ip.split('.')
        if len(parts) < 2: return "Other"
        a, b = int(parts[0]), int(parts[1])
        if a == 103 and b in [21, 22]: return "JP"
        if a == 103 and b in [4, 31]: return "SG"
        if a in [190, 188] and b in [93, 114]: return "HK"
        if a == 104 and 16 <= b <= 31 or a == 172 and 64 <= b <= 71: return "US"
        if a == 103 and b in [22, 23]: return "KR"
        if a == 141 and b == 101: return "GB"
        if a == 197 and b == 234: return "IN"
        return "Other"

    # ====================== 核心修改部分 ======================
    def parse_top_ips_by_region(self, csv_path: Path) -> list[str]:
        if not self.full_speed:
            # 仅延迟模式：按延迟升序（保持不变）
            return self._parse_latency_mode(csv_path)

        # ==================== 完整测速模式 ====================
        # 只保留有速度的IP，并按速度降序
        ip_list = []
        try:
            with open(csv_path, "r", encoding="utf-8", newline="") as f:
                next(csv.reader(f), None)
                for row in csv.reader(f):
                    if len(row) < 6 or not row[0].strip():
                        continue
                    ip = row[0].strip()
                    try:
                        speed = float(row[5])
                    except:
                        continue
                    if speed <= 0:          # 过滤掉没有速度的
                        continue
                    region = self.get_region_for_ip(ip)
                    ip_list.append((speed, ip, region))
        except Exception as e:
            print(f"❌ CSV 解析失败: {e}")

        # 按速度降序排序
        ip_list.sort(reverse=True)   # 先按 speed 降序

        # 按地区优先级筛选（每个地区最多 max_per_region 个）
        selected = []
        region_count = {r: 0 for r in self.config['priority_regions']}

        for speed, ip, region in ip_list:
            if region in region_count and region_count[region] < self.config['max_per_region']:
                selected.append(f"{ip}#{region}-{speed:.2f}")
                region_count[region] += 1
            if len(selected) >= self.config['max_total']:
                break

        return selected

    def _parse_latency_mode(self, csv_path: Path) -> list[str]:
        # 仅延迟模式的原始逻辑
        region_heaps = {r: [] for r in self.config['priority_regions']}
        try:
            with open(csv_path, "r", encoding="utf-8", newline="") as f:
                next(csv.reader(f), None)
                for row in csv.reader(f):
                    if len(row) < 5 or not row[0].strip(): continue
                    ip = row[0].strip()
                    latency = float(row[4]) if row[4].strip() else 9999.0
                    region = self.get_region_for_ip(ip)
                    if region in region_heaps:
                        item = (latency, 0.0, ip, region)
                        h = region_heaps[region]
                        if len(h) < self.config['max_per_region']:
                            heapq.heappush(h, item)
                        elif item[0] < h[0][0]:
                            heapq.heappushpop(h, item)
        except:
            pass

        selected = []
        for region, heap in region_heaps.items():
            for _, _, ip, reg in sorted(heap):
                selected.append(f"{ip}#{reg}")
        return selected[:self.config['max_total']]

    # ====================== 其余方法保持不变 ======================
    def ensure_ip_txt(self) -> bool:
        p = self.base_dir / "ip.txt"
        if p.exists():
            print("✅ ip.txt 已存在")
            return True
        return self.download_file(self.config['ip_txt_url'], p)

    def prepare_cfst_binary(self):
        url, version = self.get_cfst_url()
        filename = url.split('/')[-1]
        archive = self.work_dir / filename
        bin_dir = self.work_dir / "bin"

        if (bin_dir / "cfst.exe").exists() and not self.force_update:
            try:
                r = subprocess.run([str(bin_dir / "cfst.exe"), "--version"],
                                 capture_output=True, text=True, encoding='utf-8', errors='ignore', timeout=5)
                if version in r.stdout + r.stderr:
                    print(f"✅ 已为最新版 cfst {version}")
                    return bin_dir / "cfst.exe"
            except:
                pass

        print(f"📥 准备 cfst {version}...")
        if not archive.exists() or self.force_update:
            if not self.download_file(url, archive):
                return None

        if bin_dir.exists():
            shutil.rmtree(bin_dir)
        if not self.extract_archive(archive, bin_dir):
            return None

        try:
            cfst_bin = self.find_cfst_binary(bin_dir)
            return cfst_bin if self.check_cfst_executable(cfst_bin) else None
        except Exception as e:
            print(f"❌ cfst 准备失败: {e}")
            return None

    def process_results(self) -> bool:
        csv_path = self.base_dir / "result.csv"
        if not csv_path.exists():
            print("❌ result.csv 未找到")
            return False
        ips = self.parse_top_ips_by_region(csv_path)
        if not ips:
            print("⚠️ 未找到有效IP")
            return False
        (self.base_dir / "best_ip.txt").write_text("\n".join(ips) + "\n", encoding="utf-8")
        print(f"✅ 已提取 {len(ips)} 个最优IP")
        return True

    # upload_to_github、send_telegram_notification、run、print_summary 与之前一致
    def upload_to_github(self) -> bool:
        if not self.has_github: return False
        best = self.base_dir / "best_ip.txt"
        if not best.exists(): return False
        print(f"上传到 GitHub: {self.config['GH_REPO']}（走代理）")
        try:
            content = base64.b64encode(best.read_bytes()).decode('utf-8')
            api_url = f"https://api.github.com/repos/{self.config['GH_REPO']}/contents/best_ip.txt"
            opener = self.opener
            sha = None
            req = urllib.request.Request(api_url, method='GET')
            req.add_header('Authorization', f'token {self.config["GH_TOKEN"]}')
            req.add_header('Accept', 'application/vnd.github.v3+json')
            req.add_header('User-Agent', 'iStoreOS-CFST/1.0')
            try:
                with opener.open(req) as resp:
                    if resp.status == 200:
                        sha = json.loads(resp.read().decode())['sha']
            except urllib.error.HTTPError as e:
                if e.code != 404: raise

            data = {"message": "Update best_ip.txt", "content": content}
            if self.config.get('GH_USERNAME') or self.config.get('GH_EMAIL'):
                data["committer"] = {
                    "name": self.config.get('GH_USERNAME', 'CFST-Bot'),
                    "email": self.config.get('GH_EMAIL', 'cfst-bot@noreply.github.com')
                }
            if sha: data["sha"] = sha

            req = urllib.request.Request(api_url, data=json.dumps(data).encode(), method='PUT')
            req.add_header('Authorization', f'token {self.config["GH_TOKEN"]}')
            req.add_header('Accept', 'application/vnd.github.v3+json')
            req.add_header('Content-Type', 'application/json')
            req.add_header('User-Agent', 'iStoreOS-CFST/1.0')

            with opener.open(req) as resp:
                if resp.status in (200, 201):
                    print("✅ GitHub 上传成功")
                    return True
        except Exception as e:
            print(f"❌ GitHub 上传失败: {e}")
        return False

    def send_telegram_notification(self, message: str):
        if not self.has_telegram: return
        url = f"https://api.telegram.org/bot{self.config['TG_BOT_TOKEN']}/sendMessage"
        data = {"chat_id": self.config['TG_CHAT_ID'], "text": message, "parse_mode": "HTML"}
        try:
            req = urllib.request.Request(url, data=json.dumps(data).encode(), headers={'Content-Type': 'application/json'})
            with self.opener.open(req, timeout=15) as resp:
                if resp.status == 200:
                    print("✅ Telegram 通知已发送")
        except Exception as e:
            print(f"⚠️ Telegram 发送失败: {e}")

    def run(self) -> bool:
        print("=" * 80)
        print("🚀 Windows Cloudflare 测速脚本 [最终版]")
        print(f"系统: {platform.machine()} | Python: {platform.python_version()}")
        print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        if self.force_update: print("⚡ 强制更新模式")
        print("=" * 80)

        if not self.ensure_ip_txt(): return False
        cfst_bin = self.prepare_cfst_binary()
        if not cfst_bin: return False
        if not self.run_speed_test(cfst_bin): return False
        if not self.process_results(): return False

        upload_ok = self.upload_to_github()

        best_path = self.base_dir / "best_ip.txt"
        if best_path.exists():
            with open(best_path, 'r', encoding='utf-8') as f:
                ips = [line.strip() for line in f if line.strip()]

            elapsed = time.time() - self.start_time
            total_time = f"{int(elapsed//60)}分{int(elapsed%60)}秒"
            mode_str = "完整测速（按速度降序，只保留有速度的IP）" if self.full_speed else "仅延迟测试（不带速度）"

            msg = f"<b>🚀 Cloudflare 测速完成！</b>\n\n"
            msg += f"⏰ 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            msg += f"⏱ 总耗时: <b>{total_time}</b>\n"
            msg += f"📊 模式: {mode_str}\n"
            msg += f"📊 共找到 <b>{len(ips)}</b> 个最优IP\n\n"
            if ips:
                msg += "<b>🏆 前5条最优IP：</b>\n" + "\n".join([f"{i}. <code>{ip}</code>" for i, ip in enumerate(ips[:5], 1)])
            msg += f"\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            if self.config.get('GH_REPO'):
                link = f"https://github.com/{self.config['GH_REPO']}/blob/main/best_ip.txt"
                msg += f"📂 GitHub: https://github.com/{self.config['GH_REPO']}\n"
                msg += f"📄 查看结果: <a href=\"{link}\">best_ip.txt</a>\n"
            msg += "✅ 已上传 GitHub" if upload_ok else "⚠️ GitHub 上传失败"
            self.send_telegram_notification(msg)

        self.print_summary()
        return True

    def print_summary(self):
        elapsed = time.time() - self.start_time
        print("\n" + "=" * 80)
        print("🎉 任务完成！")
        print(f"总耗时: {int(elapsed//60)}分 {int(elapsed%60)}秒")
        print(f"模式: {'完整测速（按速度降序，只保留有速度的IP）' if self.full_speed else '仅延迟测试（不带速度）'}")
        print(f"最佳IP文件: {self.base_dir / 'best_ip.txt'}")
        best_path = self.base_dir / "best_ip.txt"
        if best_path.exists():
            with open(best_path) as f:
                ips = [line.strip() for line in f if line.strip()]
                print(f"最优IP数量: {len(ips)}")
                print("\n前5个最优IP:")
                for i, ip in enumerate(ips[:5], 1):
                    print(f"   {i}. {ip}")
        print("=" * 80)


def main():
    speedtest = CloudflareSpeedTestWindows()
    try:
        return 0 if speedtest.run() else 1
    except KeyboardInterrupt:
        print("\n👋 用户中断操作")
        return 130
    except Exception as e:
        print(f"❌ 未预期错误: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())