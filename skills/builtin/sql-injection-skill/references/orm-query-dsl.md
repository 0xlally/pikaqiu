# ORM / Query DSL Injection

ORM issues do not always look like raw SQL concatenation. The risk is user control over field names, operators, relationships, `select/include`, or a full `where/filter` object that expands a restricted query into a sensitive-data oracle.

## Entry Signals

- Django/MongoEngine style: `filter(**request.data)`, `Q(**data)`, `field__lookup`.
- Prisma/Sequelize style: request body flows directly into `where`, `select`, `include`, or `orderBy`.
- Ransack/Rails: `q[user_reset_token_start]=x`, `field_predicate`.
- OData/Graph API: `$filter`, `$select`, `$expand`, navigation properties.
- Dynamic field selection: `fields=...`, `columns=...`, `sort=...`, `include=...`.

Evidence standard: in the same dataset, changing a field, relationship, or operator stably changes result count, returned fields, sort order, error text, or timing.

## Fields And Operators

First prove a normal field is controllable, then move to sensitive fields or relationship fields:

```json
{"username":"admin"}
{"password__startswith":"a"}
{"created_by__user__password__contains":"pbkdf"}
```

Common lookup/oracle names:

- Prefix: `startswith`, `startsWith`, `start`.
- Contains: `contains`, `icontains`, `cont`.
- Regex: `regex`, `iregex`, `matches`.
- Comparison: `gt/gte/lt/lte`, OData `ge/lt`.
- Existence/null: `not: null`, `isSet`, `$exists`.

## Relationship Traversal

ORM relationships are high-value leakage surfaces. From a visible object, traverse `createdBy/user/groups/permissions/departments/employees` and build an oracle on sensitive fields.

```json
{"createdBy":{"resetToken":{"startsWith":"0"}}}
{"created_by__user__groups__user__password__startswith":"a"}
```

If the application forces `is_secret=false` or `published=true`, try traversing many-to-many relationships back to protected objects so the public filter applies to one object while leaked fields come from the related object.

## select / include / expand

When the API allows choosing returned fields, start with low-sensitivity fields, then request sensitive fields or relationships:

```json
{"select":{"createdBy":{"select":{"password":true}}}}
{"include":{"createdBy":true}}
```

OData/Graph style:

```text
$select=id,title&$expand=createdBy($select=username,token)
$filter=createdBy/token ge 'm'&$top=1
```

Returning a field is not automatically injection. Prove the user should not access that field or can use it to control the result set.

## Type Confusion And Parsers

Equality validation without a schema may accept object operators:

```json
{"resetToken":{"not":"x"}}
{"resetToken":{"startsWith":"0"}}
```

URL-encoded data, query strings, cookie JSON, and body JSON may use different parsers. Rebuild the oracle when moving the same payload between carriers.

## Extraction Strategy

1. Calibrate case sensitivity, sort order, and response markers with known fields.
2. Use `startsWith/contains/ge/lt` to build prefix or binary-search oracles.
3. For tokens or hashes, use a candidate character set; for case-sensitive values, confirm collation first.
4. Extract only fields that advance the chain: reset token, password hash, role, flag, API key, or TOTP secret.
5. Once you obtain a usable token, role, or credential, return to the normal business flow to verify access.

## Finding Record

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
