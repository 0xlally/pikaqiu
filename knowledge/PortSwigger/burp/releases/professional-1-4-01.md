# Professional 1.4.01

Source: https://portswigger.net/burp/releases/professional-1-4-01
Fetched: 2026-06-28T09:16:24.114353+00:00

This release fixes a number of bugs, most notably:

A thread synchronization problem that caused the proxy to stop forwarding requests in certain high-volume conditions.

A problem with the NTLMv2 negotiation which caused it to fail against certain server configurations.

A bug that sometimes caused active scan tasks to fail silently.

The release also contains several enhancements to the handling of parameters in macros, including:

The option to URL-encode parameters in macro requests is now by default applied only to derived parameters. Preset parameter values are now not encoded by default, because they are typically already encoded within the configured request.

In the "run macro" action, there is a new, default-on option to URL-encode parameter values in the current request that have been derived from the final macro response.

In the "run macro" action, there is a new, default-off option to tolerate a mismatched URL when attempting to match parameters from the final macro response. This is useful for URL-agnostic anti-CSRF tokens, and enables you to configure a single macro to retrieve a valid token, which you can use in requests to multiple URLs, considerably simplifying the necessary Burp configuration in some applications.

A compatibility issue with Java 7 has been resolved. Burp will still display a compatibility warning on this platform until full testing has been carried out and any further issues dealt with.
