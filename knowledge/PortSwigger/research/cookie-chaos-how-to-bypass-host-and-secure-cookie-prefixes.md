# Cookie Chaos: How to bypass __Host and __Secure cookie prefixes

Source: https://portswigger.net/research/cookie-chaos-how-to-bypass-host-and-secure-cookie-prefixes
Fetched: 2026-06-28T09:17:23.370185+00:00

Cookie Chaos: How to bypass __Host and __Secure cookie prefixes

Zakhar Fedotkin

Researcher

@zakfedotkin

Published: Wednesday, 3 September 2025 at 14:46 UTC

Updated: Wednesday, 3 September 2025 at 14:46 UTC

Browsers added cookie prefixes to protect your sessions and stop attackers from setting harmful cookies. In this post, you’ll see how to bypass cookie defenses using discrepancies in browser and server logic.

For a visual walk‑through, see the SteelCon livestream recording:

Overwriting Cookies with Unicode Whitespace

Cookie prefixes were introduced in RFC 6265bis to strengthen cookie security through naming rules:

A cookie with the __Host- prefix must be host-only, meaning it cannot be shared across subdomains

A cookie with the __Secure- prefix must be set from a secure origin.

These restrictions are enforced by browsers to prevent attacks like cookie tossing or session fixation. However, inconsistencies in how browsers and servers handle cookie encoding and parsing can introduce subtle but dangerous flaws.

According to the original RFC 6265, the Cookie header is defined as a sequence of octets, not characters. This means the browser sends raw bytes on the wire, and it’s the server’s responsibility to decode those bytes into a string. If the browser and server interpret those bytes differently, parsing discrepancies can occur.

By using UTF-8 encoding, an attacker can disguise a restricted cookie - such as one that starts with __Host- in a way that bypasses browser protections. The browser may treat it as a non-restricted cookie, but the server might decode and normalize it in a way that causes it to be interpreted as a protected one.

Here’s a minimal proof of concept that demonstrates this behavior:

document.cookie=

`${String.fromCodePoint(0x2000)}__Host-name=injected; Domain=.example.com; Path=/;`

This whitespace-prefixed cookie is interpreted by the browser as a non-prefixed, non-restricted value and is therefore sent to all subdomains within the target domain’s scope.

During testing, I discovered that certain server-side frameworks, such as Django and ASP.NET, apply normalization and trimming to cookie names before processing. Specifically, when the server interprets U+2000 as a whitespace character, it removes it, resulting in a cookie name that becomes equivalent to __Host-name.

Django uses Python’s built-in .strip() method to process cookie keys and values. This method removes a wide range of Unicode whitespace characters, including [133, 160, 5760, 8192–8202, 8232, 8233, 8239, 8287, 12288], effectively treating them as a space.

Interestingly, Safari handles this case differently. It does not support multibyte Unicode whitespace characters in cookie names, which prevents values like U+2000 from being used. However, single-byte characters such as U+0085 (NEL) and U+00A0 (non-breaking space) are still permitted.

Overwriting Cookies with legacy parsing

In addition to Unicode tricks, legacy cookie parsing behavior can also be abused to bypass prefix protections. As shown in the previous blog post, if a Cookie header begins with $Version=1, some Java-based web servers, such as Apache Tomcat and Jetty, switch into a legacy parsing. In this mode, a single cookie string may be interpreted as multiple separate cookies. For example, the following JavaScript sets a cookie that includes a forged __Host- pair:

document.cookie=

`$Version=1,__Host-name=injected; Path=/somethingreallylong/; Domain=.example.com;`;

This lets the attacker bypass the browser’s prefix checks and inject high-privilege cookies from a subdomain or over an insecure origin.

Full attack scenario

Suppose you discover an XSS vulnerability where a cookie value is reflected into a web page without proper escaping. The application uses a __Host- prefixed cookie, which normally prevents overwriting from untrusted subdomains due to browser-enforced restrictions. However, using one of the techniques described earlier, you inject a forged __Host-name cookie using JavaScript:

document.cookie=

`${String.fromCodePoint(0x2000)}__Host-name=<img src=x onerror=alert(1)>;

Domain=example.com;

Path=/;`

The browser, unaware that this cookie is equivalent to the protected one, accepts it and includes both the original and attacker-controlled cookies in the request. On the wire, the browser sends the following header:

Cookie: __Host-name=Carlos; â€€__Host-name=<img src=x onerror=alert(1)>;

When this request reaches the backend, the server parses the Cookie header. If multiple cookies with the same name are present, many frameworks, including Django, resolve the conflict by accepting only one value, typically the last occurrence. In this case, the attacker-controlled value takes precedence.

If the application reflects this cookie value into the response without proper encoding, the result is a cross-site scripting vulnerability. Alternatively, if the same cookie is used for CSRF protection or session identification, this behavior can also lead to session fixation or other privilege escalation paths.

Django responded to my vulnerability report:

The official Django documentation has a warning against permitting cookies from untrusted subdomains as this is vulnerable to attacks: https://docs.djangoproject.com/en/5.0/topics/http/sessions/#topics-session-security. As this attack relies on this, this will not be treated as a security vulnerability.

Takeaways

The same cookie can be interpreted in different ways by the browser and the backend. This mismatch can quietly break the guarantees of cookie confidentiality and integrity, even when the strongest browser-side protections. To help test for the issues discussed here I’ve created a lightweight Custom Action for Burp Suite.

It can quickly detect conditions where a backend may be vulnerable to cookie prefix bypasses.

This blog post concludes our exploration into cookie parsing inconsistencies and how they can be exploited to bypass security mechanisms. If you haven’t already, make sure to check out the previous article in this series, where we demonstrated how the cookie sandwich technique can be used to steal HttpOnly cookies.

cookie chaos

Cookies

Zakhar Favourites

XSS

Back to all articles

Related Research

The Fragile Lock:

Novel Bypasses For SAML Authentication

10 December 2025

The Fragile Lock:

Novel Bypasses For SAML Authentication

WebSocket Turbo Intruder: Unearthing the WebSocket Goldmine

17 September 2025

WebSocket Turbo Intruder: Unearthing the WebSocket Goldmine

Drag and Pwnd: Leverage ASCII characters to exploit VS Code

30 April 2025

Drag and Pwnd: Leverage ASCII characters to exploit VS Code

Stealing HttpOnly cookies with the cookie sandwich technique

22 January 2025

Stealing HttpOnly cookies with the cookie sandwich technique
