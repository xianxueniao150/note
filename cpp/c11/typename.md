typename用于泛型中,表明其后紧接着的那个标识符是一个类型,而不是一个变量。

## 类作用域
在类外部访问类中的名称时，可以使用类作用域操作符，形如MyClass::name的调用通常存在三种：静态数据成员、静态成员函数和嵌套类型：
```cpp
struct MyClass {
    static int A;
    static int B();
    typedef int C;
}
```

MyClass::A, MyClass::B, MyClass::C分别对应着上面三种。

## 引入typename的真实原因
一个例子
在Stroustrup起草了最初的模板规范之后，人们更加无忧无虑的使用了class很长一段时间。可是，随着标准化C++工作的到来，人们发现了模板这样一种定义：
```cpp
template <class T>
void foo() {
    T::iterator * iter;
    // ...
}
```
这段代码的目的是什么？多数人第一反应可能是：作者想定义一个指针iter，它指向的类型是包含在类作用域T中的iterator。可能存在这样一个包含iterator类型的结构：
```cpp
struct ContainsAType {
    struct iterator { /*...*/ };
    // ...
};
```
然后像这样实例化foo：
```cpp
foo<ContainsAType>();
```
这样一来，iter那行代码就很明显了，它是一个ContainsAType::iterator类型的指针。到目前为止，咱们猜测的一点不错，一切都看起来很美好。

问题浮现
像T::iterator这样？T是模板中的类型参数，它只有等到模板实例化时才会知道是哪种类型，更不用说内部的iterator。通过前面类作用域一节的介绍，我们可以知道，T::iterator实际上可以是以下三种中的任何一种类型：
*  静态数据成员
*  静态成员函数
*  嵌套类型
	
前面例子中的ContainsAType::iterator是嵌套类型，完全没有问题。可如果是静态数据成员呢？如果实例化foo模板函数的类型是像这样的：
```cpp
struct ContainsAnotherType {
    static int iterator;
    // ...
};
```
然后如此实例化foo的类型参数：

foo<ContainsAnotherType>();
那么，T::iterator * iter;被编译器实例化为ContainsAnotherType::iterator * iter;，这是什么？前面是一个静态成员变量而不是类型，那么这便成了一个乘法表达式，只不过iter在这里没有定义，编译器会报错：

error C2065: ‘iter’ : undeclared identifier

但如果iter是一个全局变量，那么这行代码将完全正确，它是表示计算两数相乘的表达式，返回值被抛弃。

同一行代码能以两种完全不同的方式解释，而且在模板实例化之前，完全没有办法来区分它们，这绝对是滋生各种bug的温床。这时C++标准委员会再也忍不住了，与其到实例化时才能知道到底选择哪种方式来解释以上代码，委员会决定引入一个新的关键字，这就是typename。

如果你想直接告诉编译器T::iterator是类型而不是变量，只需用typename修饰：
```cpp
template <class T>
void foo() {
    typename T::iterator * iter;
    // ...
}
```
这样编译器就可以确定T::iterator是一个类型，而不再需要等到实例化时期才能确定，因此消除了前面提到的歧义。


