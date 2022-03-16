得到其他线程中计算的结果
```cpp
#include <iostream>
#include <future>

void task(int a, int b, std::promise<int> &ret)
{
    ret.set_value(a + b);
}

int main(int argc, char const *argv[])
{
    std::promise<int> p;
    std::future<int> f = p.get_future();
    std::thread t(task, 1, 2, std::ref(p));

    // do somethind

    // get the return value
    std::cout << "return value is " << f.get() << std::endl;
    t.join();
    return 0;
}
```


将稍后才会获取到的值作为参数传递进函数，函数可以先允许前面的一部分逻辑，然后阻塞在获取该参数的部分
```cpp
#include <iostream>
#include <future>

void task(int a, std::future<int> &b, std::promise<int> &ret)
{
    // do something
    ret.set_value(a + b.get());
}

int main(int argc, char const *argv[])
{
    std::promise<int> p;
    std::future<int> f = p.get_future();

    std::promise<int> p_in;
    std::future<int> f_in = p_in.get_future();
    std::thread t(task, 1, std::ref(f_in), std::ref(p));

    // do something
    p_in.set_value(2);

    // get the return value
    std::cout << "return value is " << f.get() << std::endl;
    t.join();
    return 0;
}
```

async
```cpp
#include <iostream>
#include <future>

int task(int a, int b)
{
    return a + b;
}

int main(int argc, char const *argv[])
{
    std::future<int> ret = std::async(task, 1, 2);
    // std::future<int> ret = std::async(std::launch::deferred, task, 1, 2); //在当前线程
    // std::future<int> ret = std::async(std::launch::async, task, 1, 2);    //开启新的线程

    // get the return value
    std::cout << "return value is " << ret.get() << std::endl;
    return 0;
}
```

