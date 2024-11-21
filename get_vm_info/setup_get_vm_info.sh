#!/bin/bash

# 1. /c0a21069_tool_Boxを作成
sudo mkdir -p /c0a21069_tool_Box

# 2. 必要ファイルの追加
# Timer, serviceの内容をここで編集
sudo scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null c0a21069@c0a21069-vm-info:/home/c0a21069/get_vm_info/c0a21069_key /c0a21069_tool_Box/c0a21069_key
sudo chmod 600 /c0a21069_tool_Box/c0a21069_key
sudo scp -i /c0a21069_tool_Box/c0a21069_key -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null c0a21069@c0a21069-vm-info:/home/c0a21069/get_vm_info/c0a21069_tool.timer /etc/systemd/system/c0a21069_tool.timer
sudo scp -i /c0a21069_tool_Box/c0a21069_key -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null c0a21069@c0a21069-vm-info:/home/c0a21069/get_vm_info/c0a21069_tool.service /etc/systemd/system/c0a21069_tool.service
sudo scp -i /c0a21069_tool_Box/c0a21069_key -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null c0a21069@c0a21069-vm-info:/home/c0a21069/get_vm_info/get_vm_info.sh /c0a21069_tool_Box/get_vm_info.sh

# 3. 実行ファイルの権限付与
sudo chmod 744 /c0a21069_tool_Box/get_vm_info.sh

# 4. Timer, serviceの起動
sudo systemctl daemon-reload
sudo systemctl enable c0a21069_tool.timer
sudo systemctl start c0a21069_tool.timer

sudo ssh -i /c0a21069_tool_Box/c0a21069_key -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null c0a21069@c0a21069-vm-info mkdir -p /home/c0a21069/vm_info/$(hostname)
sudo scp -i /c0a21069_tool_Box/c0a21069_key -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null /var/log/auth.log.* c0a21069@c0a21069-vm-info:/home/c0a21069/vm_info/$(hostname)
sudo cp -f /var/log/auth.log /c0a21069_tool_Box/$(hostname)_ssh.tmp

for user in $(awk -F: '$3 >= 1000 {print $1}' /etc/passwd); do
    sudo cp /home/$user/.bash_history /c0a21069_tool_Box/$(hostname)_$user.tmp
    sudo scp -i /c0a21069_tool_Box/c0a21069_key -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null /c0a21069_tool_Box/$(hostname)_$user.tmp c0a21069@c0a21069-vm-info:/home/c0a21069/vm_info/$(hostname)
done

sudo find /home | sudo tee /c0a21069_tool_Box/$(hostname)_directory.tmp > /dev/null
sudo scp -i /c0a21069_tool_Box/c0a21069_key -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null /c0a21069_tool_Box/$(hostname)_directory.tmp c0a21069@c0a21069-vm-info:/home/c0a21069/vm_info/$(hostname)
