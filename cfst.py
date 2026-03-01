#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
iStoreOS/N1 Cloudflare 测速脚本 - 最终版（仅IPv4）
- 默认（仅延迟）：保留前10条，格式 IP#cf-延迟ms
- --full-speed（完整测速）：每个优先地区最多10条，未识别地区丢弃，格式 IP#地区码-速度MB/s
修改 cfst 参数：直接编辑 __init__ 中的 self.default_args（最前面）
"""
import os
import sys
import csv
import json
import shutil
import tarfile
import urllib.request
import subprocess
import platform
from pathlib import Path
import time
from datetime import datetime
import base64
import argparse
import heapq
from collections import defaultdict

from colorama import init, Fore, Style
init(autoreset=True)


class CloudflareSpeedTestIStoreOS:
    def __init__(self):
        # ================================================
        # ★ cfst 参数设置区 - 用户可直接在这里修改 ★
        # 参数说明（参考 cfst 官方文档）：
        # -n   测试数量（建议 50~300，太大测太久）
        # -t   测速线程数（建议 2~4，iStoreOS 资源有限别太大）
        # -dn  下载测试数量（完整测速时建议 10~20）
        # -dt  下载测速时间；单个 IP 下载测速最长时间，不能太短
        # -sl  下载速度下限（MB/s），低于这个不保留
        # -tl  延迟上限（ms），高于这个不保留
        # -p   终端显示数量
        # -o   输出文件（固定 result.csv，不要改）
        # ================================================
        self.default_args = [
            "-n",  "100",     # 测试数量
            "-t",  "3",       # 线程数
            "-dn", "10",      # 下载测试数量（完整模式才生效）
            "-dt", "5",       # 下载测速时间
            "-sl", "20",      # 速度下限 MB/s
            "-tl", "400",     # 延迟上限 ms
            "-p",  "0",       # 终端显示数量
            "-o",  "result.csv"
        ]
        # ================================================

        self.start_time = time.time()
        self.base_dir = Path(__file__).parent.resolve()
        self.work_dir = self.base_dir / ".cfst_cache"
        self.setup_directories()

        self.config = {
            'max_per_region': 10,
            'max_total_latency': 10,
            'priority_regions': ["JP", "SG", "HK", "US", "KR", "GB", "IN"],
            'ip_txt_url': "https://raw.githubusercontent.com/XIU2/CloudflareSpeedTest/master/ip.txt",
            'proxy': '',
            'GH_REPO': None,
            'GH_TOKEN': None,
            'GH_USERNAME': None,
            'GH_EMAIL': None,
            'TG_BOT_TOKEN': None,
            'TG_CHAT_ID': None
        }

        parser = argparse.ArgumentParser(description="iStoreOS Cloudflare 测速脚本")
        parser.add_argument('--full-speed', action='store_true', help="完整测速模式（带下载速度）")
        parser.add_argument('--force-update', action='store_true', help="强制更新 cfst")
        args = parser.parse_args()

        self.full_speed = args.full_speed
        self.force_update = args.force_update

        print(Fore.CYAN + "=" * 80)
        print(Fore.GREEN + "🚀 iStoreOS/N1 Cloudflare 测速脚本 [最终版]")
        print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        if self.force_update:
            print(Fore.YELLOW + "⚡ 强制更新模式")
        print(Fore.GREEN + f"当前模式: {'完整测速（带速度）' if self.full_speed else '仅延迟测试'}")
        print(Fore.CYAN + "=" * 80)

        self.opener = self._get_urllib_opener()
        self.has_proxy = False
        self.has_github = False
        self.has_telegram = False

        self.load_proxy()
        self.load_github_config()
        self.load_telegram_config()

        self.airport_to_country = {
            "SJC":"US","SEA":"US","LAX":"US","ORD":"US","MIA":"US","JFK":"US","IAD":"US","EWR":"US","ATL":"US","DFW":"US",
            "BOS":"US","DEN":"US","PHX":"US","LAS":"US","SFO":"US","PDX":"US","DTW":"US","MSP":"US",
            "NRT":"JP","HND":"JP","KIX":"JP","TYO":"JP","FUK":"JP","CTS":"JP",
            "HKG":"HK","SIN":"SG","SGP":"SG","ICN":"KR","GMP":"KR",
            "LHR":"GB","MAN":"GB","BOM":"IN","DEL":"IN",
        }

    def load_proxy(self):
        f = self.base_dir / "proxy.txt"
        if f.exists():
            p = f.read_text(encoding='utf-8').strip()
            if p:
                self.config['proxy'] = p
                self.has_proxy = True
                print(Fore.GREEN + f"✅ 已加载代理: {p}")

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
                print(Fore.GREEN + f"✅ GitHub 配置已加载: {self.config['GH_REPO']}")

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
                print(Fore.GREEN + "✅ Telegram 配置已加载")

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
                    print(Fore.GREEN + f"✅ 使用缓存最新版本: {v}")
                    return v
            except:
                pass
        print(Fore.CYAN + "🔍 检查 cfst 最新版本...")
        try:
            req = urllib.request.Request(
                "https://api.github.com/repos/XIU2/CloudflareSpeedTest/releases/latest",
                headers={"User-Agent": "iStoreOS-CFST/1.0"}
            )
            with self.opener.open(req, timeout=15) as r:
                data = json.loads(r.read().decode())
                v = data['tag_name']
            cache.write_text(f"{v}|{time.time()}", encoding='utf-8')
            print(Fore.GREEN + f"✅ 成功获取最新版本: {v}")
            return v
        except Exception as e:
            print(Fore.RED + f"❌ 获取最新 cfst 版本失败: {e}")
            sys.exit(1)

    def get_cfst_url(self):
        v = self.get_latest_cfst_version()
        machine = platform.machine().lower()
        arch = "arm64" if any(x in machine for x in ["aarch64", "arm64"]) else "amd64"
        url = f"https://github.com/XIU2/CloudflareSpeedTest/releases/download/{v}/cfst_linux_{arch}.tar.gz"
        print(Fore.CYAN + f"📥 将使用 cfst {v} ({arch})")
        return url, v

    def download_file(self, url: str, dst: Path, max_retries=2) -> bool:
        print(Fore.CYAN + f"正在下载: {url.split('/')[-1]}")
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
                print(Fore.GREEN + f"✅ 下载完成 ({dst.stat().st_size // 1024:,} KB)")
                return True
            except Exception as e:
                print(Fore.YELLOW + f"⚠️ 下载失败 (尝试 {attempt+1}): {e}")
                if attempt == max_retries:
                    return False
                time.sleep(2)
        return False

    def extract_archive(self, archive: Path, out_dir: Path) -> bool:
        out_dir.mkdir(parents=True, exist_ok=True)
        try:
            print(Fore.CYAN + f"解压: {archive.name}")
            if archive.name.lower().endswith((".tar.gz", ".tgz")):
                with tarfile.open(archive, "r:gz") as t:
                    t.extractall(out_dir)
            print(Fore.GREEN + "✅ 解压完成")
            return True
        except Exception as e:
            print(Fore.RED + f"❌ 解压失败: {e}")
            return False

    def find_cfst_binary(self, bin_dir: Path) -> Path:
        for name in ("cfst", "CloudflareST"):
            for p in [bin_dir / name, *bin_dir.rglob(name)]:
                if p.is_file():
                    return p
        raise FileNotFoundError("未找到 cfst 二进制文件")

    def check_cfst_executable(self, cfst_path: Path) -> bool:
        cache = self.work_dir / "cfst_verified.cache"
        if cache.exists() and (time.time() - cache.stat().st_mtime < 86400):
            print(Fore.GREEN + "✅ cfst 已验证（缓存）")
            return True
        cfst_path.chmod(0o755)
        try:
            r = subprocess.run([str(cfst_path), "--version"], capture_output=True, text=True, encoding='utf-8', errors='ignore', timeout=8)
            if r.returncode == 0:
                cache.touch()
                print(Fore.GREEN + f"✅ cfst 验证通过: {r.stdout.strip()}")
                return True
        except:
            pass
        print(Fore.RED + "❌ cfst 可执行文件验证失败")
        return False

    def prepare_cfst_binary(self):
        url, version = self.get_cfst_url()
        filename = url.split('/')[-1]
        archive = self.work_dir / filename
        bin_dir = self.work_dir / "bin"
        cfst_bin = bin_dir / "cfst"
        if cfst_bin.exists() and not self.force_update:
            try:
                r = subprocess.run([str(cfst_bin), "--version"], capture_output=True, text=True, encoding='utf-8', errors='ignore', timeout=5)
                if version in r.stdout + r.stderr:
                    print(Fore.GREEN + f"✅ 已为最新版 cfst {version}")
                    return cfst_bin
            except:
                pass
        print(Fore.CYAN + f"📥 准备 cfst {version}...")
        if not archive.exists() or self.force_update:
            if not self.download_file(url, archive):
                print(Fore.RED + "❌ 下载 cfst 失败")
                return None
        if bin_dir.exists():
            shutil.rmtree(bin_dir)
        if not self.extract_archive(archive, bin_dir):
            print(Fore.RED + "❌ 解压 cfst 失败")
            return None
        try:
            cfst_bin = self.find_cfst_binary(bin_dir)
            return cfst_bin if self.check_cfst_executable(cfst_bin) else None
        except Exception as e:
            print(Fore.RED + f"❌ cfst 准备失败: {e}")
            return None

    def run_speed_test(self, cfst_bin: Path) -> bool:
        print(Fore.CYAN + "🚀 开始 Cloudflare 测速（强制直连）...")
        cmd = [str(cfst_bin)] + self.config['cfst_args'].split()
        env = os.environ.copy()
        for v in ['http_proxy', 'https_proxy', 'HTTP_PROXY', 'HTTPS_PROXY', 'all_proxy', 'ALL_PROXY', 'no_proxy']:
            env.pop(v, None)
        env['no_proxy'] = '*'
        try:
            subprocess.run(cmd, cwd=self.base_dir, env=env, check=True, timeout=300)
            print(Fore.GREEN + "✅ 测速完成（直连模式）")
            return True
        except Exception as e:
            print(Fore.RED + f"❌ 测速失败: {e}")
            return False

    def get_country(self, code: str) -> str:
        code = (code or "").strip().upper()
        if not code or code == "N/A":
            return None  # 未识别 → 丢弃
        if len(code) == 2 and code.isalpha():
            return code
        country = self.airport_to_country.get(code)
        return country if country else None

    def ensure_ip_txt(self) -> bool:
        p = self.base_dir / "ip.txt"
        if p.exists() and not self.force_update:
            print(Fore.GREEN + "✅ ip.txt 已存在（跳过下载）")
            return True
        print(Fore.CYAN + "下载 IP 段文件...")
        return self.download_file(self.config['ip_txt_url'], p)

    def parse_top_ips_by_region(self, csv_path: Path) -> list[str]:
        print(Fore.CYAN + f"正在解析 result.csv（{'完整测速' if self.full_speed else '仅延迟'}模式）...")
        selected = []

        if self.full_speed:
            country_ips = defaultdict(list)
            try:
                with open(csv_path, "r", encoding="utf-8", newline="") as f:
                    next(csv.reader(f), None)
                    for row in csv.reader(f):
                        if len(row) < 7 or not row[0].strip(): continue
                        ip = row[0].strip()
                        try:
                            speed = float(row[5].strip())
                            if speed <= 0: continue
                        except:
                            continue
                        region_code = row[6].strip() if len(row) > 6 else ""
                        country = self.get_country(region_code)
                        if country is None:  # 未识别 → 丢弃
                            continue
                        country_ips[country].append((speed, ip, country))

                for country in self.config['priority_regions']:
                    if country in country_ips:
                        country_ips[country].sort(reverse=True, key=lambda x: x[0])
                        for speed, ip, reg in country_ips[country][:self.config['max_per_region']]:
                            selected.append(f"{ip}#{reg}-{speed:.2f}MB/s")

            except Exception as e:
                print(Fore.RED + f"完整测速解析失败: {e}")

        else:
            heap = []
            try:
                with open(csv_path, "r", encoding="utf-8", newline="") as f:
                    next(csv.reader(f), None)
                    for row in csv.reader(f):
                        if len(row) < 5 or not row[0].strip(): continue
                        ip = row[0].strip()
                        try:
                            latency = float(row[4].strip()) if row[4].strip() else 9999.0
                            if 0 < latency <= 400:
                                heapq.heappush(heap, (latency, ip))
                        except:
                            continue
                heap.sort()
                for latency, ip in heap[:self.config['max_total_latency']]:
                    selected.append(f"{ip}#cf-{latency:.2f}ms")
            except Exception as e:
                print(Fore.RED + f"延迟模式解析失败: {e}")

        print(Fore.GREEN + f"✅ 提取到 {len(selected)} 条有效 IP")
        return selected

    def process_results(self) -> bool:
        csv_path = self.base_dir / "result.csv"
        if not csv_path.exists():
            print(Fore.RED + "❌ result.csv 未找到")
            return False
        ips = self.parse_top_ips_by_region(csv_path)
        if not ips:
            print(Fore.YELLOW + "⚠️ 未找到有效IP")
            return False

        output_path = self.base_dir / "best_ip.txt"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"# Cloudflare 测速结果 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"# 模式: {'完整测速（带速度）' if self.full_speed else '仅延迟测试'}\n")
            f.write(f"# 测速参数: {self.config['cfst_args']}\n")
            f.write(f"# 共 {len(ips)} 条\n")
            if self.full_speed:
                f.write("# 格式: IP#地区码-速度MB/s\n")
            else:
                f.write("# 格式: IP#cf-延迟ms\n")
            f.write("# ===============================================\n\n")
            for ip_line in ips:
                f.write(ip_line + "\n")

        print(Fore.GREEN + f"✅ 已生成 best_ip.txt（共 {len(ips)} 条）")
        return True

    def upload_to_github(self) -> bool:
        if not self.has_github: return False
        best = self.base_dir / "best_ip.txt"
        if not best.exists(): return False
        print(Fore.CYAN + f"上传到 GitHub: {self.config['GH_REPO']}")
        try:
            content = base64.b64encode(best.read_bytes()).decode('utf-8')
            api_url = f"https://api.github.com/repos/{self.config['GH_REPO']}/contents/best_ip.txt"
            sha = None
            req = urllib.request.Request(api_url, method='GET')
            req.add_header('Authorization', f'token {self.config["GH_TOKEN"]}')
            req.add_header('Accept', 'application/vnd.github.v3+json')
            req.add_header('User-Agent', 'iStoreOS-CFST/1.0')
            try:
                with self.opener.open(req) as resp:
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
            with self.opener.open(req) as resp:
                if resp.status in (200, 201):
                    print(Fore.GREEN + "✅ GitHub 上传成功")
                    return True
        except Exception as e:
            print(Fore.RED + f"❌ GitHub 上传失败: {e}")
        return False

    def send_telegram_notification(self, message: str):
        if not self.has_telegram:
            return
        print(Fore.CYAN + "📨 正在使用 curl 发送 Telegram 通知...")
        cmd = [
            "curl", "-x", self.config.get('proxy', ''),
            "-H", "Content-Type: application/json",
            "-d", json.dumps({"chat_id": self.config['TG_CHAT_ID'], "text": message, "parse_mode": "HTML"}),
            f"https://api.telegram.org/bot{self.config['TG_BOT_TOKEN']}/sendMessage"
        ]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
            if result.returncode == 0 and '"ok":true' in result.stdout:
                print(Fore.GREEN + "✅ Telegram 通知已发送（curl 方式）")
            else:
                print(Fore.YELLOW + f"⚠️ Telegram 发送失败: {result.stderr.strip() or result.stdout.strip()}")
        except Exception as e:
            print(Fore.YELLOW + f"⚠️ curl 执行失败: {e}")

    def run(self) -> bool:
        print(Fore.CYAN + "=" * 80)
        try:
            for item in self.work_dir.iterdir():
                if item.is_file() and (time.time() - item.stat().st_mtime > 7 * 86400):
                    item.unlink()
            print(Fore.GREEN + "🧹 已清理旧缓存")
        except:
            pass

        if not self.ensure_ip_txt(): return False
        cfst_bin = self.prepare_cfst_binary()
        if not cfst_bin: return False

        cmd_args = self.default_args.copy()  # 使用用户可修改的参数
        if not self.full_speed:
            cmd_args.append("-dd")           # 仅延迟模式加 -dd
        self.config['cfst_args'] = " ".join(cmd_args)

        print(Fore.BLUE + "\n当前测速参数：")
        print(Fore.BLUE + self.config['cfst_args'])
        print()

        if not self.run_speed_test(cfst_bin): return False
        if not self.process_results(): return False

        upload_ok = self.upload_to_github()
        best_path = self.base_dir / "best_ip.txt"
        if best_path.exists():
            with open(best_path, 'r', encoding='utf-8') as f:
                ips = [line.strip() for line in f if line.strip() and not line.startswith('#')]

            elapsed = time.time() - self.start_time
            total_time = f"{int(elapsed//60)}分{int(elapsed%60)}秒"
            mode_str = "完整测速" if self.full_speed else "仅延迟测试（默认）"
            msg = f"<b>🚀 Cloudflare 测速完成！</b>\n\n"
            msg += f"⏰ 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            msg += f"⏱ 总耗时: <b>{total_time}</b>\n"
            msg += f"📊 模式: {mode_str}\n"
            msg += f"📊 参数: {self.config.get('cfst_args', '默认参数')}\n"
            msg += f"📊 共找到 <b>{len(ips)}</b> 个最优IP\n\n"
            if ips:
                msg += "<b>🏆 前5条最优IP：</b>\n" + "\n".join([f"{i}. <code>{ip}</code>" for i, ip in enumerate(ips[:5], 1)])
            msg += f"\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            if self.config.get('GH_REPO'):
                link = f"https://raw.githubusercontent.com/{self.config['GH_REPO']}/refs/heads/main/best_ip.txt"
                msg += f"📂 GitHub: https://github.com/{self.config['GH_REPO']}\n"
                msg += f"📄 查看结果: <a href=\"{link}\">best_ip.txt</a>\n"
            msg += "✅ 已上传 GitHub" if upload_ok else "⚠️ GitHub 上传失败"

            self.send_telegram_notification(msg)

        self.print_summary()
        return True

    def print_summary(self):
        elapsed = time.time() - self.start_time
        print(Fore.CYAN + "\n" + "=" * 80)
        print(Fore.GREEN + "🎉 任务完成！")
        print(f"总耗时: {int(elapsed//60)}分 {int(elapsed%60)}秒")
        print(f"模式: {'完整测速' if self.full_speed else '仅延迟测试（默认）'}")
        print(f"最佳IP文件: {self.base_dir / 'best_ip.txt'}")
        best_path = self.base_dir / "best_ip.txt"
        if best_path.exists():
            with open(best_path) as f:
                ips = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                print(f"最优IP数量: {len(ips)}")
                if ips:
                    print("\n前5个最优IP:")
                    for i, ip in enumerate(ips[:5], 1):
                        print(f" {i}. {ip}")
        print(Fore.CYAN + "=" * 80)


def main():
    speedtest = CloudflareSpeedTestIStoreOS()
    try:
        return 0 if speedtest.run() else 1
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n👋 用户中断操作")
        return 130
    except Exception as e:
        print(Fore.RED + f"❌ 未预期错误: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())