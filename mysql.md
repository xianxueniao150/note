mysqldump  -uray -pMyrayPass4! --no-data --no-tablespaces --databases lp >init.sql

## 查看数据表最后更新时间
```sql
SELECT UPDATE_TIME, TABLE_SCHEMA, TABLE_NAME
FROM information_schema.tables
ORDER BY UPDATE_TIME DESC, TABLE_SCHEMA, TABLE_NAME
```
