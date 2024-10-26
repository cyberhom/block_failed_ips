import subprocess
import time
import re
from collections import defaultdict

# زمان انتظار برای بررسی دوباره
CHECK_INTERVAL = 60  # در ثانیه
MAX_FAILED_ATTEMPTS = 6

failed_attempts = defaultdict(int)

def block_ip(ip):
    """بلاک کردن IP با استفاده از iptables"""
    print(f"Blocking IP: {ip}")
    subprocess.run(["iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"])

def check_logs():
    """بررسی لاگ‌ها برای شناسایی IP های ناموفق"""
    with open('/var/log/auth.log') as log_file:
        for line in log_file:
            match = re.search(r'Failed password for .* from (\d+\.\d+\.\d+\.\d+)', line)
            if match:
                ip = match.group(1)
                failed_attempts[ip] += 1
                print(f"Failed attempt from IP: {ip} (Total: {failed_attempts[ip]})")

                if failed_attempts[ip] > MAX_FAILED_ATTEMPTS:
                    block_ip(ip)

def main():
    """تابع اصلی برای اجرای مداوم"""
    while True:
        check_logs()
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()