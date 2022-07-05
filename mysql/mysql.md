mysqldump  -uray -pMyPass4! --no-data --no-tablespaces --databases lp >init.sql

## 查看数据表最后更新时间
```sql
SELECT UPDATE_TIME, TABLE_SCHEMA, TABLE_NAME
FROM information_schema.tables
ORDER BY UPDATE_TIME DESC, TABLE_SCHEMA, TABLE_NAME
```

## 不存在才插入
```sql
INSERT INTO `table` (`value1`, `value2`) 
SELECT 'stuff for value1', 'stuff for value2' FROM DUAL 
WHERE NOT EXISTS (SELECT * FROM `table` 
      WHERE `value1`='stuff for value1' AND `value2`='stuff for value2' LIMIT 1) 


insert into team_apply(team_id,user_id,role) select ?,?,? from dual where not exists(select id from team_apply where team_id=? and user_id=?)
```
只有where后面条件满足，前面插入语句才会生效
the LIMIT 1 (micro-optimization, may be omitted)
DUAL refers to a special one row, one column table present by default in all Oracle databases. On a MySQL-Server version 5.7.26 I got a valid query when omitting FROM DUAL, but older versions (like 5.5.60) seem to require the FROM information. 

## 特殊字符
有单引号的可以用双引号括起来
有双引号的可以用单引号括起来

## 存在则更新
```sql
ON DUPLICATE KEY UPDATE
```
插入影响1行，更新影响2行，0的话就是存在且更新前后值一样
