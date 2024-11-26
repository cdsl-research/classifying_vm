# classifying_vm

## get_vm_info
各仮想マシンからauth.log，.bash_history，ps auxの出力，find /homeの出力を定期的に収集するためのプログラムです．

ps auxの実行結果
```
c0a21069@c0a21069-vm-info:~$ ps aux
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.0  0.6  22480 13620 ?        Ss   Nov07   0:55 /sbin/init
root           2  0.0  0.0      0     0 ?        S    Nov07   0:00 [kthreadd]
root           3  0.0  0.0      0     0 ?        S    Nov07   0:00 [pool_workqueue_release]
root           4  0.0  0.0      0     0 ?        I<   Nov07   0:00 [kworker/R-rcu_g]
root           5  0.0  0.0      0     0 ?        I<   Nov07   0:00 [kworker/R-rcu_p]
root           6  0.0  0.0      0     0 ?        I<   Nov07   0:00 [kworker/R-slub_]
root           7  0.0  0.0      0     0 ?        I<   Nov07   0:00 [kworker/R-netns]
root          12  0.0  0.0      0     0 ?        I<   Nov07   0:00 [kworker/R-mm_pe]
root          13  0.0  0.0      0     0 ?        I    Nov07   0:00 [rcu_tasks_kthread]
root          14  0.0  0.0      0     0 ?        I    Nov07   0:00 [rcu_tasks_rude_kthread]
root          15  0.0  0.0      0     0 ?        I    Nov07   0:00 [rcu_tasks_trace_kthread]
```

find /homeの実行結果
```
c0a21069@c0a21069-vm-info:~$ find /home
/home/c0a21069/vm_info/c0a21099-dojo-wl/c0a21099-dojo-wl_2024-11-09_ssh.tmp
/home/c0a21069/vm_info/c0a21099-dojo-wl/c0a21099-dojo-wl_2024-11-24_ssh.tmp
/home/c0a21069/vm_info/c0a21099-dojo-wl/c0a21099-dojo-wl_2024-11-25_ssh.tmp
/home/c0a21069/vm_info/c0a21099-dojo-wl/c0a21099-dojo-wl_2024-11-22_ssh.tmp
/home/c0a21069/vm_info/c0a21099-dojo-wl/c0a21099-dojo-wl_2024-11-21_ssh.tmp
/home/c0a21069/vm_info/c0a21099-dojo-wl/c0a21099-dojo-wl_2024-11-24_ps.tmp
/home/c0a21069/vm_info/c0a21099-dojo-wl/c0a21099-dojo-wl_2024-11-10_ssh.tmp
```


実行方法

```sh
scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null c0a21069@c0a21069-vm-info:/home/c0a21069/get_vm_info/setup_get_vm_info.sh . && bash setup_get_vm_info.sh
```

実行結果は下のようになります．

```
c0a21069@c0a21069-db:~$ scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null c0a21069@c0a21069-vm-info:/home/c0a21069/get_vm_info/setup_get_vm_info.sh . && bash setup_get_vm_info.sh
Warning: Permanently added 'c0a21069-vm-info' (ED25519) to the list of known hosts.
c0a21069@c0a21069-vm-info's password: 
setup_get_vm_info.sh                                                                                                                                                                                                           100% 2327    49.4KB/s   00:00    
Warning: Permanently added 'c0a21069-vm-info' (ED25519) to the list of known hosts.
c0a21069@c0a21069-vm-info's password: 
c0a21069_key                                                                                                                                                                                                                   100%  419     8.8KB/s   00:00    
Warning: Permanently added 'c0a21069-vm-info' (ED25519) to the list of known hosts.
c0a21069_tool.timer                                                                                                                                                                                                            100%  142     7.6KB/s   00:00    
Warning: Permanently added 'c0a21069-vm-info' (ED25519) to the list of known hosts.
c0a21069_tool.service                                                                                                                                                                                                          100%  163     1.7KB/s   00:00    
Warning: Permanently added 'c0a21069-vm-info' (ED25519) to the list of known hosts.
get_vm_info.sh                                                                                                                                                                                                                 100% 2036   182.3KB/s   00:00    
Warning: Permanently added 'c0a21069-vm-info' (ED25519) to the list of known hosts.
Warning: Permanently added 'c0a21069-vm-info' (ED25519) to the list of known hosts.
auth.log.1                                                                                                                                                                                                                     100%  291KB  54.7MB/s   00:00    
auth.log.2.gz                                                                                                                                                                                                                  100%   12KB 724.6KB/s   00:00    
auth.log.3.gz                                                                                                                                                                                                                  100%   15KB  16.2MB/s   00:00    
auth.log.4.gz                                                                                                                                                                                                                  100%   19KB 203.0KB/s   00:00    
cp: cannot stat '/home/nobody/.bash_history': No such file or directory
Warning: Permanently added 'c0a21069-vm-info' (ED25519) to the list of known hosts.
c0a21069-db_nobody.tmp                                                                                                                                                                                                         100%    0     0.0KB/s   00:00    
Warning: Permanently added 'c0a21069-vm-info' (ED25519) to the list of known hosts.
c0a21069-db_c0a21069.tmp                                                                                                                                                                                                       100% 6663   123.3KB/s   00:00    
Warning: Permanently added 'c0a21069-vm-info' (ED25519) to the list of known hosts.
c0a21069-db_directory.tmp
```

まず，収集先の仮想マシンから``setup_get_vm_info.sh``をコピーします．

次に，``setup_get_vm_info.sh``を実行し，``c0a21069_key``，``c0a21069_tool.timer``，``c0a21069_tool.service``，``get_vm_info.sh``をコピーします．

その後，定期実行を行えるようにし，各情報の一回目の収集を行います．


### setup_get_vm_info.sh
最初のコマンド実行時にコピーするファイルです．残りのファイルのコピーと定期的に情報を取得するためのセットアップを行います．

### get_vm_info.sh
定期実行されるプログラムです．

### c0a21069_tool.service
``get_vm_info.sh``を定期実行させるファイルです．

### c0a21069_tool.timer
定期実行の間隔を設定するファイルです． 毎日6時に実行されるように設定されています．



## tool_vm
収集した情報を成形するためのプログラムです．全てPython3で書かれています．

### analysis_vm.py
実行方法
```
python3 analysis_vm.py
```

収集した``auth.log``を読み込み，1日ごとに何回SSHしたかをテキストファイルに記録します．

出力されるテキストファイルは下のようになっています．
```
【2024-10-17】
  ユーザー: c0a21069(uid=1000) - 接続回数: 1

【2024-10-24】
  ユーザー: c0a21069(uid=1000) - 接続回数: 1

【2024-10-30】
  ユーザー: c0a21069(uid=1000) - 接続回数: 1
```


### process_vm.py
実行方法
```
python3 process_vm.py
```

収集したps auxの出力をユーザーごとに実行しているプロセスをまとめてテキストファイルに記録します．

出力されるテキストファイルは下のようになっています．
```
ユーザー: root
  プロセス: /bin/bash /c0a21021_log_collect/log_collect.sh
  プロセス: /bin/bash /c0a21069_tool_Box/get_vm_info.sh
  プロセス: /bin/bash /c0a21134_tool_Box/c0a21134_log_collect.sh
  プロセス: /sbin/agetty -o -p -- \u --noclear - linux
  プロセス: /sbin/init
  プロセス: /sbin/multipathd -d -s
  プロセス: /usr/bin/VGAuthService
  プロセス: /usr/bin/python3 /usr/share/unattended-upgrades/unattended-upgrade-shutdown --wait-for-signal
```







