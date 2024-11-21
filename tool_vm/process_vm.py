import os
from collections import defaultdict
from glob import glob

# 元のログディレクトリのパス
vm_info_dir = "/home/c0a21069/vm_info"
# 集計結果を保存するベースディレクトリ
output_base_dir = "/home/c0a21069/analyzed_vm_info"

# 仮想マシンごとのディレクトリを取得
vm_dirs = [d for d in glob(os.path.join(vm_info_dir, '*')) if os.path.isdir(d)]

# 各仮想マシンごとに処理
for vm_dir in vm_dirs:
    vm_name = os.path.basename(vm_dir)  # 仮想マシン名を取得
    user_processes = defaultdict(set)  # ユーザーごとのプロセスコマンド情報を格納する辞書（重複を排除するためセットを使用）

    # _ps.tmpファイルを取得
    ps_tmp_files = glob(os.path.join(vm_dir, '*_ps.tmp'))

    # 各_ps.tmpファイルを処理
    for ps_tmp_file in ps_tmp_files:
        with open(ps_tmp_file, 'r') as f:
            lines = f.readlines()

        # ps auxの出力から各行を処理
        for line in lines:
            parts = line.split(maxsplit=10)  # 最大11列を分割（最後の列はコマンド）
            if len(parts) < 11:
                continue  # パース失敗時はスキップ

            user = parts[0]       # ユーザー名
            command = parts[10]   # コマンド

            # すべてのユーザーを記録（重複するコマンドは1つにまとめる）
            user_processes[user].add(command)

    # 集計結果を保存するディレクトリを作成
    output_vm_dir = os.path.join(output_base_dir, vm_name)
    os.makedirs(output_vm_dir, exist_ok=True)

    # 集計結果をファイルに出力
    output_file = os.path.join(output_vm_dir, f"{vm_name}_user_processes.txt")
    with open(output_file, 'w') as f:
        for user, commands in user_processes.items():
            f.write(f"ユーザー: {user}\n")
            for command in sorted(commands):  # ソートして出力
                f.write(f"  プロセス: {command}")
            f.write("\n")

