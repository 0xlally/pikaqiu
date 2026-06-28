# Professional 1.6

Source: https://portswigger.net/burp/releases/professional-1-6
Fetched: 2026-06-28T09:16:26.392698+00:00

This is the final v1.6 release.

Burp Suite Free Edition contains significant new features added since v1.5, including:

Support for WebSockets messages.

Support for PKCS#11 client SSL certificates contained in smart cards and physical tokens.

A new Extender tool, allowing dynamic loading and unloading of multiple extensions.

A new powerful extensibility API, enabling extensions to customize Burp's behavior in much more powerful ways.

Support for extensions written in Python and Ruby.

A new BApp Store feature, allowing quick and easy installation of extensions written by other Burp users.

An option to resolve DNS queries over a configured SOCKS proxy, allowing access to TOR hidden services.

Generation of CSRF PoC attacks using a new cross-domain XHR technique.

New options for SSL configuration, to help work around common problems.

Optional unpacking of compressed request bodies in the Proxy.

Support for .NET DeflateStream compression.

New and improved types of Intruder payloads.

New Proxy interception rules.

New Proxy match/replace rules.

Improved layout options in the Repeater UI.

An SSL pass-through feature, to prevent Burp from breaking the SSL tunnel for specified domains.

Support for the Firefox Plug-n-hack extension.

An option to copy a selected request as a curl command.

Burp Suite Professional contains a number of bugfixes and tweaks, added since the last beta version, including:

An occasional bug causing misplaced highlights on payloads in Scanner issues has been fixed.

A bug in which restoring default settings for the Extender tool didn't unload any currently running extensions has been fixed.

A display bug affecting the rendering of binary content (such as images) in the raw view of the HTTP message editor has been fixed.

A bug which prevented the automatic backup on exit feature from functioning in headless mode has been fixed.

In previous versions, Burp stored its preferences in separate locations for each major version. This caused persisted settings to be lost on upgrading to a new major version. This behavior has been modified, and from v1.6 onwards major versions will store their preferences in the same location. As a workaround to preserve settings from earlier releases, Pro users can launch the earlier release, save a state file containing their preferences, then launch the new release and load the state file.

Work is already underway on some exciting new features that will be arriving post v1.6 ...
