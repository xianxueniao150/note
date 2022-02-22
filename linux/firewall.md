#防火墙开放端口
```sh
firewall-cmd --zone=public --add-port=8080/tcp --permanent
firewall-cmd --reload
```

#关闭防火墙
```sh
systemctl stop firewalld.service
```
