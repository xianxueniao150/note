默认的构造函数分为有用的和无用的，所谓无用的默认构造函数就是一个空函数、什么操作也不做，而有用的默认构造函数是可以初始化成员的函数。
对构造函数的需求也是分为两类：一类是编辑器需求，一类是程序的需求。
	程序的需求：若程序需求构造函数时，就是要程序员自定义构造函数来显示的初始化类的数据成员。
	编辑器的需求：编辑器的需求也分为两类：一类是无用的空的构造函数(trivial)，一类是编辑器自己合成的有用的构造函数(non-trivival)。


在用户没有自定义构造函数的情况下：
一、由于编辑器的需求，编辑器会生成空的无用的默认构造函数。
二、但在某些情况下,编辑器就一定会合有用的默认构造函数。