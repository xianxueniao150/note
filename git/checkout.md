Git Checkout Commit
```sh
git checkout <commit hash>
git checkout <tag name>
# checkout a Git tag as a branch in the terminal
git checkout -b <branch name> <tag name>


# Restores a historic revision of a given file
git checkout <commit-hash> <file-path> 
# If you specify "HEAD" as the revision, you will restore the last committed version of the file,
# effectively undoing any local changes that you current have in that file:
$ git checkout HEAD index.html
```
如果有未提交的文件的话，会提示你commit。
Git Detached HEAD
It’s important to be aware: checking out a Git commit or a Git tag will move the HEAD point to a commit instead of a branch.
This will put your repository in what’s called detached HEAD state.

1. When you are in detached HEAD state in Git, you are not able to commit changes to a branch.
2.  You can look around, make experimental changes and commit them, and you can discard any commits you make in this
3.  state without impacting any branches by performing another checkout.
 
 If you want to create a new branch to retain commits you create, you may
 do so (now or later) by using -b with the checkout command again. Example:
 

 git checkout -b 
