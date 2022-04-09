## ES6 中类的用法§
使用 class 定义类，使用 constructor 定义构造函数。
通过 new 生成新实例的时候，会自动调用构造函数。
使用 extends 关键字实现继承，子类中使用 super 关键字来调用父类的构造函数和方法。

### 存取器§
使用 getter 和 setter 可以改变属性的赋值和读取行为：

```javascript
class Animal {
  constructor(name) {
    this.name = name;
  }
  get name() {
    return 'Jack';
  }
  set name(value) {
    console.log('setter: ' + value);
  }
}

let a = new Animal('Kitty'); // setter: Kitty
a.name = 'Tom'; // setter: Tom
console.log(a.name); // Jack
```

## TypeScript 中类的用法
TypeScript 编译之后的代码中，并没有限制 private 属性在外部的可访问性。

### 参数属性§
修饰符和readonly还可以使用在构造函数参数中，等同于类中定义该属性同时给该属性赋值，使代码更简洁。
```javascript
class Animal {
  // public name: string;
  public constructor(public name) {
    // this.name = name;
  }
}
```

### readonly§
只读属性关键字，只允许出现在属性声明或索引签名或构造函数中。
注意如果 readonly 和其他访问修饰符同时存在的话，需要写在其后面。


