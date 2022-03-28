终端就像文件，可以对该文件使用任何与文件相关的命令
```sh
#终端1
$ tty
/dev/ttys023

#终端2
$ echo "aaaaa" > /dev/ttys023

#终端1
$ aaaaa
```
