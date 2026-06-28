# Professional / Community 2021.6.2

Source: https://portswigger.net/burp/releases/professional-community-2021-6-2
Fetched: 2026-06-28T09:16:35.997543+00:00

This release includes the return of the hex view, enabling HTTP/2 for extensions, task pausing improvements, an embedded browser upgrade, and several bug fixes.

Hex view

You wanted it back so it has returned, and it's better than ever! The hex view in the message editor returns to Burp Suite, allowing you to display and edit messages in hexadecimal notation. This is especially useful when dealing with binary formats. You can also choose to copy text or hex codes when using the context menu to copy single or multiple cells in the message editor's hex view.

HTTP/2 enabled for extensions

HTTP/2 is now enabled for requests issued by extensions. Additionally, we have added two new methods to IBurpExtenderCallbacks, which can be used to force HTTP/1 usage when issuing requests. These methods are:

IHttpRequestResponse makeHttpRequest(IHttpService httpService,

byte[] request,

boolean forceHttp1);

and

byte[] makeHttpRequest(String host,

int port,

boolean useHttps,

byte[] request,

boolean forceHttp1);

These new methods are analogous to the existing makeHttpRequest() methods with the addition of the forceHttp1 flag, which when set will ensure that HTTP/1 is used.

Task pausing improvements

Burp Suite now remembers your preference for pausing tasks on starting.

Chromium version update and security fix

We have updated Burp Suite's embedded browser to Chromium version 91.0.4472.114, which fixes several security issues that Google has classified as high.

Bug fixes

This release fixes several minor bugs.
