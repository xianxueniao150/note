mvn clean package依次执行了clean、resources、compile、testResources、testCompile、test、jar(打包)等７个阶段。
mvn clean install依次执行了clean、resources、compile、testResources、testCompile、test、jar(打包)、install等8个阶段。
mvn clean deploy依次执行了clean、resources、compile、testResources、testCompile、test、jar(打包)、install、deploy等９个阶段。

由上面的分析可知主要区别如下，
package命令完成了项目编译、单元测试、打包功能，但没有把打好的可执行jar包（war包或其它形式的包）布署到本地maven仓库和远程maven私服仓库
install命令完成了项目编译、单元测试、打包功能，同时把打好的可执行jar包（war包或其它形式的包）布署到本地maven仓库，但没有布署到远程maven私服仓库
deploy命令完成了项目编译、单元测试、打包功能，同时把打好的可执行jar包（war包或其它形式的包）布署到本地maven仓库和远程maven私服仓库

## 深入理解maven构建生命周期和各种plugin插件
https://blog.csdn.net/zhaojianting/article/details/80321488

## Maven 单独构建多模块项目中的子模块
```sh
-pl, --projects
    构建指定的模块，模块间用逗号分隔；适合无依赖的项目
-am, --also-make (常用)
    同时构建所列模块的依赖模块

	
首先切换到maven父项目目录 , 单独构建web-a , 同时会构建 web-a 依赖的其他模块
mvn install -pl web-a -am
```

## Maven打包跳过测试
```sh
# 不执行测试用例，也不编译测试用例类
mvn clean install -Dmaven.test.skip=true
# 不执行测试用例，但编译测试用例类生成相应的class文件至target/test-classes下
mvn clean install -DskipTests
```

## Intellij IDEA Cannot resolve symbol XXX 问题解决办法
在编译器中打开”Maven Projects “标签，先进行clean一下，在执行install

## 解决xml不打包
```java
<build>
    <resources>
        <!--解决maven不编译xml-->
        <resource>
            <directory>src/main/java</directory>
            <includes>
                <include>**/*.vm</include>
            </includes>
            <filtering>true</filtering>
        </resource>
    </resources>
</build>
```
