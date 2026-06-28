# Professional 1.6.11

Source: https://portswigger.net/burp/releases/professional-1-6-11
Fetched: 2026-06-28T09:16:26.755232+00:00

This release adds a new Scanner check for path-relative style sheet import (PRSSI) vulnerabilities.

PRSSI vulnerabilities (sometimes termed "relative path overwrite") are not widely understood by security testers or application developers. The key prerequisite for the vulnerability (a CSS import directive that uses a path-relative URL) is both seemingly innocuous and very common. There are some other conditions that are needed for exploitability, but real vulnerabilities are quite prevalent in the wild. The impact of the vulnerability is in many cases serious, and equivalent to cross-site scripting (XSS).

Burp Suite is currently the only scanning product available that can detect PRSSI vulnerabilities. We hope that the addition of this scan check will enable Burp users to identify and fix any problems before PRSSI vulnerabilities become more widely understood and exploited.

For more information, including a real example of a recent PRSSI vulnerability in a public application, please see today's blog post.
