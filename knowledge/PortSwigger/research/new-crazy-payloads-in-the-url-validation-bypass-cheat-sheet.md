# New crazy payloads in the URL Validation Bypass Cheat Sheet

Source: https://portswigger.net/research/new-crazy-payloads-in-the-url-validation-bypass-cheat-sheet
Fetched: 2026-06-28T09:17:27.420694+00:00

New crazy payloads in the URL Validation Bypass Cheat Sheet

Zakhar Fedotkin

Researcher

@zakfedotkin

Published: Tuesday, 29 October 2024 at 13:59 UTC

Updated: Friday, 22 November 2024 at 09:06 UTC

The strength of our URL Validation Bypass Cheat Sheet lies in the

contributions from the web security community, and today’s update is no

exception. We are excited to introduce a new and improved IP address

calculator, inspired by @e1abrador's

Encode IP Burp Suite Extension

and many more.

New IP validation bypass techniques

In addition to the existing ways of representing an IPv4 address, we’ve

added the following new formats, supported by Chrome, Firefox, Safari. For example, the cloud metadata IP address 169.254.169.254 can be represented in the following ways:

169.254.43518

Partial Decimal (Class B) format combines the third and

fourth parts of the IP address into a decimal number

169.16689662

Partial Decimal (Class A) format combines the second,

third, and fourth parts of the IP address

0xA9.254.0251.0376

Mixed Encodings: each segment of the IP address can

be presented in different formats: hexadecimal, decimal, or octal. To

keep our tool efficient, we don’t generate all possible combinations.

Instead, we convert the first segment to hexadecimal, the second to

decimal, and the last two segments to octal

The cheat sheet now also supports IPv6 addresses. When a valid IPv6 address

is entered into the attacker’s hostname, the wordlist will be updated with

the expanded form of the address. If the IPv6 address contains an embedded

IPv4 address, the cheat sheet will extract it and generate all the

previously mentioned formats. This behaviour can be disabled in the advanced

settings.

Additionally, you can encode the resulting IP formats using special

encodings like Circled Latin letters and numbers, Fullwidth Forms, or even

Seven-segment display characters. To apply these, open the Advanced

settings, go to Normalization settings, and select one or more encoding

options.

Userinfo parsing discrepancies

We’ve added an intriguing new payload to our cheat sheet that targets

discrepancies in userinfo parsing, submitted by @SeanPesce:

https://example.com[@attacker.com

The “left square bracket” character [ in the userinfo segment can cause Spring’s

UriComponentsBuilder to return a hostname value that differs from how major

browsers interpret it. This discrepancy can potentially lead to

vulnerabilities such as open redirects or SSRF. While testing this payload

with our cheat sheet, I was also able to reproduce a separate

exploit

that was patched in the same

update. This is a perfect example of how our URL Validation Bypass Cheat Sheet

can be used to identify real-world vulnerabilities.

CORS validation bypass cheat sheet update

We’ve recently updated our CORS Bypass Cheat Sheet with new techniques,

including an edge case related to localhost regex implementations and

Safari-specific domain splitting attacks, submitted by @t0xodile. These updates address scenarios

where attackers can manipulate domains using special characters to bypass

validation checks. Examples include:

https://example.com.{.web-attacker.com/

https://example.com.}.web-attacker.com/

https://example.com.`.web-attacker.com/

Make sure to follow us on X (formerly Twitter)

@PortSwiggerRes to stay informed

about our latest updates and new attack techniques.

A big thanks to the web security community for continuing to keep the URL

Validation Bypass Cheat Sheet up to date with the latest techniques. If

you’d like to contribute, feel free to raise an

issue

or submit a

PR.

URL cheat sheet

SSRF

cheatsheet

Back to all articles

Related Research

Introducing the URL validation bypass cheat sheet

03 September 2024

Introducing the URL validation bypass cheat sheet

Listen to the whispers: web timing attacks that actually work

07 August 2024

Listen to the whispers: web timing attacks that actually work

SVG animate XSS vector

28 January 2020

SVG animate XSS vector

One XSS cheatsheet to rule them all

26 September 2019

One XSS cheatsheet to rule them all
