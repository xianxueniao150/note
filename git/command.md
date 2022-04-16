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

