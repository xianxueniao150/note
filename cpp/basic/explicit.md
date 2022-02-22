explicit的作用是用来声明类构造函数是显示调用的，而非隐式调用，所以只用于修饰单参构造函数。
因为无参构造函数和多参构造函数本身就是显示调用的。再加上explicit关键字也没有什么意义。

```cpp
class Circle
{
public:
    Circle(double r) : R(r) {}
    Circle(int x, int y = 0) : X(x), Y(y) {}
    Circle(const Circle &c) : R(c.R), X(c.X), Y(c.Y) {}

private:
    double R;
    int X;
    int Y;
};

int main(int argc, char const *argv[])
{
    //发生隐式类型转换,编译器会将它变成如下代码 Circle(1.23)
    Circle A = 1.23;
    //注意是int型的，调用的是Circle(int x, int y = 0)
    //它虽然有2个参数，但后一个有默认值，任然能发生隐式转换
    Circle B = 123;
    //这个算隐式调用了拷贝构造函数
    Circle C = A;
	
    //给上述构造函数加了explicit后只能这样了
    Circle A(1.23);
    Circle B(123);
    Circle C(A);
	
    return 0;
}
```
