## 拉取远程分支到本地
### 方式一
By using the "--track" parameter, you can use a remote branch as the basis for a new local branch;
this will also set up a "tracking relationship" between the two:
```
$ git checkout -b ac_branch --track origin/ac_branch  
```
有可能出现错误提示：
fatal: 'origin/ac_branch' is not a commit and a branch 'ac_branch' cannot be created from it

解决方式:
执行命令：git fetch    同步一下仓库

方式一做了三件事：
1. 拉取远程分支到本地
2. 在本地创建一个分支与远程分支对应
3. 自动切换到刚创建好的分支

### 方式二
```
git fetch origin ac_branch:ac_branch
```

方式二做了三件事：
1. 同步远程仓库（git fetch origin）
2. 拉取远程分支到本地
3. 在本地创建一个分支与远程分支对应


```sh
# 查看本地分支
git branch  
# 查看远程分支
git branch -r  
# 查看所有分支
git branch -a  

# 创建branch 
git branch 名称
# 切换branch,如果有未提交的修改，不允许切换
git checkout 名称（将HEAD指向该branch）
# 创建+切换，工作目录和暂存区的修改会移到新分支，旧分支会清除掉这部分内容
git checkout -b 名称

# 重命名branch 
git branch -m <branch>
# 删除branch,出于安全考虑，没有被合并到 master 过的 branch 在删除时会失败（怕误删未完成branch）把-d换成-D可以强制删除
git branch -d 名称
```

```sh
# 拉取所有远程分支
git fetch   
# 联网查看远程仓库的信息，如果和本机存储的不一致，会有提示命令如何同步
git remote show origin 

# 切换远程仓库地址
git remote set-url origin url

# 查看本地分支落后于远程分支多少
git branch -vv  
```

## git push 命用于从将本地的分支版本上传到远程并合并。
```sh
# 命令格式如下：
git push <远程主机名> <本地分支名>:<远程分支名>
# 如果本地分支名与远程分支名相同，则可以省略冒号：
git push <远程主机名> <本地分支名>

# To prevent you from overwriting commits, Git won’t let you push when it results in a non-fast-forward merge in the destination repository
git push <remote> --force

# The --tags flag sends all of your local tags to the remote repository
git push <remote> --tags
```


1. a
2. b
3. c
4. d
