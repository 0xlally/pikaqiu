# Testing for DOM clobbering with DOM Invader

Source: https://portswigger.net/burp/documentation/desktop/tools/dom-invader/dom-clobbering
Fetched: 2026-06-28T09:16:02.363042+00:00

Support Center

Documentation

Desktop editions

Tools

DOM Invader

Testing for DOM clobbering

ProfessionalCommunity Edition

Testing for DOM clobbering with DOM Invader

Last updated:

June 18, 2026

Read time:

1 Minute

DOM Invader can automatically test for DOM clobbering vulnerabilities on your behalf. DOM clobbering is a technique in which you inject HTML into a page to manipulate the DOM in a way that enables you to change the behavior of JavaScript on the page.

Web Security Academy

For more information about DOM clobbering, as well as some interactive, deliberately vulnerable labs, check out the related topic on the Web Security Academy.

DOM clobbering

Enabling DOM clobbering

To avoid interfering with your target site's functionality, DOM clobbering is disabled by default. To enable these checks:

Go to the DOM Invader settings menu.

Under Attack types, toggle the switch so that DOM clobbering is on.

Click Reload to refresh the browser. This is necessary for your changes to take effect.

DOM Invader now scans for DOM clobbering vulnerabilities as you browse.
