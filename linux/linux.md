## Shell 输入/输出重定向
```python
command > file  	 将输出重定向到 file。
command < file  	 将输入重定向到 file。
command >> file 	 将输出以追加的方式重定向到 file。
n > file        	 将文件描述符为 n 的文件重定向到 file。
n >> file       	 将文件描述符为 n 的文件以追加的方式重定向到 file。
n >& m          	 将输出文件 m 和 n 合并。
n <& m          	 将输入文件 m 和 n 合并。
```

```sh
# 如果希望 stderr 重定向到 file，可以这样写：
$ command 2>file
# 2 表示标准错误文件(stderr)。

# 如果希望将 stdout 和 stderr 合并后重定向到 file，可以这样写：
$ command > file 2>&1
```

## 将Linux命令的结果作为下一个命令的参数
### 管道符
使用管道操作符”|”（竖杠），一个命令的标准输出可以通过管道送至另一个命令的标准输入：
```cpp
command1 | command2
```

### exec  将前面的结果交给后面命令去执行
```cpp
-exec command {} ;

find ~ -type f -name 'foo*' -exec rm '{}' ';'
find ~ -type f -name 'foo*' -exec ls -l '{}' ';'
```

1. 符号：` `
作用：反引号括起来的字符串被shell解释为命令行，在执行时，shell首先执行该命令行，并以它的标准输出结果取代整个反引号（包括两个反引号）部分

2. $()
效果同` `

3. 命令：xargs
|是将标准输出转化为标准输入传给后面命令
xargs是将标准输入转化为命令行参数
| xargs一起用，就是标准输出转化为标准输入，再转化为命令行参数（即 标准输出转化为命令行参数）

一个处理字符串的命令，它的输入通常分为三种
- 传入字符串内容本身
- 传入一个文件名
- 标准输入


1、接受内容本身作为输入# upper.py
```python
import sys
text = sys.argv[1]
print(text.upper())
```

2、接受文件名作为输入# upper_filename.py
```python
import sys
filename = sys.argv[1]
with open(filename, 'r') as f:
    for line in f:
        print(line.strip().upper())
```

3、接受标准输入# upper_stdin.py
```python
import sys
for line in sys.stdin.readlines():
    print(line.strip().upper())
```

4、接受文件名或标准输入：如果有传参数就当做文件名，没有就接受标准输入# upper_file.py
```python
import sys
if len(sys.argv) == 2:
    filename = sys.argv[1]
    with open(filename, 'r') as f:
        for line in f:
            print(line.strip().upper())
else:
    for line in sys.stdin.readlines():
        print(line.strip().upper())
```

---接受标准输入的程序直接运行是什么效果呢？它会等用户输入一段字符，输入完成后用Ctrl+D(Unix)或Ctrl+Z(Windows)停止输入，程序就会处理这段字符并输出。
```
python upper_file.py
abc
bcd
>> Ctrl+D(Unix)或Ctrl+Z(Windows)
ABC
BCD
```

如果去试一下cat会发现不一样，它是每输入一行就处理一下并返回，就像提供了一个即时处理的窗口。它的内部程序大概是这样的import sys
```
for line in sys.stdin:
    print(line.strip().upper()) 
```
运行情况如下
```
python upper_stdin.py
abc
ABC
bcd
BCD
>> Ctrl+D(Unix)或Ctrl+Z(Windows)
```
