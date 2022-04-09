SWAP就是LINUX下的虚拟内存分区,它的作用是在 物理内存使用完之后,将磁盘空间(也就是SWAP分区)虚拟成内存来使用.

临时创建交换文件
```sh
sudo dd if=/dev/zero of=/swapfile bs=1M count=2048  #创建大小为2G的交换文件
sudo mkswap /swapfile    #设置交换文件
sudo swapon /swapfile 
```

删除上面临时创建的
```sh
sudo swapoff /swapfile
sudo rm /swapfile
```


