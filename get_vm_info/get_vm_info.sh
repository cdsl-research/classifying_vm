#! /bin/bash
# 一時ファイルの作成（上書き用）
temp_ps_file="/c0a21069_tool_Box/$(hostname)_$(date "+%Y-%m-%d")_ps.tmp"
temp_ssh_file="/c0a21069_tool_Box/$(hostname)_$(date "+%Y-%m-%d")_ssh.tmp"

ps aux > "$temp_ps_file"

diff /c0a21069_tool_Box/$(hostname)_ssh.tmp /var/log/auth.log > "$temp_ssh_file"
cp -f /var/log/auth.log /c0a21069_tool_Box/$(hostname)_ssh.tmp

scp -i /c0a21069_tool_Box/c0a21069_key -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null "$temp_ps_file" c0a21069@c0a21069-vm-info:/home/c0a21069/vm_info/$(hostname)
scp -i /c0a21069_tool_Box/c0a21069_key -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null "$temp_ssh_file" c0a21069@c0a21069-vm-info:/home/c0a21069/vm_info/$(hostname)
rm "$temp_ps_file"
rm "$temp_ssh_file"

for user in $(awk -F: '$3 >= 1000 {print $1}' /etc/passwd); do
    diff /home/"$user"/.bash_history /c0a21069_tool_Box/$(hostname)_"$user".tmp > /c0a21069_tool_Box/$(hostname)_"$user"_$(date "+%Y-%m-%d").tmp
    cp /home/"$user"/.bash_history /c0a21069_tool_Box/$(hostname)_"$user".tmp
    scp -i /c0a21069_tool_Box/c0a21069_key -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null /c0a21069_tool_Box/$(hostname)_"$user"_$(date "+%Y-%m-%d").tmp c0a21069@c0a21069-vm-info:/home/c0a21069/vm_info/$(hostname)
    rm /c0a21069_tool_Box/$(hostname)_"$user"_$(date "+%Y-%m-%d").tmp
done

find /home > /c0a21069_tool_Box/$(hostname)_directory_diff.tmp
diff /c0a21069_tool_Box/$(hostname)_directory_diff.tmp /c0a21069_tool_Box/$(hostname)_directory.tmp > /c0a21069_tool_Box/$(hostname)_$(date "+%Y-%m-%d")_directory.tmp
scp -i /c0a21069_tool_Box/c0a21069_key -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null /c0a21069_tool_Box/$(hostname)_$(date "+%Y-%m-%d")_directory.tmp c0a21069@c0a21069-vm-info:/home/c0a21069/vm_info/$(hostname)
cp /c0a21069_tool_Box/$(hostname)_directory_diff.tmp /c0a21069_tool_Box/$(hostname)_directory.tmp
rm /c0a21069_tool_Box/$(hostname)_directory_diff.tmp
rm /c0a21069_tool_Box/$(hostname)_$(date "+%Y-%m-%d")_directory.tmp