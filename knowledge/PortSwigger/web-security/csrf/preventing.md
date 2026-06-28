# How to prevent CSRF vulnerabilities

Source: https://portswigger.net/web-security/csrf/preventing
Fetched: 2026-06-28T09:17:46.516701+00:00

Web Security Academy

CSRF

How to prevent CSRF vulnerabilities

How to prevent CSRF vulnerabilities

In this section, we'll provide some high-level guidance on how you can protect your own websites from the kinds of vulnerabilities we've demonstrated in our CSRF labs.

Use CSRF tokens

The most robust way to defend against CSRF attacks is to include a CSRF token within relevant requests. The token must meet the following criteria:

Unpredictable with high entropy, as for session tokens in general.

Tied to the user's session.

Strictly validated in every case before the relevant action is executed.

How should CSRF tokens be generated?

CSRF tokens should contain significant entropy and be strongly unpredictable, with the same properties as session tokens in general.

You should use a cryptographically secure pseudo-random number generator (CSPRNG), seeded with the timestamp when it was created plus a static secret.

If you need further assurance beyond the strength of the CSPRNG, you can generate individual tokens by concatenating its output with some user-specific entropy and take a strong hash of the whole structure. This presents an additional barrier to an attacker who attempts to analyze the tokens based on a sample that are issued to them.

How should CSRF tokens be transmitted?

CSRF tokens should be treated as secrets and handled in a secure manner throughout their lifecycle. An approach that is normally effective is to transmit the token to the client within a hidden field of an HTML form that is submitted using the POST method. The token will then be included as a request parameter when the form is submitted:

<input type="hidden" name="csrf-token" value="CIwNZNlR4XbisJF39I8yWnWX9wX4WFoz" />

For additional safety, the field containing the CSRF token should be placed as early as possible within the HTML document, ideally before any non-hidden input fields and before any locations where user-controllable data is embedded within the HTML. This mitigates against various techniques in which an attacker can use crafted data to manipulate the HTML document and capture parts of its contents.

An alternative approach, of placing the token into the URL query string, is somewhat less safe because the query string:

Is logged in various locations on the client and server side;

Is liable to be transmitted to third parties within the HTTP Referer header; and

can be displayed on-screen within the user's browser.

Some applications transmit CSRF tokens within a custom request header. This presents a further defense against an attacker who manages to predict or capture another user's token, because browsers do not normally allow custom headers to be sent cross-domain. However, the approach limits the application to making CSRF-protected requests using XHR (as opposed to HTML forms) and might be deemed over-complicated for many situations.

CSRF tokens should not be transmitted within cookies.

How should CSRF tokens be validated?

When a CSRF token is generated, it should be stored server-side within the user's session data. When a subsequent request is received that requires validation, the server-side application should verify that the request includes a token which matches the value that was stored in the user's session. This validation must be performed regardless of the HTTP method or content type of the request. If the request does not contain any token at all, it should be rejected in the same way as when an invalid token is present.

Use Strict SameSite cookie restrictions

In addition to implementing robust CSRF token validation, we recommend explicitly setting your own SameSite restrictions with each cookie you issue. By doing so, you can control exactly which contexts the cookie will be used in, regardless of the browser.

Even if all browsers eventually adopt the "Lax-by-default" policy, this isn't suitable for every cookie and can be more easily bypassed than Strict restrictions. In the meantime, the inconsistency between different browsers also means that only a subset of your users will benefit from any SameSite protections at all.

Ideally, you should use the Strict policy by default, then lower this to Lax only if you have a good reason to do so. Never disable SameSite restrictions with SameSite=None unless you're fully aware of the security implications.

Be wary of cross-origin, same-site attacks

Although properly configured SameSite restrictions provide good protection from cross-site attacks, it's vital to understand that they are completely powerless against cross-origin, same-site attacks.

If possible, we recommend isolating insecure content, such as user-uploaded files, on a separate site from any sensitive functionality or data. When testing a site, be sure to thoroughly audit all of the available attack surface belonging to the same site, including any of its sibling domains.

Find CSRF vulnerabilities using Burp Suite

Try for free
