# Professional 2.1.05

Source: https://portswigger.net/burp/releases/professional-2-1-05
Fetched: 2026-06-28T09:16:30.570267+00:00

This release adds experimental support for using Burp's embedded Chromium browser to perform all navigation while scanning.

This new approach will provide a robust basis for future capabilities in Burp Scanner, enabling it to eventually deal with any client-side technologies and navigational structures that a modern browser is able to deal with. It has the potential to dramatically improve coverage of the scan, during both the crawling and auditing phases.

In this initial release, Burp Scanner now correctly deals with:

Applications that dynamically construct the navigational UI (links and forms) using JavaScript.

Applications that dynamically mutate the request when a link is clicked or a form is submitted, using JavaScript event handlers.

There are numerous caveats at this stage:

Performance is poor and will be improved considerably over the next few releases.

Navigational elements other than links and forms are not yet supported (such as DIV elements with an onclick handler that makes a request).

Asynchronous requests such as XHR are honored during navigation but are not audited.

Navigational actions that mutate the existing DOM without causing a request to the server are not properly handled.

Frames and iframes are not properly supported.

File uploads are not supported.

The new feature is currently experimental, and is being released to gather feedback from users who want to play with the new capability and assess its effectiveness. The new feature is not currently a suitable replacement for the existing default scanning mode: you are likely to gain some coverage of JavaScript-heavy applications, but also lose some coverage and experience poor performance. Rest assured that over the coming months the new feature will be considerably enhanced until it becomes a robust and superior replacement to the existing scanning mode.

To enable experimental support for browser-based scan navigation, create a new scan, add a crawl configuration, and under "Miscellaneous" select "Use embedded browser for navigation". You can also configure whether to allow the browser to fetch page resources that are out-of-scope.

The release also includes various other bugfixes. The embedded JRE that is included in Burp's installer has been updated to Java 12.
