## 安装 TypeScript
TypeScript 的命令行工具安装方法如下：
`npm install -g typescript`
以上命令会在全局环境下安装 tsc 命令，安装完成之后，我们就可以在任何地方执行 tsc 命令了。

编译一个 TypeScript 文件很简单：
`tsc hello.ts`
我们约定使用 TypeScript 编写的文件以 .ts 为后缀，用 TypeScript 编写 React 时，以 .tsx 为后缀。

## 基本
TypeScript 只会在编译时对类型进行静态检查，如果发现有错误，编译的时候就会报错。而在运行时，与普通的 JavaScript 文件一样，不会对类型进行检查。

## tsconfig
如果一个目录下存在一个tsconfig.json文件，那么它意味着这个目录是TypeScript项目的根目录。 tsconfig.json文件中指定了用来编译这个项目的根文件和编译选项。 一个项目可以通过以下方式之一来编译：

### 使用tsconfig.json
- 不带任何输入文件的情况下调用tsc，编译器会从当前目录开始去查找tsconfig.json文件，逐级向上搜索父目录。
- 不带任何输入文件的情况下调用tsc，且使用命令行参数--project（或-p）指定一个包含tsconfig.json文件的目录。
- 当命令行上指定了输入文件时，tsconfig.json文件会被忽略。

在命令行上指定的编译选项会覆盖在tsconfig.json文件里的相应选项。

### 指定编译文件
"files"指定一个包含相对或绝对文件路径的列表。 
"include"和"exclude"属性指定一个文件glob匹配模式列表。 支持的glob通配符有：
>		- * 匹配0或多个字符（不包括目录分隔符）
>		- ? 匹配一个任意字符（不包括目录分隔符）
>		- **/ 递归匹配任意子目录
如果一个glob模式里的某部分只包含*或.*，那么仅有支持的文件扩展名类型被包含在内（比如默认.ts，.tsx，和.d.ts， 如果allowJs设置能true还包含.js和.jsx）。
如果没有特殊指定，"exclude"默认情况下会排除node_modules，bower_components，jspm_packages和<outDir>目录。
使用"include"引入的文件可以使用"exclude"属性过滤。 然而，通过"files"属性明确指定的文件却总是会被包含在内，不管"exclude"如何设置。 
任何被"files"或"include"指定的文件所引用的文件也会被包含进来。 A.ts引用了B.ts，因此B.ts不能被排除
需要注意编译器不会去引入那些可能做为输出的文件；比如，假设我们包含了index.ts，那么index.d.ts和index.js会被排除在外。 通常来讲，不推荐只有扩展名的不同来区分同目录下的文件。

### noEmitOnError
TypeScript 编译的时候即使报错了，还是会生成编译结果，我们仍然可以使用这个编译之后的文件。
如果要在报错的时候终止 js 文件的生成，可以在 tsconfig.json 中配置 noEmitOnError 即可。

## allowJs 允许编译 js 文件。
设置为 true 时，js 文件会被 tsc 编译，否则不会。一般在项目中 js, ts 混合开发时需要设置。

## allowSyntheticDefaultImports§
允许对不包含默认导出的模块使用默认导入。这个选项不会影响生成的代码，只会影响类型检查。

export = foo 是 ts 为了兼容 commonjs 创造的语法，它对应于 commonjs 中的 module.exports = foo。

在 ts 中，如果要引入一个通过 export = foo 导出的模块，标准的语法是 import foo = require('foo')，或者 import * as foo from 'foo'。

但由于历史原因，我们已经习惯了使用 import foo from 'foo'。

这个选项就是为了解决这个问题。当它设置为 true 时，允许使用 import foo from 'foo' 来导入一个通过 export = foo 导出的模块。当它设置为 false 时，则不允许，会报错。

当然，我们一般不会在 ts 文件中使用 export = foo 来导出模块，而是在写（符合 commonjs 规范的）第三方库的声明文件时，才会用到 export = foo 来导出类型。

比如 React 的声明文件中，就是通过 export = React 来导出类型：

export = React;
export as namespace React;

declare namespace React {
    // 声明 React 的类型
}
此时若我们通过 import React from 'react' 来导入 react 则会报错，查看示例 ：

import React from 'react';
// Module '"typescript-tutorial/examples/compiler-options/02-allowSyntheticDefaultImports/false/node_modules/@types/react/index"' can only be default-imported using the 'esModuleInterop' flagts(1259)
解决办法就是将 allowSyntheticDefaultImports 设置为 true。
