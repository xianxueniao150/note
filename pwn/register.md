```sh
rsp 指向栈顶位置
rbp 指向栈底,保存的是上一个函数的栈底，再高一处保存的是return address(即当前函数结束后下一句要执行的代码)
rip 存放当前执行的指令的地址
eap 保存函数的返回值
```


```sh
pop    寄存器        ;出栈用一个寄存器接收出栈的数据
leave 				 等效于MOV ESP, EBP; POP EBP
RET					 等效于：POP RIP（这条指令实际是不存在的，不能直接向RIP寄存器传送数据）
```


栈是由高往低增长
## 函数调用时,栈的变化
1.首先此时还是在调用函数(caller)的栈中。
	1) 调用函数会将被调函数(callee)的参数按照逆序依次压入栈内，即先压arg2，再压arg1。
	2) 然后将调用返回时要执行的下一条指令地址压栈。
	3) 再将当前的ebp 寄存器的值（也就是调用函数的基地址）压入栈内，并将 ebp 寄存器的值更新为当前栈顶的地址。这样调用函数（caller）的 ebp（基地址）信息得以保存。同时，ebp 被更新为被调用函数（callee）的基地址。
2.此时来到了callee的栈中
	1) 将callee的局部变量压入栈内
	
调用完成后
1.callee的局部变量会从栈内直接弹出，栈顶会指向被调用函数（callee）的基地址
2.然后将基地址内存储的调用函数（caller）的基地址从栈内弹出，并存到 ebp 寄存器内。这样调用函数（caller）的 ebp（基地址）信息得以恢复。此时栈顶会指向返回地址。
3.再将返回地址从栈内弹出，并存到 eip 寄存器内。这样调用函数（caller）的 eip（指令）信息得以恢复。
