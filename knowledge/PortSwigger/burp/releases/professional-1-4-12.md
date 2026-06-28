# Professional 1.4.12

Source: https://portswigger.net/burp/releases/professional-1-4-12
Fetched: 2026-06-28T09:16:24.277858+00:00

This release resolves a problem with proxying SSL connections from Android clients. When Android proxies SSL, it resolves the destination hostname locally, and issues a CONNECT request containing the host's IP address. In earlier versions, Burp would then generate an SSL certificate with the IP address as its subject name, causing the Android client to show an SSL error, because the subject name on the certificate did not match the original hostname that Android had resolved.

Burp now behaves differently. If a CONNECT request is received containing an IP address, Burp connects to the destination server to obtain its SSL certificate. Burp then generates an SSL certificate with the same subject name (and alternative subject names, if defined) as the server's actual certificate. Assuming the server is returning a valid certificate for the hostname that Android is requesting, this should remove the SSL errors relating to the mismatched hostname.

(Note that it is still necessary to install Burp's CA certificate in the Android client, as for other SSL clients.)

A number of bugs are also fixed:

Some further causes of deadlock in the new UI.

A bug in the Scanner, where the "skip all tests" configuration was not properly applied to REST parameters.

An error saving and restoring state in headless mode, which was introduced in recent versions.

A bug in the macro item editor UI which prevented the list of items from scrolling properly.

Finally, the active scan wizard for consolidating multiple scanned items now contains an option to remove items with no parameters. (Note that this option should not necessarily be used automatically, because items with no parameters are normally fast to scan, and may still contain interesting bugs that can only be found via the active scanner.)
