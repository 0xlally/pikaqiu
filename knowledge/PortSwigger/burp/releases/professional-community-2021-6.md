# Professional / Community 2021.6

Source: https://portswigger.net/burp/releases/professional-community-2021-6
Fetched: 2026-06-28T09:16:35.793790+00:00

This release includes the return of the hex view to the message editor, HTTP/2 requests for extensions, and several bug fixes.

Hex view

You wanted it back so it has returned, and it's better than ever! The hex view in the message editor returns to Burp Suite, allowing you to display and edit messages in hexadecimal notation. This is especially useful when dealing with binary formats.

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

Bug fixes

This release includes the following bug fixes.

Playing back recorded login sequences is now more reliable when one of the elements in the series is hidden by other elements on the page.

Recorded login sequences can now be tested correctly when you play them from the configuration library.

Changes to the configuration of Burp Collaborator server will now be honored across extensions as well as Burp Suite.

Burp Logger's context menu now works correctly.

Multiple requests are now correctly sent when using a null payload with Burp Intruder.

Rules added to a target scope now display correctly if the rule was added after loading a configuration file that contains other target scope rules.

We corrected ALPN settings, which previously led to No application protocols errors with some servers.

We fixed incorrect parsing of redirect URLs within meta tags.

HTTP/2 will now be correctly used when testing macros within the macro editor.

Burp Suite now correctly handles HTTP/2 settings frames with zero initial window size.

Intruder redirection configurations are now honored in the grep extract "fetch response" feature.
