---
name: ffuf-skill
description: 使用 ffuf 和沙箱内置 SecLists 字典进行 Web fuzz。适用于目录和文件发现、递归扫描、扩展名和备份文件枚举、vhost/Host header fuzz、GET/POST 参数名和值 fuzz、JSON/body 字段 fuzz、Header/Cookie fuzz、HTTP 方法 fuzz、原始 HTTP 请求 fuzz、多字典组合、ffuf 过滤器和 matcher 调优、输出保存、命中复验和 Burp/ZAP replay。
---

# ffuf 使用说明

把 Web fuzz 任务收敛成一个能直接在 Kali 沙箱里运行的 `ffuf` 命令。默认使用沙箱已安装的 SecLists 字典

## 基本原则

1. 先确认 fuzz 点：路径、文件名、GET 参数名、GET 参数值、POST 表单字段、JSON 字段、Header 名或 Header 值。
2. 优先给一个主命令；只有存在明确取舍时再给一个备选命令。
3. 先做小范围可解释验证，再扩大字典、线程数或递归范围。
4. 对复杂认证请求优先使用 `-request request.txt`，不要手工重拼 Cookie、Token 和特殊 Header。
5. 所有命中都要回到原始 HTTP 响应复验，重点看状态码、长度、词数、行数、关键字符串和跳转位置。

## SecLists 常用路径

这些路径在沙箱中可直接使用：

| 场景 | 字典路径 | 说明 |
| --- | --- | --- |
| 快速目录/文件发现 | `/usr/share/seclists/Discovery/Web-Content/common.txt` | 小而快，适合第一轮探测 |
| 轻量目录扫描 | `/usr/share/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-2.3-small.txt` | 覆盖面比 common 更大 |
| 中等覆盖目录扫描 | `/usr/share/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-2.3-medium.txt` | 更慢，适合已有线索后的扩展 |
| 参数名 fuzz | `/usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt` | GET/POST/JSON 字段名常用首选 |
| API 路径发现 | `/usr/share/seclists/Discovery/Web-Content/api/api-endpoints.txt` | 如果不存在，回退到 common 或 DirBuster |
| DNS 子域名 | `/usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt` | 只在目标允许子域枚举时使用 |
| 常见用户名 | `/usr/share/seclists/Usernames/top-usernames-shortlist.txt` | 无 |
| 常见密码 | `/usr/share/seclists/Passwords/Common-Credentials/10k-most-common.txt` | 无 |
| 默认凭据 | `/usr/share/seclists/Passwords/Default-Credentials/default-passwords.txt` | 设备/后台默认口令排查 |

如果不确定某个文件是否存在，先运行：

```bash
ls -l /usr/share/seclists/Discovery/Web-Content/
find /usr/share/seclists -iname '*parameter*' -o -iname '*api*'
```

## 命令模板

### 路径发现

```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/common.txt \
  -u 'http://TARGET/FUZZ' \
  -mc all -fc 404
```

如果目标所有响应都是 200，先用一个明显不存在的路径测基线长度，再过滤：

```bash
curl -s -o /tmp/notfound.html -w 'code=%{http_code} size=%{size_download}\n' 'http://TARGET/__no_such_path__'
ffuf -w /usr/share/seclists/Discovery/Web-Content/common.txt \
  -u 'http://TARGET/FUZZ' \
  -mc all -fs 1234
```

### 带扩展名的文件发现

PHP 站点示例：

```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-2.3-small.txt \
  -u 'http://TARGET/FUZZ' \
  -e .php,.txt,.bak,.zip \
  -mc all -fc 404
```

### GET 参数名 fuzz

```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt \
  -u 'http://TARGET/page.php?FUZZ=test' \
  -mc all -fs 1234
```

### GET 参数值 fuzz

参数名已知、值未知时，优先自建小字典：

```bash
printf '1\n2\nadmin\ntest\ntrue\nfalse\n../etc/passwd\n' > values.txt
ffuf -w values.txt \
  -u 'http://TARGET/item?id=FUZZ' \
  -mc all -fw 87
```

### POST 表单字段名 fuzz

```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt \
  -u 'http://TARGET/login' \
  -X POST \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'FUZZ=test' \
  -mc all -fs 3010
```

### JSON 字段名 fuzz

```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt \
  -u 'http://TARGET/api/user' \
  -X POST \
  -H 'Content-Type: application/json' \
  -d '{"FUZZ":"test"}' \
  -mc all -fw 91
```

### Header fuzz

Header 值 fuzz：

```bash
printf '127.0.0.1\nlocalhost\n::1\n10.0.0.1\n' > header-values.txt
ffuf -w header-values.txt \
  -u 'http://TARGET/admin' \
  -H 'X-Forwarded-For: FUZZ' \
  -mc all -fl 52
```

Header 名 fuzz：

```bash
printf 'X-Forwarded-For\nX-Real-IP\nX-Originating-IP\nX-Forwarded-Host\n' > header-names.txt
ffuf -w header-names.txt \
  -u 'http://TARGET/admin' \
  -H 'FUZZ: 127.0.0.1' \
  -mc all -fl 52
```

### 原始请求 fuzz

当已有 Burp/浏览器保存的请求时，在需要 fuzz 的位置放 `FUZZ`：

```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt \
  -request request.txt \
  -request-proto http \
  -mc all -fs 4242
```

## 过滤和匹配

常用控制：

- `-mc`：保留指定状态码；不确定时用 `-mc all`
- `-fc`：过滤状态码，如 `-fc 404`
- `-fs`：过滤响应大小，适合模板稳定的页面
- `-fw`：过滤词数，适合存在输入反射导致长度轻微变化的页面
- `-fl`：过滤行数，适合布局稳定的页面
- `-mr`：只保留匹配正则的响应
- `-fr`：过滤匹配正则的响应

经验规则：

- 404 明确：用 `-fc 404`
- 全部 200：用 `-mc all` 加 `-fs` 或 `-fw`
- 输入被反射：优先尝试 `-fw`
- 只关心特定字符串：用 `-mr 'regex'`
- 命中太多：先缩小字典，不要一开始叠很多过滤器

## 输出和复验

保存 JSON 结果：

```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/common.txt \
  -u 'http://TARGET/FUZZ' \
  -mc all -fc 404 \
  -o ffuf-results.json -of json
```

把命中请求转发到 Burp/ZAP：

```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/common.txt \
  -u 'http://TARGET/FUZZ' \
  -mc all -fc 404 \
  -replay-proxy http://127.0.0.1:8080
```

## 常见误区

- 不要在不知道基线时盲目跑大字典。
- 不要把复杂认证请求拆成很多 `-H` 手写，优先 `-request`。
- JSON fuzz 必须保留 `Content-Type: application/json`。
- 不要假设有不同状态码才是命中，CTF 靶机常常全是 200。
- 超时时降低线程、缩小字典或先验证单个候选，不要重复跑同一个大扫描。
