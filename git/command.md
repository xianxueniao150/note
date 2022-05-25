## git设置只在本地忽略某些文件
```sh
git update-index --skip-worktree <file-list>
# Reverse it by:
git update-index --no-skip-worktree <file-list>
```

## 单独设置push地址
```sh
git remote set-url --add --push origin git@github.com:MY_REPOSITY/dnmp.git
```

## 浅clone
```sh
--depth 1
```

## 查看项目远程地址
```sh
git remote -v
```

## tag
```sh
# 列出标签
$ git tag

# 创建标签, 默认标签是打在最新提交的commit上的。
git tag <name>

# 一次性推送全部尚未推送到远程的本地标签：
$ git push origin --tags
```

## git命令将文件夹移到另一个文件夹中
不需要显式跟踪文件重命名。 Git会通过比较文件的内容来弄明白。
```cpp
$ mkdir include
$ mv common include
$ git rm -r common
$ git add include/common
```

运行git status应该会显示如下：
```sh
$ git status
# On branch master
# Changes to be committed:
#   (use "git reset HEAD <file>..." to unstage)
#
#   renamed:    common/file.txt -> include/common/file.txt
#
```
