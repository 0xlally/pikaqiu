# Professional 1.6beta

Source: https://portswigger.net/burp/releases/professional-1-6beta
Fetched: 2026-06-28T09:16:28.184409+00:00

This release introduces the BApp Store, a repository of Burp extensions that have been written by users of Burp Suite, to extend its capabilities:

You can install BApps with one click from within Burp, and you can also download them from the BApp Store web site for manual installation on machines without Internet access. We've assembled an initial list of extensions and will hopefully be adding more soon.

The handling of URL-encoding of parameters within session handling macros has been rationalized, to make Burp "just do" the right thing in nearly every case, without the need for any special configuration by the user. Previously, there was a per-parameter configuration option whether to URL-encode its value. Since Burp actually knows the context in a response from which a parameter's value is being derived, and the context in a subsequent request into which it is being placed, Burp can automatically take care of the encoding in exactly the cases where it is needed.

The exception to this, where some manual configuration is still required, is where you have configured a custom parameter location within a response. Since this is a custom location, you need to tell Burp whether or not the raw extracted value is already URL-encoded, and Burp will handle it correctly when using its value in subsequent requests.

A bug that was introduced in v1.5.21, affecting Proxy SSL negotiation in cases where the client has only specified an IP address, has been fixed. The previous behavior, where Burp fetches the authentic SSL certificate from the destination host and forges a copy signed by its own CA certificate, has been restored. This technique is necessary to support Android clients, which only send a target's IP address in the CONNECT request that precedes the SSL negotiation.

This is officially a beta release, and when the final version is released, relevant changes since v1.5 will be ported into a new release of Burp Suite Free Edition.
