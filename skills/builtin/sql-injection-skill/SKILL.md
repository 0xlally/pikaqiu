---
name: sql-injection-skill
description: 面向授权 CTF/靶场/渗透测试的 SQL/NoSQL/ORM 注入专项技能。用于存在明确注入信号的场景：SQL/ORM 错误、引号/括号/布尔/时间差分、登录/搜索/排序/筛选/INSERT/UPDATE/二阶查询异常、UNION/盲注迹象、标识符或 ORDER BY 可控、JSON/URL 嵌套对象被保留、MongoDB 操作符、MongoEngine __raw__、GraphQL 字段或 filter 参数进入数据库查询、Django/Prisma/Ransack/OData 等查询 DSL 可控。Use when Codex needs focused SQL/NoSQL/ORM injection validation, oracle modeling, minimal data extraction, or sqlmap-assisted verification without broad payload spraying.
---

# sql-injection-skill

目标：把可疑输入点推进成可利用的 SQL/NoSQL/ORM 注入原语，并拿到登录态、目标字段、凭据、token、flag 或下一阶段入口。

## 最小思路

1. 找到输入进入查询的位置：SQL 字符串、排序/字段名、登录查询、INSERT/UPDATE、二阶触发、NoSQL 对象、GraphQL/ORM 查询 DSL。
2. 建立一个稳定原语：布尔差分、错误差分、时间差分、排序差分、返回行控制或对象操作符保留。
3. 按目标选择利用方式：UNION 回显、盲注提取、认证绕过、二阶触发、NoSQL/GraphQL 字段提取或 ORM/DSL 绕过。
4. 只提取推进链条需要的数据；拿到登录态或权限变化后，继续看新功能面。

## 参考

- SQL 上下文、UNION、盲注、登录绕过、排序注入、二阶查询：`references/sql-playbook.md`
- JSON、MongoDB/MongoEngine、GraphQL、字段选择：`references/nosql-graphql.md`
- Django/Prisma/Ransack/OData/动态查询 DSL：`references/orm-query-dsl.md`
- sqlmap 复核或复杂请求加速：`references/sqlmap-verification.md`

主文件只给方向，不限制具体打法；根据现场 oracle 和目标选择最短路线。
