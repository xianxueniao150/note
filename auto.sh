
set -u
set -x
set -e



git add .

commitMessage=$(date "+%Y-%m-%d")
if [ $# -eq 1 ];then
    $commitMessage=$1
fi

git commit -m $commitMessage
git push
