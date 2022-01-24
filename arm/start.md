run.sh
```sh
# -M 指定开发版
# -m 指定内存
# -kernel 指定内核文件
# -dtb 指定设备树文件
# -nographic 命令行
# -append "root=/dev/mmcblk0 rw console=ttyAMA0"    挂载根文件系统到sdk设备第一个分区
# -sd myrootfs.ext3 以sdk卡
qemu-system-arm -M vexpress-a9 -m 512M  -kernel zImage -dtb vexpress-v2p-ca9.dtb  -nographic -append "root=/dev/mmcblk0 rw console=ttyAMA0"  2>/dev/null  -sd myrootfs.ext3
```

## 制作根文件系统
```sh
# 创建一个32M大小的空白文件
dd if=/dev/zero of=myrootfs.ext3 bs=1M count=32

# 格式化
mkfs.ext3 myrootfs.ext3

# 挂载
sudo mount -t ext3 myrootfs.ext3 /mnt -o loop

# 将必要文件拷贝到/mnt下
# 将busybox制作出来的bin  linuxrc  sbin  usr 拷贝,这里是下载源码配置（指定交叉编译工具链) 编译安装生成的_install目录
cp -r ~/develop/busybox/_install/* /mnt
# 将库文件拷贝,这里直接用的交叉编译工具的
cp -r /usr/arm-linux-gnueabi/lib/* /mnt
# 绘制启动时显示的图形
sudo cp ~/develop/myrootfs/etc/init.d/rcS /mnt/etc/init.d/

# 正式启动前一定要先卸载
sudo umount /mnt
```

## 制作Linux镜像
```sh
# 配置交叉工具链
# 在Linux源码顶级目录Makefile搜索cross
 ARCH            ?= arm
 CROSS_COMPILE   ?= arm-linux-gnueabi-

 # 编写配置文件（配置文件中主要是对一些宏开关的指定）
 # 这里直接使用了arch/arm/configs/vexpress_defconfig,然后老师做了一些调整,将配置文件粘贴到Linux主目录下
 # LDDD3_vexpress_defconfig这个就是微调后的配置文件，只有几百行
 cp arch/arm/configs/LDDD3_vexpress_defconfig .config
 # 可用可视化菜单进行二次配置,这里只是示范性的简单的修改了启动时的版本打印名字,在可视化菜单中用ctrl+backspace 删除
 # 配置完成后.config文件会自动刷新，这里再看的话就有上千行了
 make menuconfig

 # 编译内核镜像文件
 make zImage -j4
 # 编译模块文件
 make modules -j4
 # 编译设备树
 make dtbs

 # 将编译好的镜像文件和设备树文件拷贝到启动目录中 
 cp ./arch/arm/boot/zImage ./extra/
 cp ./arch/arm/boot/dts/*ca9.dtb ./extra/
```

