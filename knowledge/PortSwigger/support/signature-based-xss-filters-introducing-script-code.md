# Signature-Based XSS Filters: Introducing Script Code

Source: https://portswigger.net/support/signature-based-xss-filters-introducing-script-code
Fetched: 2026-06-28T09:17:34.928021+00:00

This page may be out of date

We haven't updated it for a while because we're busy working on new, improved content to help you get the

most out of Burp Suite. In the meantime, please note that the information on this page may no longer be

accurate.

Visit our Support Center

Signature-Based XSS Filters: Introducing Script Code

You can introduce script code in to an HTML page by various means. In this article we provide examples of some popular methods that may succeed in bypassing signature-based input filters.

Note: Browser support for different HTML and scripting syntax varies widely. The behavior of individual browsers often changes with each new version. Any "definitive" guide to individual browsers' behavior is therefore liable to quickly become out of date. However, from a security perspective, applications need to behave in a robust way for all current and recent versions of popular browsers.

The example uses a version of the "Magical Code Injection Rainbow" taken from OWASP’s Broken Web Application Project. Find out how to download, install and use this project.

Script Tags

In this example our initial input has been rejected and we have been presented with an error message.

The next step is to determine which characters or expressions within your input are triggering the filter. An effective approach is to remove different parts of your string in turn and see whether the input is still being blocked.

Typically, this process establishes fairly quickly what specific expression or character is causing the request to be blocked. In this example, the characters <script> are being blocked.

You then need test the filter to establish whether any bypasses exist.

Beyond directly using a <script> tag, there are various ways in which you can use somewhat convoluted syntax to wrap the use of a tag.

In this example we have used an object tag with a data attribute and a Base64-encoded string.

The encoded element of the payload is equivalent to:

<script>alert(1)</script>

We have used alert to confirm that the payload fires and that the filter has been beaten.

In many cases, you may find that signature-based filters can be defeated simply by switching to a different, lesser-known method of executing script, as above. However, if this fails, you need to look at ways of obfuscating your attack.

Event Handlers

Numerous event handlers can be used with various tags to cause a script to execute.

In this example we can see the <svg> tag being used with the onload event handler:

<svg onload="alert(1)">

We can see the payload firing effectively in the most recent version of Firefox. For reference purposes, this article was written in July 2016.

As browsers and applications develop, an attacker will need to modify payloads accordingly. It is important to keep up to date with working attack vectors.

Script Pseudo-Protocols

Script pseudo-protocols can be used in various locations to execute inline script within an attribute that expects a URL. Here are some examples:

<object data=javascript:alert(1)>

<iframe src=javascript:alert(1)>

<embed src=javascript:alert(1)>
