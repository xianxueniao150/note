```sh
# 配置用户名
git config --global user.name "用户名"
# 配置邮箱
git config --global user.email "邮箱地址"
# 查看所有配置
git config -l

# 配置代理
git config --global http.proxy 'socks5://127.0.0.1:1080' 
git config --global https.proxy 'socks5://127.0.0.1:1080'

 git config --global core.editor "vim"
 git config --global alias.lg "log --color --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit"

```
