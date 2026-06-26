---
name: ffuf-skill
description: Use ffuf with sandbox-installed SecLists wordlists for web fuzzing, endpoint discovery, route/path/directory/file discovery, recursive scans, extension and backup file enumeration, vhost and Host header fuzzing, login/register form input mapping, GET/POST parameter name and value fuzzing, JSON/body field fuzzing, Header/Cookie fuzzing, HTTP method fuzzing, raw HTTP request fuzzing, multi-wordlist combinations, ffuf matcher/filter tuning, output saving, hit verification, and Burp/ZAP replay before vulnerability testing.
---

# ffuf Usage Guide

Turn a web fuzzing task into one `ffuf` command that can run directly inside the Kali sandbox. Prefer the sandbox-installed SecLists wordlists.

## Principles

1. Identify the fuzz point first: path, file name, GET parameter name, GET parameter value, POST form field, JSON field, header name, or header value.
2. Give one primary command first; add an alternative only when there is a clear tradeoff.
3. Start with a small, explainable check before increasing wordlist size, threads, or recursion depth.
4. For authenticated or complex requests, prefer `-request request.txt` instead of manually rebuilding cookies, tokens, and special headers.
5. Recheck hits with raw HTTP responses. Compare status code, size, word count, line count, keywords, and redirect location.

## SecLists Paths

These paths are available inside the sandbox:

| Task | Wordlist path | Notes |
| --- | --- | --- |
| Fast path/file discovery | `/usr/share/seclists/Discovery/Web-Content/common.txt` | Small first pass |
| Lightweight directory scan | `/usr/share/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-2.3-small.txt` | Wider than `common.txt` |
| Medium directory scan | `/usr/share/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-2.3-medium.txt` | Use after finding useful leads |
| Parameter names | `/usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt` | Good for GET/POST/JSON field names |
| API endpoints | `/usr/share/seclists/Discovery/Web-Content/api/api-endpoints.txt` | Fall back to `common.txt` or DirBuster if missing |
| DNS subdomains | `/usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt` | Only when subdomain enumeration is in scope |
| Common usernames | `/usr/share/seclists/Usernames/top-usernames-shortlist.txt` | Username checks |
| Common passwords | `/usr/share/seclists/Passwords/Common-Credentials/10k-most-common.txt` | Password checks |
| Default credentials | `/usr/share/seclists/Passwords/Default-Credentials/default-passwords.txt` | Device/admin default credentials |

If a path may not exist, check first:

```bash
ls -l /usr/share/seclists/Discovery/Web-Content/
find /usr/share/seclists -iname '*parameter*' -o -iname '*api*'
```

## Command Templates

### Path Discovery

```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/common.txt \
  -u 'http://TARGET/FUZZ' \
  -mc all -fc 404
```

If every response is `200`, measure an impossible path and filter by size:

```bash
curl -s -o /tmp/notfound.html -w 'code=%{http_code} size=%{size_download}\n' 'http://TARGET/__no_such_path__'
ffuf -w /usr/share/seclists/Discovery/Web-Content/common.txt \
  -u 'http://TARGET/FUZZ' \
  -mc all -fs 1234
```

### File Discovery With Extensions

```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-2.3-small.txt \
  -u 'http://TARGET/FUZZ' \
  -e .php,.txt,.bak,.zip \
  -mc all -fc 404
```

### GET Parameter Name Fuzzing

```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt \
  -u 'http://TARGET/page.php?FUZZ=test' \
  -mc all -fs 1234
```

### GET Parameter Value Fuzzing

When the parameter name is known but values are unknown, start with a small custom list:

```bash
printf '1\n2\nadmin\ntest\ntrue\nfalse\n../etc/passwd\n' > values.txt
ffuf -w values.txt \
  -u 'http://TARGET/item?id=FUZZ' \
  -mc all -fw 87
```

### POST Form Field Name Fuzzing

```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt \
  -u 'http://TARGET/login' \
  -X POST \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'FUZZ=test' \
  -mc all -fs 3010
```

### JSON Field Name Fuzzing

```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt \
  -u 'http://TARGET/api/user' \
  -X POST \
  -H 'Content-Type: application/json' \
  -d '{"FUZZ":"test"}' \
  -mc all -fw 91
```

### Header Fuzzing

Header value:

```bash
printf '127.0.0.1\nlocalhost\n::1\n10.0.0.1\n' > header-values.txt
ffuf -w header-values.txt \
  -u 'http://TARGET/admin' \
  -H 'X-Forwarded-For: FUZZ' \
  -mc all -fl 52
```

Header name:

```bash
printf 'X-Forwarded-For\nX-Real-IP\nX-Originating-IP\nX-Forwarded-Host\n' > header-names.txt
ffuf -w header-names.txt \
  -u 'http://TARGET/admin' \
  -H 'FUZZ: 127.0.0.1' \
  -mc all -fl 52
```

### Raw Request Fuzzing

For a request saved from Burp or the browser, put `FUZZ` at the mutation point:

```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt \
  -request request.txt \
  -request-proto http \
  -mc all -fs 4242
```

## Filters And Matchers

- `-mc`: keep matching status codes; use `-mc all` when unsure.
- `-fc`: filter status codes, such as `-fc 404`.
- `-fs`: filter response size; useful for stable templates.
- `-fw`: filter word count; useful when reflection slightly changes size.
- `-fl`: filter line count; useful for stable layouts.
- `-mr`: keep responses matching a regex.
- `-fr`: filter responses matching a regex.

Rules of thumb:

- Clear `404`: use `-fc 404`.
- All `200`: use `-mc all` plus `-fs` or `-fw`.
- Reflected input: try `-fw` first.
- Need a specific keyword: use `-mr 'regex'`.
- Too many hits: shrink the wordlist before stacking filters.

## Output And Replay

Save JSON output:

```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/common.txt \
  -u 'http://TARGET/FUZZ' \
  -mc all -fc 404 \
  -o ffuf-results.json -of json
```

Replay hits through Burp/ZAP:

```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/common.txt \
  -u 'http://TARGET/FUZZ' \
  -mc all -fc 404 \
  -replay-proxy http://127.0.0.1:8080
```

## Common Mistakes

- Do not run a large wordlist before knowing the baseline response.
- Do not rebuild complex authenticated requests by hand; use `-request`.
- Keep `Content-Type: application/json` when fuzzing JSON bodies.
- Do not assume a hit needs a different status code; CTF targets often return `200` for everything.
- On timeouts, reduce threads, shrink the wordlist, or validate a single candidate before repeating a large scan.
