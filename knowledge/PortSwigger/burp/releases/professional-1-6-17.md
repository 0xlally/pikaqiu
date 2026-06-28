# Professional 1.6.17

Source: https://portswigger.net/burp/releases/professional-1-6-17
Fetched: 2026-06-28T09:16:26.955942+00:00

This release contains a number of minor enhancements and bugfixes:

The Proxy now uses SHA256 to generate its CA and per-host certificates if this algorithm is available, otherwise it fails over to using SHA1. Updating to a SHA256-based CA certificate removes SSL warnings in some browsers.

There is a new button at Proxy / Options / Proxy Listeners to force Burp to regenerate its CA certificate. You will need to restart Burp for the change to take effect, and then install the new certificate in your browser. You can use this function to help switch to using a SHA256-based CA certificate.

A bug in the "Paste from file" function which caused Burp to sometimes retain a lock on the selected file has been fixed.

A bug in the Intruder "extract grep" function, which sometimes caused extracted HTML content to be rendered as HTML in the results table, has been fixed.

The Proxy now by default strips any Proxy-* headers received in client requests. Browsers sometimes send request headers containing information intended for the proxy server that is being used. Some attacks exist whereby a malicious web site may attempt to induce a browser to include sensitive data within these headers. There is a new option at Proxy / Options / Misc allowing you to configure Burp to leave these headers unmodified if desired.

A bug in the Collaborator server configuration settings, in which Burp would wrongly add the prefix "polling." to the configured location of a private polling server, has been fixed. The documentation on deploying a private Collaborator server has been updated to clarify the use of the "polling" subdomain in some Collaborator server configurations.

A bug which caused the use of the request throttle option in Sequencer live capture to delay the initial rendering of the live capture UI has been fixed.

A bug in the issue selection step of the Scanner reporting wizard, which caused all extension-generated issues to be shown using the name of the first extension-generated issue, has been fixed. Extension-generated issues are now always labelled as "Extension-generated" in this panel.

A bug in the following of cross-domain redirections, which caused Burp to include cookies from the original request in the redirected request, has been fixed. In some situations, the bug presents a security risk because sensitive data in cookies could be leaked to a different and potentially untrusted domain. As always, users are encouraged to update to the latest Burp release to resolve this issue.

The Spider now ignores Burp Collaborator URLs when attempting to extract links from within response text. Some applications contain functionality to store and retrieve textual inputs. When these applications are scanned using Burp, they are prone to store some or all of the payloads that Burp sends during scanning, and return these in later responses. It is preferable for Burp not to add any returned Collaborator URLs to the site map when spidering.
