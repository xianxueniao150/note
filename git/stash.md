https://www.atlassian.com/git/tutorials/saving-changes/git-stash

git stash 只作用于工作目录和暂存区，不会影响已经commit的，执行stash命令后所有更改将会消失，将stash pop后如果存在冲突，不会提示解决冲突，而是会提醒你先把当前未commit的修改另存或者commit
```shell
# 新增stash, -u: stash untracked files   -a: stash ignored files
$ git stash save "test-cmd-stash"

$ git stash list

# 将指定stash删除，并将对应修改应用到当前的工作目录下,默认是第一个
$ git stash pop
# 应用指定的的stash, 但并不删除
$ git stash apply

# 移除指定的stash
$ git stash drop stash@{0}
# 删除所有缓存的stash
git stash clear

# Viewing stash diffs, pass the -p option to view the full diff of a stash
$ git stash show 

# Creating a branch from your stash
$ git stash branch branch_name stash@{1}
```

git stash temporarily shelves (or stashes) changes you've made to your working copy so you can work on something else, and then come back and re-apply them later on. Stashing is handy if you need to quickly switch context and work on something else, but you're mid-way through a code change and aren't quite ready to commit.

## Stashing untracked or ignored files

By default, running `git stash` will stash:		

- changes that have been added to your index (staged changes)
- changes made to files that are currently tracked by Git (unstaged changes)

But it will **not** stash:

- new files in your working copy that have not yet been staged
- files that have been ignored

So if we add a third file to our example above, but don't stage it (i.e. we don't run `git add`), `git stash` won't stash it.
Adding the `-u` option (or `--include-untracked`) tells `git stash` to also stash your untracked files

You can include changes to ignored when running `git stash`.

![Git Stash options](image/01-20210912124535094.svg){:height="30%" width="30%"}



## Managing multiple stashes

By default, stashes are identified simply as a "WIP" – work in progress – on top of the branch and commit that you created the stash from. 

```shell
$ git stash list
stash@{0}: WIP on main: 5002d47 our new homepage
stash@{1}: WIP on main: 5002d47 our new homepage
stash@{2}: WIP on main: 5002d47 our new homepage
```

To provide a bit more context, it's good practice to annotate your stashes with a description, using `git stash save "message"`:

```shell
$ git stash save "add style to our site"
Saved working directory and index state On main: add style to our site
HEAD is now at 5002d47 our new homepage

$ git stash list
stash@{0}: On main: add style to our site
stash@{1}: WIP on main: 5002d47 our new homepage
stash@{2}: WIP on main: 5002d47 our new homepage
```

By default, `git stash pop` will re-apply the most recently created stash: `stash@{0}`

You can choose which stash to re-apply by passing its identifier as the last argument, for example:

```shell
$ git stash pop stash@{2}
```


## Partial stashes

You can also choose to stash just a single file, a collection of files, or individual changes from within files. If you pass the `-p` option (or `--patch`) to `git stash`, it will iterate through each changed "hunk" in your working copy and ask whether you wish to stash it:

```shell
$ git stash -p
diff --git a/style.css b/style.css
new file mode 100644
index 0000000..d92368b
--- /dev/null
+++ b/style.css
@@ -0,0 +1,3 @@
+* {
+  text-decoration: blink;
+}
Stash this hunk [y,n,q,a,d,/,e,?]? y
diff --git a/index.html b/index.html
index 9daeafb..ebdcbd2 100644
--- a/index.html
+++ b/index.html
@@ -1 +1,2 @@
+<link rel="stylesheet" href="style.css"/>
Stash this hunk [y,n,q,a,d,/,e,?]? n
```

![Git Stash -p](image/02.svg)

You can hit **?** for a full list of hunk commands. Commonly useful ones are:

| **Command** | **Description**                                              |
| ----------- | ------------------------------------------------------------ |
| */*         | search for a hunk by regex                                   |
| *?*         | help                                                         |
| *n*         | don't stash this hunk                                        |
| *q*         | quit (any hunks that have already been selected will be stashed) |
| *s*         | split this hunk into smaller hunks                           |
| *y*         | stash this hunk                                              |

There is no explicit "abort" command, but hitting `CTRL-C`(SIGINT) will abort the stash process.

## Creating a branch from your stash

If the changes on your branch diverge from the changes in your stash, you may run into conflicts when popping or applying your stash. Instead, you can use `git stash branch` to create a new branch to apply your stashed changes to:

```shell
$ git stash branch add-stylesheet stash@{1}
Switched to a new branch 'add-stylesheet'
On branch add-stylesheet
Changes to be committed:

    new file:   style.css

Changes not staged for commit:

    modified:   index.html

Dropped refs/stash@{1} (32b3aa1d185dfe6d57b3c3cc3b32cbf3e380cc6a)
```

This checks out a new branch based on the commit that you created your stash from, and then pops your stashed changes onto it.

## How git stash works

If you just wanted to know how to use `git stash`, you can stop reading here. But if you're curious about how Git (and `git stash`) works under the hood, read on!

Stashes are actually encoded in your repository as commit objects. The special ref at `.git/refs/stash` points to your most recently created stash, and previously created stashes are referenced by the `stash` ref's reflog. This is why you refer to stashes by `stash@{n}:` you're actually referring to the nth reflog entry for the `stash` ref. Since a stash is just a commit, you can inspect it with `git log`:

```
$ git log --oneline --graph stash@{0}
*-.   953ddde WIP on main: 5002d47 our new homepage
|\ \ 
| | * 24b35a1 untracked files on main: 5002d47 our new homepage
| * 7023dd4 index on main: 5002d47 our new homepage
|/ 
* 5002d47 our new homepage
```

Depending on what you stashed, a single `git stash` operation creates either two or three new commits. The commits in the diagram above are:

- `stash@{0}`, a new commit to store the tracked files that were in your working copy when you ran `git stash`

- `stash@{0}`'s first parent, the pre-existing commit that was at HEAD when you ran `git stash`

- `stash@{0}`'s second parent, a new commit representing the index when you ran `git stash`

- `stash@{0}` 's third parent, a new commit representing untracked files that were in your working copy when you ran
 `git stash` . This third parent only created if:

  - your working copy actually contained untracked files; and
  - you specified the `--include-untracked` or `--all` option when invoked `git stash`.

How `git stash` encodes your worktree and index as commits:

- Before stashing, your worktree may contain changes to tracked files, untracked files, and ignored files. Some of these changes may also be staged in the index.

  ![Before stashing](image/03.svg)

- Invoking `git stash` encodes any changes to tracked files as two new commits in your DAG: one for unstaged changes, and one for changes staged in the index. The special `refs/stash` ref is updated to point to them.

  ![Git stash](image/04.svg)

- Using the `--include-untracked` option also encodes any changes to untracked files as an additional commit.

  ![Git stash --include-untracked](image/05.svg)

- Using the `--all` option includes changes to any ignored files alongside changes to untracked files in the same commit.

  ![Git Stash --all](image/06.svg)

   

When you run `git stash pop`, the changes from the commits above are used to update your working copy and index, and the stash reflog is shuffled to remove the popped commit. Note that the popped commits aren't immediately deleted, but do become candidates for future garbage collection.
