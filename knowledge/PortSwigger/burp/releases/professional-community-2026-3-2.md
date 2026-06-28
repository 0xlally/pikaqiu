# Professional / Community 2026.3.2

Source: https://portswigger.net/burp/releases/professional-community-2026-3-2
Fetched: 2026-06-28T09:16:56.792426+00:00

This release introduces custom CA certificate support, host-level SOCKS proxy bypass, the ability to hide decoded hover tooltips, and some bug fixes.

Custom CA certificates

You can now add certificate authorities (CAs) directly in Burp. This removes the need for manual workarounds to connect through intercepting proxies or to services that use certificates signed by an internal certificate authority.

To add a certificate, go to Settings > Network > TLS > Custom CA certificates and add your CA certificate.

Quality of life improvements

We've made the following quality of life improvements:

You can now specify hosts that should bypass a configured SOCKS proxy, instead of sending all connections through it.

You can now hide decoded text tooltips that appear when hovering over request and response content, preventing large tooltips from obscuring your view.

Bug fixes

We've fixed the following bugs:

An issue that allowed unsupported file types to be uploaded via manual installation in the BApp Store.

An issue where removing an extension from a filtered list in the Extensions tab could remove the wrong extension.

An issue affecting Montoya API extensions where requests created without an associated HttpService could fail silently during network operations. Burp now reports a clearer error if this occurs.

Browser upgrade

This release upgrades Burp's browser to Chromium 146.0.7680.178 for Windows & Mac and 146.0.7680.177 for Linux. For more information, see the Chromium release notes.
