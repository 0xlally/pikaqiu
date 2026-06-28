# Professional 1.5.05

Source: https://portswigger.net/burp/releases/professional-1-5-05
Fetched: 2026-06-28T09:16:24.710616+00:00

This release contains a number of feature enhancements and bugfixes, including:

The SOCKS proxy support now has an option to perform DNS lookups remotely via the proxy. This enables Burp to access TOR hidden services, and to work in some unusual infrastructures. When this option is enabled, no local DNS lookups will be performed by Burp.

The per-installation CA certificate and key used by Proxy listeners to create per-host certificates can now be exported for use with other tools or another instance of Burp. You can also import a certificate and key into the current instance. The export/import function can be accessed via the Proxy listener configuration panel. Note that you should not disclose the private key for your certificate to any untrusted party. A malicious attacker in possession of your certificate and key may be able to intercept your browser's HTTPS traffic even when you are not using Burp.

Your CA certificate (not the key) can now be downloaded by visiting http://burp/cert in your browser (configured to use Burp as its proxy). This makes it easier to install the certificate on some mobile devices.

The IBurpExtenderCallbacks interface has two new methods, unloadExtension and get CommandLineArguments.

The implementation of per-extension persistent preferences has been modified to use sub-nodes of Burp's preferences store, allowing extensions to use much longer preference names. Preferences saved by extensions using earlier versions of Burp will unfortunately be lost.

There is a new option in Burp Proxy's miscellenaeous options to disable logging to the Proxy history and target site map. This option may be useful if you are using Burp Proxy for some specific purpose, such as authenticating to upstream servers or performing match-and-replace operations, and you want to avoid incurring the memory and storage overhead that logging entails.

The Target Analyzer function now includes a column in the parameters view to show the value observed for the selected parameter in each request that uses it.

There is now a command-line license activation process for use in headless installations of Burp.

Burp now allows interactive debugging of extensions.
