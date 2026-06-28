# Community 1.6.01

Source: https://portswigger.net/burp/releases/community-1-6-01
Fetched: 2026-06-28T09:16:12.938422+00:00

This release backports to the Burp Suite Free Edition two security-related fixes that were applied in v1.6.17 Professional edition:

The Proxy now by default strips any Proxy-* headers received in client requests. Browsers sometimes send request headers containing information intended for the proxy server that is being used. Some attacks exist whereby a malicious web site may attempt to induce a browser to include sensitive data within these headers.

A bug in the following of cross-domain redirections, which caused Burp to include cookies from the original request in the redirected request, has been fixed. In some situations, the bug presents a security risk because sensitive data in cookies could be leaked to a different and potentially untrusted domain.

As always, users are encouraged to update to the latest Burp release to resolve these issues.

Other than these bugfixes, this release is functionally identical to v1.6 Free Edition.
