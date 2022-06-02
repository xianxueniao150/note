## setnx 
```sh
# 返回0表示设置失败，返回1表示设置成功
# lock-name 没有特定要求，建议lock-key格式,value设为1即可,
setnx lock-name value

# 操作完毕通过del操作释放锁
del  lock-name

# 使用 expire 为锁key添加时间限定，到时不释放，放弃锁
expire lock-key second
pexpire lock-key milliseconds
```

利用setnx命令的返回值特征
 对于返回设置成功的，拥有控制权，进行下一步的具体业务操作
 对于返回设置失败的，不具有控制权，排队或等待
