## 虚函数
```cpp
#include <iostream>
using namespace std;

class Parent
{
public:
    Parent(string n = "Parent") { name = n; }

    //子类自动继承,子类如果重写，只要实际指向的对象为子类，输出的便是子类的
    virtual void Speak()
    {
        cout << "\tI am " << name << ", I am parent" << endl;
    }

    virtual void Run()
    {
        cout << "\tI am " << name << ", I run" << endl;
    }

    //子类自动继承,但子类即使重写，只要调用的对象为父类，输出的仍然是父类的
    void Work()
    {
        cout << "\tI am " << name << ", I need to do official work" << endl;
    }

    void Sleep()
    {
        cout << "\tI am " << name << ", I sleep" << endl;
    }

protected:
    string name;
};

class Child : public Parent
{
public:
    Child(string n = "Child") : Parent(n) {}

    virtual ~Child() {}

    virtual void Speak()
    {
       cout << "\tI am " << name << ", I am child" << endl;
    }

    void Work()
    {
        cout << "\tI am " << name << ", I need to do part-time work" << endl;
    }
};

int main(int argc, char const *argv[])
{
    cout << "p1-------------------------" << endl;
    Parent *p1 = new Child();
    p1->Work();  //I am Child, I need to do official work
    p1->Speak(); //I am Child, I am child

    cout << "p2-------------------------" << endl;
    Child *p2 = new Child();
    p2->Work();  //I am Child, I need to do part-time work
    p2->Sleep(); //I sleep
    p2->Run();   //I run

    return 0;
} 
```
