import os
from collections import defaultdict

# 仮想マシンごとのプロセス情報を格納するディクショナリ
vm_processes = defaultdict(list)

# 仮想マシンごとのプロセス情報ファイルが格納されているディレクトリ
base_directory = '/home/c0a21069/analyzed_vm_info/'

# 仮想マシンのディレクトリを検索し、プロセスファイルを読み込む
for vm_dir in os.listdir(base_directory):
    vm_path = os.path.join(base_directory, vm_dir)
    
    # ディレクトリ内のプロセスファイルを読み込む
    if os.path.isdir(vm_path):
        for filename in os.listdir(vm_path):
            if filename.endswith('.txt'):  # プロセス情報が含まれるファイル
                file_path = os.path.join(vm_path, filename)
                
                # 仮想マシン名をファイル名から取得
                vm_name = filename.split('_')[1]  # ファイル名から仮想マシン名を抽出
                
                # プロセスファイルを読み込んでプロセスをリストに追加
                with open(file_path, 'r') as file:
                    lines = file.readlines()
                    for line in lines:
                        if line.startswith("  プロセス: "):
                            process_name = line.split(": ", 1)[1].strip()
                            vm_processes[vm_name].append(process_name)

# 各VMのプロセスリストを比較して特徴的なプロセスを抽出
unique_processes = defaultdict(list)

# 各仮想マシンのプロセスリストと比較
for vm_name, processes in vm_processes.items():
    for process in processes:
        is_unique = True
        # 他の仮想マシンでそのプロセスが存在するか確認
        for other_vm_name, other_processes in vm_processes.items():
            if vm_name != other_vm_name and process in other_processes:
                is_unique = False
                break
        # 他のVMに存在しないプロセスがあれば特徴的なプロセスとしてリストに追加
        if is_unique:
            unique_processes[vm_name].append(process)

# 結果をファイルに書き込む
output_file = '/home/c0a21069/analyzed_vm_info/feture_vm.txt'
with open(output_file, 'w') as file:
    for vm_name, unique_procs in unique_processes.items():
        file.write(f"VM名: {vm_name}\n")
        for proc in unique_procs:
            file.write(f"  特徴的なプロセス: {proc}\n")
        file.write("\n")

