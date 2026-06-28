# XSS: Beating HTML Sanitizing Filters

Source: https://portswigger.net/support/xss-beating-html-sanitizing-filters
Fetched: 2026-06-28T09:17:37.468461+00:00

This page may be out of date

We haven't updated it for a while because we're busy working on new, improved content to help you get the

most out of Burp Suite. In the meantime, please note that the information on this page may no longer be

accurate.

Visit our Support Center

XSS: Beating HTML Sanitizing Filters

The most prevalent manifestation of data sanitization occurs when the application HTML-encodes certain key characters that are necessary to deliver an attack (so < becomes &lt; and > becomes &gt;). In other cases, the application may remove certain characters or expressions in an attempt to cleanse your input of malicious content.

The example uses a version of the "Magical Code Injection Rainbow" taken from OWASP's Broken Web Application Project. Find out how to download, install and use this project.

When you encounter this defense, your first step is to determine precisely which characters and expressions are being sanitized, and whether it is still possible to carry out an attack without directly employing these characters or expressions.

For example, if your data is being inserted directly into an existing script, you may not need to employ any HTML tag characters.

Or, if the application is removing script tags from your input, you may be able to use a different tag with a suitable event handler.

Additionally, you should consider any techniques that deal with signature-based filters. By modifying your input in various ways, you may be able to devise an attack that does not contain any of the characters or expressions that the filter is sanitizing and therefore successfully bypass it.

If it appears impossible to perform an attack without using characters that are being sanitized, you need to test the effectiveness of the sanitizing filter to establish whether any bypasses exist.

Some string manipulation APIs contain methods to replace only the first instance of a matched expression, and these are sometimes easily confused with methods that replace all instances.

So, if <script> is being stripped from your input, you should try the following to check whether all instances are being removed:

<script><script>alert(1)</script>

In this situation you should also check whether the sanitization is being performed recursively:

<scr<script>ipt>alert(1)</script>

In this example the input is not being stripped recursively and the payload successfully executes a script.

Furthermore if the filter performs several sanitizing steps on your input, you should check whether the order or interplay between these can be exploited. For example, if the filter strips <script> recursively and then strips <object> recursively, the following attack may succeed:

<scr<object>ipt>alert(1)</script>

When you are injecting into a quoted string inside an existing script, it is common to find that the application sanitizes your input by placing the backslash character before any quotation mark characters you submit, preventing you from terminating the string and injecting arbitrary script.

In this situation, you should always verify whether the backslash character itself is being escaped. If not, a simple filter bypass is possible, by submitting your own backslash at the point where the application inserts a backslash. The first backslash escapes the second, so that the following character remains unescaped..
