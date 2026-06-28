# DOM Invader

Source: https://portswigger.net/burp/documentation/desktop/tools/dom-invader
Fetched: 2026-06-28T09:16:02.942033+00:00

Support Center

Documentation

Desktop editions

Tools

DOM Invader

ProfessionalCommunity Edition

DOM Invader

Last updated:

June 18, 2026

Read time:

1 Minute

DOM Invader is a browser-based tool that helps you test for DOM XSS vulnerabilities using a variety of sources and sinks, including both web message and prototype pollution vectors. It is available exclusively via Burp's built-in browser, where it comes preinstalled as an extension.

Key features

When enabled, DOM Invader adds a new tab to the browser's DevTools panel. This enables you to perform the following key tasks:

Test for DOM XSS like reflected XSS. The augmented DOM view enables you to instantly identify controllable sinks on the page, showing you both the XSS context and how your input is being sanitized. For more information, see Testing for DOM XSS.

Log, modify, and resend web messages that are sent on a page via the postMessage() method. This enables you to test for DOM XSS via web messages. You can also let DOM Invader probe for vulnerabilities on your behalf by sending its own specially crafted web messages. For more information, see Testing for DOM XSS using web messages.

Automatically identify sources of client-side prototype pollution and scan for controllable gadgets that are passed to dangerous sinks. For more information, see Testing for client-side prototype pollution.

Automatically identify DOM clobbering vulnerabilities.

For more information on how to enable DOM Invader, see Enabling DOM Invader.

DOM Invader is highly configurable, so you can fine-tune its behavior to suit different websites and use cases. For more information, see DOM Invader settings.
