## 视图
### 用户视图
用户从终端成功登录至设备即进入用户视图，在屏幕上显示：

<Huawei>

在用户视图下，用户可以完成查看运行状态和统计信息等功能。

### 系统视图
在用户视图下，输入命令system-view(sys)后回车，进入系统视图。

[Huawei]

在系统视图下，用户可以配置系统参数以及通过该视图进入其他的功能配置视图。

### 接口视图
使用interface命令并指定接口类型及接口编号可以进入相应的接口视图。

[Huawei]int e0/0/0
[Huawei-Ethernet0/0/0]

### 退出命令行视图
执行q命令，即可从当前视图退出至上一层视图。
<Ctrl+Z>或者执行r命令,直接退回到用户视图。

## 帮助
>?  ”获取该命令视图下所有的命令及其简单描述
也可以键入一条命令的部分关键字，后接以空格分隔的“?”

### 基本命令
```sh
#(sysname)修改路由器的名称为R1
sys R1

# 撤销操作
undo 命令

# 保存，不保存的话重启之后配置就都没有了
save

# 重启设备
reboot

# 关闭探测信息
undo terminal monitor
```


### ip配置
```sh
# 交换机，需要通过vlan配置
[Huawei]vlan 10
[Huawei-vlan10]q
[Huawei]int vlan10
[Huawei-Vlanif10]ip address 192.168.2.254 24
[Huawei-Vlanif10]q
[Huawei]int g0/0/1
[Huawei-GigabitEthernet0/0/1]port link-type access 
[Huawei-GigabitEthernet0/0/1]port default vlan 10
# 查看配置是否生效
[Huawei]dis vlan
```



```sh
#查看接口简略(brief)配置
dis ip int b 


# 查看路由表
dis ip routing-table
# 查看静态路由表，包括
dis ip routing-table


```