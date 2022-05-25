## ldd 列出可执行文件或者共享库依赖的共享库


## readelf
```cpp
-W    Allow output width to exceed 80 characters
-h    Display the ELF file header
-l    Display the program headers
-S    Display the sections' header
```

## objdump 将elf文件反汇编
```sh
-S:将其反汇编并且将其C语言源代码混合显示出来(编译时要加-g)
-s:将所有段的内容以十六进制的方式打印出来 
-d:将包含指令的段反汇编
```


## nm 查看符号表

## addr2line
用来将程序地址转换成其所对应的程序源文件及所对应的代码行，也可以得到所对应的函数。该工具将帮助调试器在调试的过程中定位对应的源代码位置。

## size
列出可执行文件每个部分的尺寸和总尺寸，代码段、数据段、总大小等。

## objcopy
将一种对象文件翻译成另一种格式，譬如将.bin转换成.elf、或者将.elf转换成.bin等。
