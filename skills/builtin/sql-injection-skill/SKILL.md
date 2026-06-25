---
name: sql-injection-skill
description: 面向授权 CTF/靶场/渗透测试的 SQL/NoSQL/ORM 注入专项技能。用于存在明确注入信号的场景：SQL/ORM 错误、引号/括号/布尔/时间差分、登录/搜索/排序/筛选/INSERT/UPDATE/二阶查询异常、UNION/盲注迹象、标识符或 ORDER BY 可控、JSON/URL 嵌套对象被保留、MongoDB 操作符、MongoEngine __raw__、GraphQL 字段或 filter 参数进入数据库查询、Django/Prisma/Ransack/OData 等查询 DSL 可控。Use when Codex needs focused SQL/NoSQL/ORM injection validation, oracle modeling, minimal data extraction, or sqlmap-assisted verification without broad payload spraying.
---

# sql-injection-skill

目标：把可疑输入点推进成可复现结论：排除、候选、已验证注入，或已拿到目标数据。先建稳定 oracle，再提取最小目标；每次只改变一个变量。

## 最短闭环

1. 固定基线：记录方法、URL、参数、Cookie、角色、Content-Type、状态码、长度、关键文本、跳转和耗时。
2. 定位上下文：用少量代表性探针区分数字、字符串、括号、排序/标识符、INSERT/UPDATE、JSON 对象、GraphQL 参数、ORM 查询 DSL、二阶触发或二次查询。
3. 建立 oracle：用成对请求证明 true/false、row/no-row、error/no-error、delay/no-delay 或字段存在/不存在差分。
4. 选择路线：有回显走 UNION；无回显走布尔/错误/时间盲注；认证点优先控制返回行；对象查询转向 NoSQL/GraphQL。
5. 提取目标：只取推进所需的库名、表列、用户名、密码/哈希、token、role、flag 字段或下一阶段入口。
6. 闭环验证：保留最小请求对和响应信号；登录或权限变化后继续检查上传、导出、管理面、文件读取等新功能面。

## 选择引用

- 已确认 SQL 上下文、过滤点、UNION/盲注、登录绕过、排序注入、二阶或二次查询时，读 `references/sql-playbook.md`。
- 输入是 JSON、URL 嵌套参数、MongoDB/MongoEngine、GraphQL schema/filter/search 或字段选择时，读 `references/nosql-graphql.md`。
- 输入进入 Django/Prisma/Ransack/OData/动态字段选择等 ORM 或查询 DSL 时，读 `references/orm-query-dsl.md`。
- 已有稳定可疑参数，需要用 sqlmap 复核、加速枚举或处理复杂请求时，读 `references/sqlmap-verification.md`。

## 记录卡点

失败时写链条位置，不写“SQLi 失败”。例如：入口已确认；字符串闭合未确定；`'` 报错但 true/false 无差分；排序参数可控但 CASE 无稳定 marker；GraphQL 可请求 `flag` 字段但 filter 对象未证明进入 Mongo；下一步比较一对最小请求。
