```c
long do_sys_open(int dfd, const char __user *filename, int flags, umode_t mode)
{
	struct open_flags op;
	int fd = build_open_flags(flags, mode, &op);
	struct filename *tmp;

	if (fd)
		return fd;

	tmp = getname(filename);
	if (IS_ERR(tmp))
		return PTR_ERR(tmp);

	//1.得到一个文件描述符
	fd = get_unused_fd_flags(flags);
	if (fd >= 0) {
		//2.得到一个struct file结构；
		struct file *f = do_filp_open(dfd, tmp, &op);
		if (IS_ERR(f)) {
			put_unused_fd(fd);
			fd = PTR_ERR(f);
		} else {
			fsnotify_open(f);
			//3.把文件描述符和struct file结构关联起来
			fd_install(fd, f);
		}
	}
	putname(tmp);
	return fd;
}
```

```c
struct file {
	struct path		f_path;
	struct inode		*f_inode;	/* cached value */
	const struct file_operations	*f_op;
```
