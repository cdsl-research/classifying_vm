import gzip
import os
import re
from collections import defaultdict
from glob import glob
from datetime import datetime, timedelta

# 元のログディレクトリのパス
vm_info_dir = "/home/c0a21069/vm_info"
# 集計結果を保存するベースディレクトリ（コードを実行したディレクトリ）
output_base_dir = "/home/c0a21069/analyzed_vm_info"

# 仮想マシンごとのディレクトリを取得
vm_dirs = [d for d in glob(os.path.join(vm_info_dir, '*')) if os.path.isdir(d)]

# 各仮想マシンごとに処理
for vm_dir in vm_dirs:
    vm_name = os.path.basename(vm_dir)
    ssh_summary = defaultdict(lambda: defaultdict(int))  # SSH接続情報を格納する辞書
    
    # auth.logファイルと圧縮ファイル(auth.log.*.gz)を取得
    log_files = glob(os.path.join(vm_dir, 'auth.log*'))
    # _ssh.tmpファイルを取得
    ssh_tmp_files = glob(os.path.join(vm_dir, '*_ssh.tmp'))

    # auth.logファイルの処理
    for log_file in log_files:
        #print(f"Processing auth log file: {log_file}")
        if log_file.endswith('.gz'):
            with gzip.open(log_file, 'rt') as f:
                lines = f.readlines()
        else:
            with open(log_file, 'r') as f:
                lines = f.readlines()

        for line in lines:
            if "sshd" in line and "session opened" in line:
                # 日時とユーザー名のマッチ
                # ISO 8601形式 (例: 2024-10-31T14:12:18.264087+09:00)
                date_match = re.search(r'^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})', line)
                user_match = re.search(r'session opened for user (\S+)', line)

                if date_match and user_match:
                    date_str = date_match.group(1)
                    date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')
                    date_jst = date_obj + timedelta(hours=9)  # 日本時間に変換

                    date_formatted = date_jst.strftime('%Y-%m-%d')
                    user = user_match.group(1)
                    ssh_summary[date_formatted][user] += 1
                else:
                    # ローカル日時形式 (例: Oct 25 11:17:20)
                    date_match = re.search(r'([A-Za-z]{3} \d{2} \d{2}:\d{2}:\d{2})', line)
                    
                    if date_match and user_match:
                        date_str = date_match.group(1)
                        # 現在の年を追加して日付を作成
                        date_obj = datetime.strptime(f"{datetime.now().year} {date_str}", '%Y %b %d %H:%M:%S')
                        date_formatted = date_obj.strftime('%Y-%m-%d')
                        user = user_match.group(1)
                        ssh_summary[date_formatted][user] += 1

    # _ssh.tmpファイルの処理
    for ssh_tmp_file in ssh_tmp_files:
        #print(f"Processing _ssh.tmp file: {ssh_tmp_file}")
        with open(ssh_tmp_file, 'r') as f:
            lines = f.readlines()

        for line in lines:
            if "sshd" in line and "session opened" and ">" in line:
                line = line[2:]                # 日付とユーザー名をマッチ
                date_match = re.search(r'^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})', line)
                user_match = re.search(r'session opened for user (\S+)', line)

                if date_match and user_match:
                    date_str = date_match.group(1)
                    date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')
                    date_jst = date_obj + timedelta(hours=9)  # 日本時間に変換

                    date_formatted = date_jst.strftime('%Y-%m-%d')
                    user = user_match.group(1)
                    ssh_summary[date_formatted][user] += 1
                else:
                    # ローカル日時形式の場合（Oct 25 11:17:20）
                    date_match = re.search(r'([A-Za-z]{3} \d{2} \d{2}:\d{2}:\d{2})', line)  # ローカル日時形式

                    if date_match and user_match:
                        date_str = date_match.group(1)
                        # 現在の年を追加して日付を作成
                        date_obj = datetime.strptime(f"{datetime.now().year} {date_str}", '%Y %b %d %H:%M:%S')
                        date_formatted = date_obj.strftime('%Y-%m-%d')
                        user = user_match.group(1)
                        ssh_summary[date_formatted][user] += 1



    # 集計結果を保存するディレクトリを作成
    output_vm_dir = os.path.join(output_base_dir, vm_name)
    os.makedirs(output_vm_dir, exist_ok=True)

    # 集計結果をファイルに出力
    output_file = os.path.join(output_vm_dir, f"{vm_name}_ssh_summary.txt")
    with open(output_file, 'w') as f:
        for date in sorted(ssh_summary):
            f.write(f"【{date}】\n")
            for user, count in ssh_summary[date].items():
                f.write(f"  ユーザー: {user} - 接続回数: {count}\n")
            f.write("\n")
    
    #print(f"集計結果が {output_file} に保存されました。")

    # デバッグ用にファイルの内容を確認
    #with open(output_file, 'r') as f:
        #print(f"Contents of {output_file}:\n{f.read()}")
