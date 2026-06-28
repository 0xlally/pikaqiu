# Web Storage: the lesser evil for session tokens

Source: https://portswigger.net/research/web-storage-the-lesser-evil-for-session-tokens
Fetched: 2026-06-28T09:17:31.994489+00:00

Web Storage: the lesser evil for session tokens

James Kettle

Director of Research

@albinowax

Published: Tuesday, 31 May 2016 at 14:38 UTC

Updated: Monday, 1 February 2021 at 11:33 UTC

I was recently asked whether it was safe to store session tokens using Web Storage (sessionStorage/localStorage) instead of cookies. Upon googling this I found the top results nearly all assert that web storage is highly insecure relative to cookies, and therefore not suitable for session tokens. For the sake of transparency, I've decided to publicly document the rationale that lead me to the opposite conclusion.

The core argument used against Web Storage says because Web Storage doesn't support cookie-specific features like the Secure flag and the HttpOnly flag, it's easier for attackers to steal it. The path attribute is also cited. I'll take a look at each of these features and try to examine the history of why they were implemented, what purpose they serve and whether they really make cookies the best choice for session tokens.

The secure flag

The secure flag is quite important for cookies, and outright irrelevant for web storage. Web Storage adheres to the Same Origin Policy, which isolates data based on an origin consisting of a protocol and a domain name. Cookies need the secure flag because they don't properly adhere to the Same Origin Policy - cookies set on https://example.com will be transmitted to and accessible via http://example.com by default. Conversely, a value stored in localStorage on https://example.com will be completely inaccessible to http://example.com because the protocols are different.

In other words, cookies are insecure by default, and the secure flag is simply a bodge to make them as resilient to MITM attacks as Web Storage. Web Storage used over HTTPS effectively has the secure flag by default. Further information on related nuances in the Same Origin Policy can be found in The Tangled Web by Michal Zalewski.

The path attribute

The path attribute is widely known to be pretty much useless for security. It's another example of where cookies are out of sync with the Same Origin Policy - paths are not considered part of an origin so there's no security boundary between them. The only way to isolate two applications from each other at the application layer is to place them on separate origins.

The HttpOnly flag

The HttpOnly flag is an almost useless XSS mitigation. It was invented back in 2002 to prevent XSS being used to steal session tokens. At the time, stealing cookies may have been the most popular attack vector - it was four years later that CSRF was described as the sleeping giant.

Today, I think any competent attacker will exploit XSS using a custom CSRF payload or drop a BeEF hook. Session token stealing attacks introduce a time-delay and environment shift that makes them impractical and error prone in comparison - see Why HttpOnly Won't Protect You for more background on why. This means that if an attacker is proficient, HttpOnly won't even slow them down. It's like a WAF that's so ineffective attackers don't even notice it exists.

The only instance I've seen where HttpOnly was a significant security boundary is on bugzilla.mozilla.org. Untrusted HTML attachments are served from a subdomain which has access to the parent domain's session cookies thanks to cookies' not-quite-same-origin-policy. Ultimately as with the secure flag, the HttpOnly flag is only really required to make cookies as secure as web storage.

Differences that matter

One major difference between the two options is that unlike cookies, web browsers don't automatically attach the contents of web storage to HTTP requests - you need to write JavaScript to attach the session token to a HTTP header. This actually conveys a huge security benefit, because it means the session tokens don't act as an ambient authority. This makes entire classes of exploits irrelevant. Browsers' behaviour of automatically attaching cookies to cross-domain requests is what enables attacks like CSRF and cross-origin timing attacks. There's a specification for yet another cookie attribute to fix this very problem in development at the moment but for now to get this property, your best bet is Web Storage.

Meanwhile, the unhealthy state of the cookie protocol leads to crazy situations where the cookie header can contain a blend of trusted and untrusted data. This is something the ill-conceived double-submit CSRF defence fell foul of. The solution for this is yet another cookie attribute: Origin.

Unlike cookies, web storage doesn't support automatic expiry. The security impact of this is minimal as expiry of session tokens should be done server-side, but it is something to watch out for. Another distinction is that sessionStorage will expire when you close the tab rather than when you close the browser, which may be awesome or inconvenient depending on your use case. Also, Safari disables Web Storage in private browsing mode, which isn't very helpful.

This post is intended to argue that Web Storage is often a viable and secure alternative to cookies. Web Storage isn't ideal for session token storage in every situation - retrofitting it to a non single-page application may add a significant request overhead, Safari disables Web Storage in private browsing mode, and it's insecure in Internet Explorer 8. Likewise, if you do use cookies please use both Secure and HttpOnly.

Conclusion

At first glance it looks like cookies have more security features, but they're ultimately patches over a poor core design. For an in depth assessment of cookies, check out HTTP cookies, or how not to design protocols. Web Storage offers an alternative that, if not secure by default, is less insecure by default.

Back to all articles

Related Research

05 February 2026

06 January 2026

The Fragile Lock:

Novel Bypasses For SAML Authentication

10 December 2025

The Fragile Lock:

Novel Bypasses For SAML Authentication

Introducing HTTP Anomaly Rank

11 November 2025

Introducing HTTP Anomaly Rank
