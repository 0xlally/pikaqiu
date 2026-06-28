# Professional 1.4.06

Source: https://portswigger.net/burp/releases/professional-1-4-06
Fetched: 2026-06-28T09:16:23.879513+00:00

This release contains a number of bugfixes and other minor enhancements:

A bug has been fixed which meant the Spider sometimes did not honour the configured maximum requests per URL.

A bug has been fixed where the Spider did not handle BASE tags properly.

The Burp Extender API IHttpRequestResponse.setHighlight(String color) now accepts a null value in the parameter, which has the effect of clearing any existing highlight.

A bug has been fixed in the HTTP message viewer/editor which caused display errors in some long lines.

A bug has been fixed which caused some waiting items in the active scan queue not to restart following restoration of state.

The session handling cookie jar now tracks cookie expiration times. The session handling rule to update the request with cookies from Burp's cookie jar now removes cookies from requests when they have expired. Previously, the failure to remove expired cookies prevented Burp from working properly with some authentication mechanisms. There is a one-day tolerance for expiration times due to timezone anomalies on many applications, but this is generally acceptable since most applications set the expiry date on cancelled cookies to be far in the past.

A bug has been fixed affecting NTLM authentication when following redirects.

A further issue affecting NTLM authentication reported by some users appears to arise when browsers attempt to perform HTTP request pipelining. Burp Proxy now has two options which can be used to deter browsers from attempting pipelining: you can configure the Proxy to always use HTTP/1.0 in responses, and to always set the response header "Connection: close".

A bug affecting Sequencer's token analysis has been addressed. When analysing relatively small samples of tokens with large character sets (such as Base64-decoded binary data), Sequencer's probabilistic analysis was producing inaccurate character-level results, due to the small number of samples relative to the number of available characters. The fix for this is that Sequencer skips the character-level analysis when this condition is liable to occur. The bit-level analysis is not affected.
