# XSS: Defensive Filters

Source: https://portswigger.net/support/xss-defensive-filters
Fetched: 2026-06-28T09:17:37.518400+00:00

This page may be out of date

We haven't updated it for a while because we're busy working on new, improved content to help you get the

most out of Burp Suite. In the meantime, please note that the information on this page may no longer be

accurate.

Visit our Support Center

XSS: Defensive Filters

When testing for XSS vulnerabilities, you will often discover that the server modifies your initial attempted exploits in some way, so they do not succeed in executing your injected script. In this scenario, your next task is to determine whether you input is being affected by server-side processing and, if so, work around it.

This server-side processing is often referred to as a defensive filter. There are three broad possibilities to consider; signature-based filters, sanitizing filters, and length limits.

Beating Signature-Based Filters

Signature-based filters typically cause the application to respond to your attack string with an entirely different response than it did for the harmless string. For example, it might respond with an error message, possibly even stating that an XSS attack was detected.

If this occurs, the next step is to determine which characters or expressions within your input are triggering the filter. An effective approach is to remove different parts of your string in turn and see whether the input is still being blocked.

Typically, this process establishes fairly quickly that a specific expression or character is causing the request to be blocked. In our first example, the expression <script> is being blocked. The next step is to test the filter to establish whether any bypasses exist.

The articles below provide examples of how to beat signature-based filters:

Signature-Based XSS Filters: Introducing Script Code

Bypassing Signature-Based XSS Filters: Modifying HTML

Bypassing Signature-Based XSS Filters: Modifying Script Code

Beating Sanitizing Filters

Of all the obstacles that you may encounter when attempting to exploit potential XSS conditions, sanitizing filters are probably the most common. Here, the application performs some kind of sanitization or encoding on your attack string that renders it harmless, preventing it from causing the execution of JavaScript.

The articles below provide examples of how to beat sanitizing filters:

XSS: Beating HTML Sanitizing Filters

XSS: Beating HTML Sanitizing Filters: Event Handlers

Beating Length Limits

When the application truncates your input to a fixed maximum length, you have three possible approaches to creating a working exploit.

The articles below provide an example of these three approaches:

XSS Filters: Beating Length Limits Using DOM-based Techniques

XSS Filters: Beating Length Limits Using Shortened Payloads

XSS Filters: Beating Length Limits Using Spanned Payloads
