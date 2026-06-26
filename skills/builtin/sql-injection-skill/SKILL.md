---
name: sql-injection-skill
description: Focused SQL/NoSQL/ORM injection skill for authorized CTF, lab, and pentest targets. Use for SQL/ORM errors, quote/boolean/time differences, login/search/sort/filter/INSERT/UPDATE/second-order anomalies, UNION or blind behavior, controllable ORDER BY or identifiers, JSON/URL nested objects, MongoDB operators, MongoEngine __raw__, GraphQL filters, Django/Prisma/Ransack/OData query DSLs, oracle modeling, minimal extraction, auth bypass validation, and sqlmap verification.
---

# sql-injection-skill

Goal: turn a suspicious input into one usable primitive, then extract only the state, credential, token, flag, or entry needed.

## Minimal Approach

1. Locate where input reaches a query: SQL string, sort field, login lookup, INSERT/UPDATE path, second-order trigger, NoSQL object, GraphQL argument, or ORM DSL.
2. Build one stable primitive: boolean, error, time, sort, returned-row, or object-operator difference.
3. Choose the shortest path from that primitive: UNION echo, blind extraction, auth bypass, second-order trigger, NoSQL/GraphQL extraction, or ORM/DSL bypass.
4. Extract the smallest useful data. After login or privilege changes, inspect newly reachable functionality instead of dumping broadly.

## References

- SQL contexts, UNION, blind injection, login bypass, sort injection, and second-order queries: `references/sql-playbook.md`
- JSON, MongoDB/MongoEngine, GraphQL, and field selection: `references/nosql-graphql.md`
- Django, Prisma, Ransack, OData, and dynamic query DSLs: `references/orm-query-dsl.md`
- sqlmap recheck or complex request acceleration: `references/sqlmap-verification.md`

The main file gives direction, not a fixed playbook. Select the shortest route from the live oracle.
