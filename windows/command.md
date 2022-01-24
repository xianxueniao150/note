## 查看占用端口的线程
```sh
netstat -aon|findstr "7001"
```

## 强制杀死线程
```sh
taskkill /f  /PID 12012
```

## 查看空闲ip
打开电脑的cmd命令行界面，依次点击【开始】【运行】，输入【cmd】。在命令行窗口输入【for /L %i IN (1,1,254) DO ping -w 1 -n 1 192.168.60.%i】，执行完毕之后，输入【arp -a】,就可以看到局域网内在线的IP了

## 查看详细网络配置（包括dns)
```sh
ipconfig /all
```


