# Lab: SSRF with blacklist-based input filter

Source: https://portswigger.net/web-security/ssrf/lab-ssrf-with-blacklist-filter
Fetched: 2026-06-28T09:18:04.596883+00:00

Web Security Academy

SSRF

Lab

Lab: SSRF with blacklist-based input filter

This lab has a stock check feature which fetches data from an internal system.

To solve the lab, change the stock check URL to access the admin interface at http://localhost/admin and delete the user carlos.

The developer has deployed two weak anti-SSRF defenses that you will need to bypass.

Solution

Visit a product, click "Check stock", intercept the request in Burp Suite, and send it to Burp Repeater.

Change the URL in the stockApi parameter to http://127.0.0.1/ and observe that the request is blocked.

Bypass the block by changing the URL to: http://127.1/

Change the URL to http://127.1/admin and observe that the URL is blocked again.

Obfuscate the "a" by double-URL encoding it to %2561 to access the admin interface and delete the target user.

Community solutions

Intigriti

Rana Khalil

Michael Sommer (no audio)

Find SSRF vulnerabilities using Burp Suite

Try for free
