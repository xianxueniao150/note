## 安装 Homebrew
Homebrew 作为 macOS 不可或缺的套件管理器，用来安装、升级以及卸载常用的软件。在命令行中执行以下命令即可安装：
```sh
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)" # 使用系统自带的 ruby 安装 Homebrew
```


安装后可以修改 Homebrew 源，国外源一直不是很给力，这里我们将 Homebrew 的 git 远程仓库改为中国科学技术大学开源软件镜像：
```sh
cd "$(brew --repo)"
git remote set-url origin https://mirrors.ustc.edu.cn/brew.git # 替换brew.git:

cd "$(brew --repo)/Library/Taps/homebrew/homebrew-core"
git remote set-url origin https://mirrors.ustc.edu.cn/homebrew-core.git # 替换homebrew-core.git:

echo 'export HOMEBREW_BOTTLE_DOMAIN=https://mirrors.ustc.edu.cn/homebrew-bottles' >> ~/.zshrc # 替换Homebrew Bottles源:

source ~/.zshrc
```

