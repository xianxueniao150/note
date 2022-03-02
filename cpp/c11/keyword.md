## final
C++11的关键字final有两个用途。第一，它阻止了从类继承；第二，阻止一个虚函数的重载。我们先来看看final类吧。

在C++11中，无子类类型将被声明为如下所示：
```cpp
class TaskManager {/*..*/} final; 
class PrioritizedTaskManager: public TaskManager {
};  //compilation error: base class TaskManager is final
```

同样，你可以通过声明它为final来禁止一个虚函数被进一步重载。如果一个派生类试图重载一个final函数，编译器就会报错：
```cpp
class A
{
pulic:
  virtual void func() const;
};
class  B: A
{
pulic:
  void func() const override final; //OK
};
class C: B
{
pulic:
 void func()const; //error, B::func is final
};
```

## override
在派生类中，重写 (override) 继承自基类成员函数的实现 (implementation) 时，要满足如下条件：
*   一虚：基类中，成员函数声明为虚拟的 (virtual)
*   二容：基类和派生类中，成员函数的返回类型和异常规格 (exception specification) 必须兼容
*   四同：基类和派生类中，成员函数名、形参类型、常量属性 (constness) 和 引用限定符 (reference qualifier) 必须完全相同
	
  如此多的限制条件，导致了虚函数重写如上述代码，极容易因为一个不小心而出错
  C++11 中的 override 关键字，可以显式的在派生类中声明，哪些成员函数需要被重写，如果没被重写，则编译器会报错。 
