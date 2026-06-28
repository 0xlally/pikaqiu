# Web cache deception

Source: https://portswigger.net/kb/issues/00200650_web-cache-deception
Fetched: 2026-06-28T09:17:11.278740+00:00

Support Center

Issue Definitions

Web cache deception

Web cache deception

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Web cache deception

Web cache deception exploits discrepancies between cache proxy and backend parsers, leading web servers to mistakenly cache and serve dynamic content as though it were static. This vulnerability is often exploited by attackers adding fake static file extensions to dynamic URLs, for example, changing "/path" to "/path/WCD.css". When users click on these modified links, the caching system erroneously identifies the request as for a static resource and caches the response, making the user's sensitive information public. If subsequent unauthorized users make a request to the same URL then they will be served the cached page, potentially exposing the sensitive information repeatedly. The distributed nature of web caches means that even a single web cache deception attack can have far-reaching effects, extending the potential for sensitive data exposure across various users and sessions.

Remediation: Web cache deception

To mitigate the risk of web cache deception vulnerabilities, web administrators should:

Clearly specify which content should be cached. This involves setting up clear caching rules within your application.

Implement strong cache management by using Cache-Control headers. For dynamic content, use settings like no-cache to prevent it from being stored.

Implement strong URL parameters validation, blocking any unexpected file extensions or paths that could be exploited.

Regularly review your cache configuration and audit the content it contains. This can help you identify and address any potential issues quickly.

Treat all content as non-cacheable unless it has been explicitly approved for caching. This approach helps minimize the risk of inadvertently caching sensitive information.

Typical severity

Medium

Type index (hex)

0x00200650

Type index (decimal)

2098768

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Burp Scanner

This issue - and many more like it - can be found using our

web vulnerability scanner

Read more

Get Burp

Scan your web application from just $499.00

Find out more
