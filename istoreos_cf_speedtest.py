#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
iStoreOS/N1 Cloudflare 测速脚本 - 自动更新 cfst 最终完美版
下载走代理 | 测速强制直连 | 自动获取最新 cfst | 延迟模式不带速度
"""

import os
import sys
import csv
import json
import shutil
import tarfile
import zipfile
import urllib.request
import subprocess
import platform
from pathlib import Path
import time
from datetime import datetime
import base64
import argparse


class CloudflareSpeedTestIStoreOS:
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

        parser = argparse.ArgumentParser(description="Cloudflare 测速脚本 - 自动更新 cfst")
        parser.add_argument('--full-speed', action='store_true', help="启用完整测速（带速度）")
        parser.add_argument('--force-update', action='store_true', help="强制更新 cfst 到最新版")
        args = parser.parse_args()

        self.full_speed = args.full_speed
        self.force_update = args.force_update

        if self.full_speed:
            self.config['cfst_args'] = "-n 200 -t 4 -dn 100 -dt 8 -p 0 -o result.csv"
            print("✅ 已切换为完整测速模式（延迟 + 下载速度）")
        else:
            print("✅ 当前模式：只测延迟（best_ip.txt 将不带速度）")

        self.has_proxy = False
        self.has_github = False
        self.has_telegram = False

        self.load_proxy()
        self.load_github_config()
        self.load_telegram_config()

    def load_proxy(self):
        proxy_file = self.base_dir / "proxy.txt"
        if proxy_file.exists():
            with open(proxy_file, 'r', encoding='utf-8') as f:
                proxy_str = f.read().strip()
                if proxy_str:
                    self.config['proxy'] = proxy_str
                    self.has_proxy = True
                    print(f"✅ 已加载代理: {proxy_str}")
        else:
            print("ℹ️ 未找到 proxy.txt")

    def load_github_config(self):
        gh_file = self.base_dir / "github.txt"
        if gh_file.exists():
            with open(gh_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if '=' in line and not line.startswith('#'):
                        k, v = line.split('=', 1)
                        key = k.strip()
                        if key in self.config:
                            self.config[key] = v.strip()
            if self.config.get('GH_TOKEN') and self.config.get('GH_REPO'):
                self.has_github = True
                print(f"✅ GitHub 配置已加载: {self.config['GH_REPO']}")
        else:
            print("ℹ️ 未找到 github.txt")

    def load_telegram_config(self):
        tg_file = self.base_dir / "tg.txt"
        if tg_file.exists():
            with open(tg_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if '=' in line and not line.startswith('#'):
                        k, v = line.split('=', 1)
                        key = k.strip()
                        if key in self.config:
                            self.config[key] = v.strip()
            if self.config.get('TG_BOT_TOKEN') and self.config.get('TG_CHAT_ID'):
                self.has_telegram = True
                print("✅ Telegram 配置已加载")
        else:
            print("ℹ️ 未找到 tg.txt")

    def setup_directories(self):
        self.work_dir.mkdir(parents=True, exist_ok=True)
        (self.work_dir / "bin").mkdir(parents=True, exist_ok=True)

    def _get_urllib_opener(self):
        opener = urllib.request.build_opener()
        if self.config.get('proxy'):
            try:
                proxy_handler = urllib.request.ProxyHandler({
                    'http': self.config['proxy'],
                    'https': self.config['proxy']
                })
                opener = urllib.request.build_opener(proxy_handler)
            except:
                pass
        return opener

    def get_latest_cfst_version(self):
        cache_file = self.work_dir / "latest_version.cache"
        if not self.force_update and cache_file.exists():
            try:
                content = cache_file.read_text(encoding='utf-8').strip()
                if '|' in content:
                    version, ts = content.split('|')
                    if time.time() - float(ts) < 86400:
                        print(f"✅ 使用缓存最新版本: {version}")
                        return version
            except:
                pass

        print("🔍 检查 cfst 最新版本 (GitHub API)...")
        try:
            api_url = "https://api.github.com/repos/XIU2/CloudflareSpeedTest/releases/latest"
            req = urllib.request.Request(api_url, headers={"User-Agent": "iStoreOS-CFST/1.0"})
            with self._get_urllib_opener().open(req, timeout=15) as r:
                data = json.loads(r.read().decode('utf-8'))
                version = data.get('tag_name', 'v2.3.4')
                cache_file.write_text(f"{version}|{time.time()}", encoding='utf-8')
                print(f"✅ 最新 cfst 版本: {version}")
                return version
        except Exception as e:
            print(f"⚠️ API 获取失败，使用稳定版 v2.3.4 ({e})")
            return "v2.3.4"

    def get_cfst_url(self):
        version = self.get_latest_cfst_version()
        machine = platform.machine().lower()
        arch = "arm64" if any(x in machine for x in ["aarch64", "arm64"]) else "amd64"
        url = f"https://github.com/XIU2/CloudflareSpeedTest/releases/download/{version}/cfst_linux_{arch}.tar.gz"
        print(f"📥 将使用 cfst {version} ({arch})")
        return url, version

    def download_file(self, url: str, dst: Path, max_retries=2) -> bool:
        print(f"正在下载: {url.split('/')[-1]}（走代理）")
        dst.parent.mkdir(parents=True, exist_ok=True)
        temp_file = dst.with_suffix(dst.suffix + '.part')

        for attempt in range(max_retries + 1):
            try:
                headers = {"User-Agent": "iStoreOS-CFST/1.0"}
                downloaded = temp_file.stat().st_size if temp_file.exists() else 0
                if downloaded > 0:
                    headers['Range'] = f'bytes={downloaded}-'

                req = urllib.request.Request(url, headers=headers)
                with self._get_urllib_opener().open(req, timeout=80) as r:
                    mode = 'ab' if downloaded > 0 else 'wb'
                    with open(temp_file, mode) as f:
                        shutil.copyfileobj(r, f)

                temp_file.rename(dst)
                print(f"✅ 下载完成 ({dst.stat().st_size // 1024} KB)")
                return True
            except Exception as e:
                print(f"⚠️ 下载失败 (尝试 {attempt+1}/{max_retries+1}): {e}")
                if attempt == max_retries:
                    return False
                time.sleep(3)
        return False

    def extract_archive(self, archive: Path, out_dir: Path) -> bool:
        out_dir.mkdir(parents=True, exist_ok=True)
        try:
            print(f"解压: {archive.name}")
            if archive.name.lower().endswith((".tar.gz", ".tgz")):
                with tarfile.open(archive, "r:gz") as t:
                    t.extractall(out_dir)
            elif archive.name.lower().endswith(".zip"):
                with zipfile.ZipFile(archive, "r") as z:
                    z.extractall(out_dir)
            print("✅ 解压完成")
            return True
        except Exception as e:
            print(f"❌ 解压失败: {e}")
            return False

    def find_cfst_binary(self, bin_dir: Path) -> Path:
        for name in ("cfst", "CloudflareST"):
            for p in [bin_dir / name, *bin_dir.rglob(name)]:
                if p.is_file():
                    return p
        raise FileNotFoundError("未找到 cfst 二进制文件")

    def check_cfst_executable(self, cfst_path: Path) -> bool:
        if not cfst_path.exists():
            return False
        cfst_path.chmod(0o755)
        try:
            result = subprocess.run([str(cfst_path), "--version"], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print(f"✅ cfst 验证通过: {result.stdout.strip()}")
                return True
        except:
            pass
        return False

    def run_speed_test(self, cfst_bin: Path) -> bool:
        print("🚀 开始 Cloudflare 测速...（强制直连，不走代理）")
        cmd = [str(cfst_bin)] + self.config['cfst_args'].split()
        env = os.environ.copy()
        for var in ['http_proxy', 'https_proxy', 'HTTP_PROXY', 'HTTPS_PROXY', 'all_proxy', 'ALL_PROXY']:
            env.pop(var, None)
        try:
            subprocess.run(cmd, cwd=self.base_dir, env=env, check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def get_region_for_ip(self, ip: str) -> str:
        ip_parts = ip.split('.')
        if len(ip_parts) < 2:
            return "Other"
        first, second = int(ip_parts[0]), int(ip_parts[1])
        if first == 103 and second in [21, 22]: return "JP"
        if first == 103 and second in [4, 31]: return "SG"
        if first in [190, 188] and second in [93, 114]: return "HK"
        if first == 104 and 16 <= second <= 31 or first == 172 and 64 <= second <= 71: return "US"
        if first == 103 and second in [22, 23]: return "KR"
        if first == 141 and second == 101: return "GB"
        if first == 197 and second == 234: return "IN"
        return "Other"

    def parse_top_ips_by_region(self, csv_path: Path) -> list[str]:
        ip_data = []
        try:
            with open(csv_path, "r", encoding="utf-8", newline="") as f:
                reader = csv.reader(f)
                next(reader, None)
                for row in reader:
                    if len(row) < 5 or not row[0].strip():
                        continue
                    ip = row[0].strip()
                    latency = float(row[4]) if row[4].strip() else 9999.0
                    speed = float(row[5]) if len(row) > 5 and row[5].strip() else 0.0
                    region = self.get_region_for_ip(ip)
                    ip_data.append((ip, latency, region, speed))
        except Exception as e:
            print(f"❌ 读取 result.csv 失败: {e}")

        ip_data.sort(key=lambda x: x[1])
        selected_ips = []
        region_counts = {r: 0 for r in self.config['priority_regions']}
        for ip, latency, region, speed in ip_data:
            if region in region_counts and region_counts[region] < self.config['max_per_region']:
                if self.full_speed and speed > 0:
                    selected_ips.append(f"{ip}#{region}-{speed:.2f}")
                else:
                    selected_ips.append(f"{ip}#{region}")
                region_counts[region] += 1
            if len(selected_ips) >= self.config['max_total']:
                break
        return selected_ips[:10]

    def ensure_ip_txt(self) -> bool:
        ip_txt = self.base_dir / "ip.txt"
        if ip_txt.exists():
            print("✅ ip.txt 已存在")
            return True
        return self.download_file(self.config['ip_txt_url'], ip_txt)

    def prepare_cfst_binary(self):
        cfst_url, version = self.get_cfst_url()
        filename = cfst_url.split('/')[-1]
        archive = self.work_dir / filename
        bin_dir = self.work_dir / "bin"
        cfst_bin = bin_dir / "cfst"

        if cfst_bin.exists() and not self.force_update:
            try:
                result = subprocess.run([str(cfst_bin), "--version"], capture_output=True, text=True, timeout=5)
                if version in (result.stdout + result.stderr):
                    print(f"✅ 已为最新版 cfst {version}")
                    return cfst_bin
            except:
                pass

        print(f"📥 准备 cfst {version}...")
        if not archive.exists() or self.force_update:
            if not self.download_file(cfst_url, archive):
                return None

        if bin_dir.exists():
            shutil.rmtree(bin_dir)
        if not self.extract_archive(archive, bin_dir):
            return None

        try:
            cfst_bin = self.find_cfst_binary(bin_dir)
            cfst_bin.chmod(0o755)
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
        best_path = self.base_dir / "best_ip.txt"
        best_path.write_text("\n".join(ips) + "\n", encoding="utf-8")
        print(f"✅ 已提取 {len(ips)} 个最优IP → best_ip.txt")
        return True

    def upload_to_github(self) -> bool:
        if not self.has_github:
            return False
        best_path = self.base_dir / "best_ip.txt"
        if not best_path.exists():
            return False
        print(f"上传到 GitHub: {self.config['GH_REPO']}（走代理）")
        try:
            content = base64.b64encode(best_path.read_bytes()).decode('utf-8')
            api_url = f"https://api.github.com/repos/{self.config['GH_REPO']}/contents/best_ip.txt"
            opener = self._get_urllib_opener()

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
                if e.code != 404:
                    raise

            data = {"message": "Update best_ip.txt", "content": content}
            if self.config.get('GH_USERNAME') or self.config.get('GH_EMAIL'):
                data["committer"] = {
                    "name": self.config.get('GH_USERNAME', 'CFST-Bot'),
                    "email": self.config.get('GH_EMAIL', 'cfst-bot@noreply.github.com')
                }
            if sha:
                data["sha"] = sha

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
        if not self.has_telegram:
            return
        url = f"https://api.telegram.org/bot{self.config['TG_BOT_TOKEN']}/sendMessage"
        data = {"chat_id": self.config['TG_CHAT_ID'], "text": message, "parse_mode": "HTML"}
        try:
            opener = self._get_urllib_opener()
            req = urllib.request.Request(url, data=json.dumps(data).encode(), headers={'Content-Type': 'application/json'})
            with opener.open(req, timeout=15) as resp:
                if resp.status == 200:
                    print("✅ Telegram 通知已发送")
        except Exception as e:
            print(f"⚠️ Telegram 发送失败: {e}")

    def run(self) -> bool:
        print("=" * 80)
        print("🚀 iStoreOS/N1 Cloudflare 测速脚本 [自动更新 cfst]")
        print(f"系统: {platform.machine()} | Python: {platform.python_version()}")
        print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        if self.force_update:
            print("⚡ 强制更新模式已开启")
        print("=" * 80)

        if not self.ensure_ip_txt():
            return False
        cfst_bin = self.prepare_cfst_binary()
        if not cfst_bin:
            return False
        if not self.run_speed_test(cfst_bin):
            return False
        if not self.process_results():
            return False

        upload_ok = self.upload_to_github()

        best_path = self.base_dir / "best_ip.txt"
        if best_path.exists():
            with open(best_path, 'r', encoding='utf-8') as f:
                ips = [line.strip() for line in f if line.strip()]

            elapsed = time.time() - self.start_time
            total_time = f"{int(elapsed//60)}分{int(elapsed%60)}秒"
            mode_str = "完整测速（含速度）" if self.full_speed else "仅延迟测试（不带速度）"

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
        print(f"模式: {'完整测速（带速度）' if self.full_speed else '仅延迟测试（不带速度）'}")
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
    speedtest = CloudflareSpeedTestIStoreOS()
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