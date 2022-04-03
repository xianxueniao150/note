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
