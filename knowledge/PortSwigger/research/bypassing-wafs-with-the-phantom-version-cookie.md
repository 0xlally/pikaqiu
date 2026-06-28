# Bypassing WAFs with the phantom $Version cookie

Source: https://portswigger.net/research/bypassing-wafs-with-the-phantom-version-cookie
Fetched: 2026-06-28T09:17:22.051621+00:00

Bypassing WAFs with the phantom $Version cookie

Zakhar Fedotkin

Researcher

@zakfedotkin

Published: Wednesday, 4 December 2024 at 15:03 UTC

Updated: Monday, 30 June 2025 at 16:01 UTC

HTTP cookies often control critical website features, but their long and convoluted history exposes them to parser discrepancy vulnerabilities. In this post, I'll explore some dangerous, lesser-known features of modern cookie parsers and show how they can be abused to bypass web application firewalls. This is the first part of a series of blog posts on cookie parsing.

Downgrading cookie parsers with $Version

There have been many attempts to standardize HTTP cookies, starting with the first official standard: RFC2109. Even though modern browsers do not support legacy RFCs, many web servers still do. Here's an example valid Cookie header:

Cookie: $Version=1; foo="bar"; $Path="/"; $Domain=abc;

$Version is a required attribute, identifying the version of the state management specification to which the cookie conforms. Other interesting attributes include $Domain and $Path, which we’ll discuss later. According to the standard, a Cookie value can include special characters like spaces, semicolons, and equal signs if they are enclosed in double quotes:

Many HTTP/1.1 header field values consist of words separated by LWS (Linear

White Space) or special characters. These special characters MUST be in a

quoted string to be used within a parameter value. - RFC 2068.

Modern frameworks analyze that header in the following ways:

Flask: {"foo":"bar","$Version":"1","$Path":"/","$Domain":"abc"}

Django: {"foo":"bar","$Version":"1","$Path":"/","$Domain":"abc"}

PHP: {"foo":"\"bar\"","$Version":"1","$Path":"\"\/\"","$Domain":"abc"}

Ruby: {"foo":"\"bar\"","$Version":"1","$Path":"\"\/\"","$Domain":"abc"}

Spring: { "foo": "\"bar\""}

SimpleCookie: { "foo": "bar"}

As we can see, the results are messy. This mess gives us a chance to look for security weaknesses. Let’s focus on Spring Boot Starter Web 2.x.x first. It uses Apache Tomcat v. 9.0.83 by default, which processes cookie headers in the following ways:

It handles both RFC6265 and RFC2109 standards, defaulting to legacy parsing logic if a string starts with the special $Version attribute.

It also supports the $Path and $Domain attributes, which may enable users to change reflected cookie attributes if they aren’t checked properly before responding.

The parser will also unescape any character starting with backslash (\), as shown in the following example.

Cookie: $Version=1; foo="\b\a\r"; $Path=/abc; $Domain=example.com =>

Set-Cookie: foo="bar"; Path=/abc; Domain=example.com

Another good example is the Python SimpleCookie parser, which supports legacy cookie request attributes when followed by key-value pairs. This enables the injection of malicious cookie attributes in the same manner demonstrated previously. All Python-based frameworks (Flask, Django, etc.) allow quoted cookie values but don't recognize the magic strings, like $Version, treating it as a normal cookie name instead. They also automatically decode octal escape sequences within quoted strings as follows:

Any non-text character is translated into a 4 character sequence: a

forward-slash followed by the three-digit octal equivalent of the character. -

Cookies.py

For example:

"\012" <=> \n

"\015" <=> \r

"\073" <=> ;

Bypass Web Application Firewalls (WAFs)

Many WAFs are not equipped to detect the techniques described above, allowing malicious payloads to be hidden within quoted strings.

Bypassing value analysis with quoted-string encoding

In addition, quoted cookies can facilitate injection vulnerabilities, such as SQL injection or command injection. These types of attacks often use special command separators - such as semicolons (;), commas (,), newline characters (\n), and backslashes (\). While typically restricted in cookie values, these can sometimes be manipulated to trigger vulnerabilities. Implementing this type of quoted cookie encoding can be easily achieved using a Burp Suite extension with the HttpHandler interface:

def handleHttpRequestToBeSent(requestToBeSent):

result = "$Version=1; "

for param in requestToBeSent.parameters:

result += f"{param.name}=\""

for char in param.value:

result += f"\\{char}"

result += "\"; "

return continueWith(requestToBeSent.withAddedHeader("Cookie",result))

For example, the Amazon Web Services WAF blocks any request that contains any parameter inside disallowed function:

eval() => allowed

eval('test') => forbidden

"\e\v\a\l\(\'\t\e\s\t\'\)" => allowed

"\145\166\141\154\050\047\164\145\163\164\047\051" => allowed

Bypassing cookie-name blocklists

Another crucial aspect of RFC2109: a server should also accept a comma (,) as a separator between cookie values. This can be exploited to bypass simple WAF signatures that may not anticipate a cookie name being concealed within the value. Additionally, the specification permits any number of space or tab characters before or after the equal sign in an injected attribute-value pair, which could also be used to avoid the detection. Consider the Cookie header example:

$Version=1; foo=bar, abc = qux => "abc": "qux"

Bypassing value analysis with cookie splitting

Like many other HTTP headers, the Cookie header can be sent multiple times in a single request. The way how a server handles multiple identical headers may then vary. For example, I sent following GET request:

GET / HTTP/1.1

Host: example.com

Cookie: param1=value1;

Cookie: param2=value2;

And got the following back:

Flask: { "param1": "value1", ",param2": "value2"}

Django: { "param1": "value1", ",param2": "value2"}

PHP: { "param1": "value1", ",_param2": "value2"}

Ruby: { "param1": "value1", ", param2": "value2"}

Spring: { "param1": "value1", "param2": "value2"}

As we can see, Ruby, PHP, and the Python frameworks Django and Flask combine headers into a single comma-separated string (with an optional space between parameters). Quoted cookie values are also supported, which allows hiding malicious payloads by using the Cookie header as a multiline header continuation.

Unfortunately, the quoted strings technique does not work with PHP and Ruby. To bypass the mentioned AWS signatures, you can use the following request:

Cookie: name=eval('test') => forbidden

Cookie: name=eval('test//

Cookie: comment')

Resulting cookie: name=eval('test//, comment') => allowed

Automation using Burp Extensions

We've implemented the best of these techniques in Param Miner for you:

Preventing vulnerabilities

You can take a range of steps to prevent parser discrepancy vulnerabilities in cookies, as follows:

Ensure that legacy support for RFC2109 is disabled on the web server unless it is explicitly required.

Validate all user inputs rigorously to identify and mitigate potentially dangerous data. This helps ensure that inputs are safe for processing within your application or when interacting with other system components.

Avoid relying on assumptions about the presence or absence of specific characters in user inputs to reduce the risk of unexpected behavior.

Want to learn more?

This blog post is just the first part of our exploration into cookie parsing logic. To learn how these techniques can be applied in real-world scenarios to escalate vulnerabilities, be sure to check out the Stealing HttpOnly cookies with the cookie sandwich technique.

For our latest blog posts and security insights, follow us on X (formerly Twitter) and Bluesky, and join the official PortSwigger Discord.

If you're interested in learning more about quoted cookies, take a look at

my earlier research on

the Memcached Command Injections at Pylibmc

If you're curious about invalid characters in cookie headers,I recommend April King's Handling Cookies is a Minefield research.

Cookies

WAF

SQL Injection

XSS

Zakhar Favourites

cookie chaos

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

Cookie Chaos: How to bypass __Host and __Secure cookie prefixes

03 September 2025

Cookie Chaos: How to bypass __Host and __Secure cookie prefixes

Drag and Pwnd: Leverage ASCII characters to exploit VS Code

30 April 2025

Drag and Pwnd: Leverage ASCII characters to exploit VS Code
