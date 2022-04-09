## 原始数据类型
### 空值
JavaScript 没有空值（Void）的概念，在 TypeScript 中，可以用 void 表示没有任何返回值的函数：
function alertName(): void {
    alert('My name is Tom');
}

### Null 和 Undefined
在 TypeScript 中，可以使用 null 和 undefined 来定义这两个原始数据类型，undefined 和 null 是所有类型的子类型。也就是说 undefined 类型的变量，可以赋值给 number 类型的变量

## 任意值
任意值（Any）用来表示允许赋值为任意类型。

如果是一个普通类型，在赋值过程中改变类型是不被允许的：
```javascript
let myFavoriteNumber: string = 'seven';
myFavoriteNumber = 7;

// index.ts(2,1): error TS2322: Type 'number' is not assignable to type 'string'.
```
但如果是 any 类型，则允许被赋值为任意类型。
```javascript
let myFavoriteNumber: any = 'seven';
myFavoriteNumber = 7;
```

在任意值上访问任何属性都是允许的：
```cpp
let anyThing: any = 'hello';
console.log(anyThing.myName);
```
也允许调用任何方法：
可以认为，声明一个变量为任意值之后，对它的任何操作，返回的内容的类型都是任意值。

变量如果在声明的时候，未指定其类型，那么它会被识别为任意值类型：
```javascript
let something;
something = 'seven';
something = 7;
```

## 类型推论
如果没有明确的指定类型，那么 TypeScript 会依照类型推论（Type Inference）的规则推断出一个类型。
如果定义的时候没有赋值，不管之后有没有赋值，都会被推断成 any 类型而完全不被类型检查：

## 联合类型
联合类型（Union Types）表示取值可以为多种类型中的一种。
联合类型使用 | 分隔每个类型。
```javascript
let myFavoriteNumber: string | number;
myFavoriteNumber = 'seven';
myFavoriteNumber = 7;
```
这里的 let myFavoriteNumber: string | number 的含义是，允许 myFavoriteNumber 的类型是 string 或者 number，但是不能是其他类型。

访问联合类型的属性或方法
当 TypeScript 不确定一个联合类型的变量到底是哪个类型的时候，我们只能访问此联合类型的所有类型里共有的属性或方法：
```javascript
function getLength(something: string | number): number {
    return something.length;
}

// index.ts(2,22): error TS2339: Property 'length' does not exist on type 'string | number'.
//   Property 'length' does not exist on type 'number'.
```
上例中，length 不是 string 和 number 的共有属性，所以会报错。

访问 string 和 number 的共有属性是没问题的：
```javascript
function getString(something: string | number): string {
    return something.toString();
}
```

联合类型的变量在被赋值的时候，会根据类型推论的规则推断出一个类型：
```javascript
let myFavoriteNumber: string | number;
myFavoriteNumber = 'seven';
console.log(myFavoriteNumber.length); // 5
myFavoriteNumber = 7;
console.log(myFavoriteNumber.length); // 编译时报错

// index.ts(5,30): error TS2339: Property 'length' does not exist on type 'number'.
```
上例中，第二行的 myFavoriteNumber 被推断成了 string，访问它的 length 属性不会报错。
而第四行的 myFavoriteNumber 被推断成了 number，访问它的 length 属性时就报错了

## 对象的类型——接口
在 TypeScript 中，我们使用接口（Interfaces）来定义对象的类型。
TypeScript 中的接口是一个非常灵活的概念，除了可用于对类的一部分行为进行抽象以外，也常用于对「对象的形状（Shape）」进行描述。
```javascript
interface Person {
    name: string;
    age: number;
}

let tom: Person = {
    name: 'Tom',
    age: 25
};
```
上面的例子中，我们定义了一个接口 Person，接着定义了一个变量 tom，它的类型是 Person。这样，我们就约束了 tom 的形状必须和接口 Person 一致。

定义的变量比接口少了一些属性是不允许的：
多一些属性也是不允许的：

### 可选属性
有时我们希望不要完全匹配一个形状，那么可以用可选属性：
```javascript
interface Person {
    name: string;
    age?: number;
}

let tom: Person = {
    name: 'Tom'
};
```
可选属性的含义是该属性可以不存在。
这时仍然不允许添加未定义的属性：

## 任意属性
我们在自定义类型的时候，有可能会希望一个接口允许有任意的属性签名，这时候 任意属性 就派上用场了。
任意属性有两种定义的方式：一种属性签名是 string 类型的，另一种属性签名是 number 类型的。

### string 类型任意属性
第一种，属性签名是 string，比如对象的属性：
```javascript
interface A {
    [prop: string]: number;
}

const obj: A = {
    a: 1,
    b: 3,
};
```
[prop: string]: number 的意思是，A 类型的对象可以有任意属性签名，string 指的是对象的键都是字符串类型的，number 则是指定了属性值的类型。
prop 类似于函数的形参，是可以取其他名字的。

### number 类型任意属性
第二种，属性签名是 number 类型的，比如数组下标：
```javascript
interface B {
    [index: number]: string;
}

const arr: B = ['suukii'];
```
[index: number]: string 的意思是，B 类型的数组可以有任意的数字下标，而且数组的成员的类型必须是 string。
同样的，index 也只是类似于函数形参的东西，用其他标识符也是完全可以的。

### 同时定义两种任意属性
需要注意的是，一个接口可以同时定义这两种任意属性，但是 number 类型的签名指定的值类型必须是 string 类型的签名指定的值类型的子集，举个例子：

```javascript
interface C {
    [prop: string]: number;
    [index: number]: string;
}

// Numeric index type 'string' is not assignable to string index type 'number'.
```
上面定义是不成立的，因为 index 指定的值类型是 string，而 prop 指定的值类型是 number，string 并不是 number 的子集。

### 同时定义任意属性和其他类型的属性
另外还有一个需要注意的点，一旦定义了任意属性，那么其他属性(确定属性、可选属性、只读属性等)的类型都必须是它的类型的子集。
```javascript
interface Person {
    name: string;
    age?: number;
    [prop: string]: string;
}

// Property 'age' of type 'number' is not assignable to string index type 'string'.
```
但其实这样子的定义是不成立的，因为 [prop: string]: string 的存在，规定了其他属性的类型也必须是 string，如果想要解决报错，我们可以使用联合类型：
```javascript
interface Person {
    name: string;
    age?: number;
    [prop: string]: string | number;
}
```

对于 number 类型的任意属性签名，情况也是一样的：
```javascript
type MyArray = {
    0: string;
    [index: number]: number;
};
// Property '0' of type 'string' is not assignable to numeric index type 'number'.
```
但是，number 类型的任意属性签名不会影响其他 string 类型的属性签名：
```javascript
type Arg = {
    [index: number]: number;
    length: string;
};
```
如上，虽然指定了 number 类型的任意属性的类型是 number，但 length 属性是 string 类型的签名，所以不受前者的影响。

但是反过来就不一样了，如果接口定义了 string 类型的任意属性签名，它不仅会影响其他 string 类型的签名，也会影响其他 number 类型的签名。这一点可以参考两种任意类型签名并存时，number 类型的签名指定的值类型必须是 string 类型的签名指定的值类型的子集这句话。

### 只读属性§
有时候我们希望对象中的一些字段只能在创建的时候被赋值，那么可以用 readonly 定义只读属性：
注意，只读的约束存在于第一次给对象赋值的时候，而不是第一次给只读属性赋值的时候：
```javascript
interface Person {
    readonly id: number;
    name: string;
    age?: number;
    [propName: string]: any;
}

let tom: Person = {
    name: 'Tom',
    gender: 'male'
};

tom.id = 89757;

// index.ts(8,5): error TS2322: Type '{ name: string; gender: string; }' is not assignable to type 'Person'.
//   Property 'id' is missing in type '{ name: string; gender: string; }'.
// index.ts(13,5): error TS2540: Cannot assign to 'id' because it is a constant or a read-only property.
```
上例中，报错信息有两处，第一处是在对 tom 进行赋值的时候，没有给 id 赋值。
第二处是在给 tom.id 赋值的时候，由于它是只读属性，所以报错了。

## 函数的类型
一个函数有输入和输出，要在 TypeScript 中对其进行约束，需要把输入和输出都考虑到，其中函数声明的类型定义较简单：
```javascript
function sum(x: number, y: number): number {
    return x + y;
}
```

### 用接口定义函数的形状§
我们也可以使用接口的方式来定义一个函数需要符合的形状：
```javascript
interface SearchFunc {
    (source: string, subString: string): boolean;
}

let mySearch: SearchFunc;
mySearch = function(source: string, subString: string) {
    return source.search(subString) !== -1;
}
```

### 可选参数§
与接口中的可选属性类似，我们用 ? 表示可选的参数：
需要注意的是，可选参数必须接在必需参数后面。

在 ES6 中，我们允许给函数的参数添加默认值，TypeScript 会将添加了默认值的参数识别为可选参数：

```javascript
function buildName(firstName: string, lastName: string = 'Cat') {
    return firstName + ' ' + lastName;
}
let tomcat = buildName('Tom', 'Cat');
let tom = buildName('Tom');
```
此时就不受「可选参数必须接在必需参数后面」的限制了：


### 剩余参数§
ES6 中，可以使用 ...rest 的方式获取函数中的剩余参数（rest 参数）：
```javascript
function push(array, ...items) {
    items.forEach(function(item) {
        array.push(item);
    });
}

let a: any[] = [];
push(a, 1, 2, 3);
```

事实上，items 是一个数组。所以我们可以用数组的类型来定义它：
```javascript
function push(array: any[], ...items: any[]) {
    items.forEach(function(item) {
        array.push(item);
    });
}
```
注意，rest 参数只能是最后一个参数，关于 rest 参数，可以参考 ES6 中的 rest 参数。


## 类型断言
类型断言（Type Assertion）可以用来手动指定一个值的类型。
### 语法§
> ```值 as 类型```
> 或
> ```<类型>值```

### 类型断言的用途§

#### 将一个联合类型断言为其中一个类型§
之前提到过，当 TypeScript 不确定一个联合类型的变量到底是哪个类型的时候，我们只能访问此联合类型的所有类型中共有的属性或方法：
而有时候，我们确实需要在还不确定类型的时候就访问其中一个类型特有的属性或方法，比如：
```javascript
interface Cat {
    name: string;
    run(): void;
}
interface Fish {
    name: string;
    swim(): void;
}

function isFish(animal: Cat | Fish) {
    if (typeof animal.swim === 'function') {
        return true;
    }
    return false;
}

// index.ts:11:23 - error TS2339: Property 'swim' does not exist on type 'Cat | Fish'.
//   Property 'swim' does not exist on type 'Cat'.
```
上面的例子中，获取 animal.swim 的时候会报错。

此时可以使用类型断言，将 animal 断言成 Fish：
```javascript
function isFish(animal: Cat | Fish) {
    if (typeof (animal as Fish).swim === 'function') {
        return true;
    }
    return false;
}
```
这样就可以解决访问 animal.swim 时报错的问题了。

需要注意的是，类型断言只能够「欺骗」TypeScript 编译器，无法避免运行时的错误，反而滥用类型断言可能会导致运行时错误：
```javascript
function swim(animal: Cat | Fish) {
    (animal as Fish).swim();
}

const tom: Cat = {
    name: 'Tom',
    run() { console.log('run') }
};
swim(tom);
// Uncaught TypeError: animal.swim is not a function`
```
上面的例子编译时不会报错，但在运行时会报错：

#### 将任何一个类型断言为 any§
理想情况下，TypeScript 的类型系统运转良好，每个值的类型都具体而精确。
当我们引用一个在此类型上不存在的属性或方法时，就会报错. 这种错误提示显然是非常有用的。

但有的时候，我们非常确定这段代码不会出错，比如下面这个例子：
```javascript
window.foo = 1;

// index.ts:1:8 - error TS2339: Property 'foo' does not exist on type 'Window & typeof globalThis'.
```
上面的例子中，我们需要将 window 上添加一个属性 foo，但 TypeScript 编译时会报错，提示我们 window 上不存在 foo 属性。

此时我们可以使用 as any 临时将 window 断言为 any 类型：
> ```(window as any).foo = 1;```

在 any 类型的变量上，访问任何属性都是允许的。

需要注意的是，将一个变量断言为 any 可以说是解决 TypeScript 中类型问题的最后一个手段。
它极有可能掩盖了真正的类型错误，所以如果不是非常确定，就不要使用 as any。


#### 将 any 断言为一个具体的类型§
在日常的开发中，我们不可避免的需要处理 any 类型的变量，它们可能是由于第三方库未能定义好自己的类型，也有可能是历史遗留的或其他人编写的烂代码，还可能是受到 TypeScript 类型系统的限制而无法精确定义类型的场景。

遇到 any 类型的变量时，我们可以选择无视它，任由它滋生更多的 any。
我们也可以选择改进它，通过类型断言及时的把 any 断言为精确的类型，亡羊补牢，使我们的代码向着高可维护性的目标发展。

