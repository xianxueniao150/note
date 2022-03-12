cherry-pick
假设你现在正在开发一个项目，有一个功能分支 feature，开发分支 develop。 feature 有3个提交，分别是 A ，B ，C 。develop 分支只想加入 C 功能， 此时合并操作无法满足，因为直接合并 feature，会将3个提交都合并上，我想合并就只有 C，不要 A，B。此时就需要挑樱桃大法–cherry pick！

### 具体的做法：
1. 切换到 develop 分支。
2. 通过 git log feature,找到 C 的 SHA1 值。
3. 通过 git cherry-pick <C的SHA1> ，将 C 的修改内容合并到当前内容分支 develop 中。
4. 若无冲突，过程就已经完成了。如果有冲突，按正常冲突解决流程即可。

如果某文件是C新增的文件，则一般不会冲突，如果不是，可能会连带着引入之前提交对该文件的修改


### 转移多个提交
Cherry pick 支持一次转移多个提交。
```sh
# 将 A 和 B 两个提交应用到当前分支。这会在当前分支生成两个对应的新提交。
$ git cherry-pick <HashA> <HashB>
# 转移从 A 到 B 的所有提交。
$ git cherry-pick A..B 
# 注意，使用上面的命令，提交 A 将不会包含在 Cherry pick 中。如果要包含提交 A，可以使用下面的语法。
$ git cherry-pick A^..B
```

### 配置项
git cherry-pick命令的常用配置项如下。

（1）-e，--edit

打开外部编辑器，编辑提交信息。

（2）-n，--no-commit

只更新工作区和暂存区，不产生新的提交。

（3）-x

在提交信息的末尾追加一行(cherry picked from commit ...)，方便以后查到这个提交是如何产生的。

（4）-s，--signoff

在提交信息的末尾追加一行操作者的签名，表示是谁进行了这个操作。

（5）-m parent-number，--mainline parent-number

如果原始提交是一个合并节点，来自于两个分支的合并，那么 Cherry pick 默认将失败，因为它不知道应该采用哪个分支的代码变动。

-m配置项告诉 Git，应该采用哪个分支的变动。它的参数parent-number是一个从1开始的整数，代表原始提交的父分支编号。


$ git cherry-pick -m 1 <commitHash>
上面命令表示，Cherry pick 采用提交commitHash来自编号1的父分支的变动。

一般来说，1号父分支是接受�动的分支（the branch being merged into），2号父分支是作为变动来源的分支（the branch being merged from）。�
