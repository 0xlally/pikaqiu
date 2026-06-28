# Bypassing Referer-based CSRF defenses

Source: https://portswigger.net/web-security/csrf/bypassing-referer-based-defenses
Fetched: 2026-06-28T09:17:45.972245+00:00

Web Security Academy

CSRF

Bypassing Referer-based CSRF defenses

Bypassing Referer-based CSRF defenses

Aside from defenses that employ CSRF tokens, some applications make use of the HTTP Referer header to attempt to defend against CSRF attacks, normally by verifying that the request originated from the application's own domain. This approach is generally less effective and is often subject to bypasses.

Referer header

The HTTP Referer header (which is inadvertently misspelled in the HTTP specification) is an optional request header that contains the URL of the web page that linked to the resource that is being requested. It is generally added automatically by browsers when a user triggers an HTTP request, including by clicking a link or submitting a form. Various methods exist that allow the linking page to withhold or modify the value of the Referer header. This is often done for privacy reasons.

Validation of Referer depends on header being present

Some applications validate the Referer header when it is present in requests but skip the validation if the header is omitted.

In this situation, an attacker can craft their CSRF exploit in a way that causes the victim user's browser to drop the Referer header in the resulting request. There are various ways to achieve this, but the easiest is using a META tag within the HTML page that hosts the CSRF attack:

<meta name="referrer" content="never">

Validation of Referer can be circumvented

Some applications validate the Referer header in a naive way that can be bypassed. For example, if the application validates that the domain in the Referer starts with the expected value, then the attacker can place this as a subdomain of their own domain:

http://vulnerable-website.com.attacker-website.com/csrf-attack

Likewise, if the application simply validates that the Referer contains its own domain name, then the attacker can place the required value elsewhere in the URL:

http://attacker-website.com/csrf-attack?vulnerable-website.com

Note

Although you may be able to identify this behavior using Burp, you will often find that this approach no longer works when you go to test your proof-of-concept in a browser. In an attempt to reduce the risk of sensitive data being leaked in this way, many browsers now strip the query string from the Referer header by default.

You can override this behavior by making sure that the response containing your exploit has the Referrer-Policy: unsafe-url header set (note that Referrer is spelled correctly in this case, just to make sure you're paying attention!). This ensures that the full URL will be sent, including the query string.

Find CSRF vulnerabilities using Burp Suite

Try for free
