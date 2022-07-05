mysql主键自增有个参数innodb_autoinc_lock_mode，他有三种可能只0,1,2，mysql5.1之后加入的，默认值是1，之前的版本可以看做都是0。
可以使用下面的语句看当前是哪种模式
```sql
select @@innodb_autoinc_lock_mode;
```

### 模式1
当做简单插入（可以确定插入行数）的时候，直接将auto_increment加1，而不会去锁表，这也就提高了性能。
当插入的语句类似insert into select ...这种复杂语句的时候，提前不知道插入的行数，这个时候就要要锁表（一个名为AUTO_INC的特殊表锁）了，这样auto_increment才是准确的，等待语句结束的时候才释放锁。
还有一种称为Mixed-mode inserts的插入，比如INSERT INTO t1 (c1,c2) VALUES (1,'a'), (NULL,'b'), (5,'c'), (NULL,'d')，其中一部分明确指定了自增主键值，一部分未指定，还有我们这里讨论的INSERT ... ON DUPLICATE KEY UPDATE ...也属于这种，这个时候会分析语句，然后按尽可能多的情况去分配auto_incrementid，这个要怎么理解呢，我看下面这个例子:
```sql
truncate table t1;
insert into t1 values(NULL, 100, "test1"),(NULL, 101, "test2"),(NULL, 102, "test2"),(NULL, 103, "test2"),(NULL, 104, "test2"),(NULL, 105, "test2");

-- 此时数据表下一个自增id是7

delete from t1 where id in (2,3,4);

-- 此时数据表只剩1，5，6了，自增id还是7

insert into t1 values(2, 106, "test1"),(NULL, 107, "test2"),(3, 108, "test2");

-- 这里的自增id是多少呢？
```
上面的例子执行完之后表的下一个自增id是10，你理解对了吗，因为最后一条执行的是一个Mixed-mode inserts语句，innoDB会分析语句，然后分配三个id，此时下一个id就是10了，但分配的三个id并不一定都使用。

### 模式0
不管什么情况都是加上表锁，等语句执行完成的时候在释放，如果真的添加了记录，将auto_increment加1。

### 模式2
什么情况都不加AUTO_INC锁，存在安全问题，当binlog格式设置为Statement模式的时候，从库同步的时候，执行结果可能跟主库不一致，问题很大。因为可能有一个复杂插入，还在执行呢，另外一个插入就来了，恢复的时候是一条条来执行的，就不能重现这种并发问题，导致记录id可能对不上。
