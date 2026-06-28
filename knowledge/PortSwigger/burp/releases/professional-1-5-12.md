# Professional 1.5.12

Source: https://portswigger.net/burp/releases/professional-1-5-12
Fetched: 2026-06-28T09:16:25.241367+00:00

This release contains various enhancements and bugfixes:

There is a new payload type in Intruder, which copies the value of the current payload at another payload position. You can also define processing rules to systematically derive one payload from another, rather than copying its literal value. This function is useful in cases where you need to submit the same payload in two locations, or where one parameter is derived from (e.g. a hash of) the parameter that you need to test.

You can define Proxy interception rules based on the listener port number, so you can e.g. prevent interception of all messages on a specific listener.

The IResponseInfo interface has two new methods: getStatedMimeType() and getInferredMimeType().

The memory overhead of saving and restoring state, and performing search operations, is reduced.

The Scanner no longer prompts the user for confirmation when an extension programmatically initiates a scan of an out-of-scope item.

The problem with superfluous whitespace characters appearing when text is copied from the Scanner advisory panel into another application has been resolved.

The CSRF PoC generator now properly escapes tag brackets when using the XHR method, to prevent any closing script tags that are required within the generated request message from breaking the PoC script.

Parameter matching between macro items now tolerates URL-encoding of parameter names when performing matching.

A bug where certain nonprinting characters were corrupted when loading Intruder payloads from a file has been resolved.
