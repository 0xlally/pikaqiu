# Professional 1.5.08

Source: https://portswigger.net/burp/releases/professional-1-5-08
Fetched: 2026-06-28T09:16:25.034964+00:00

This release includes various minor enhancements and bugfixes, including:

The Proxy has a new option to unpack compressed request bodies (previously only compressed responses were supported). This option is off by default as it may break some applications that require compressed requests.

Decompression of compressed content now works with .NET DeflateStream compression, and a bug affecting some other deflate implementations has been fixed.

The default Proxy match and replace rules include an available item to remove the Accept-Encoding header in requests, to deter servers from compressing response content.

The active scan queue is now much more responsive, in terms of providing real-time information about progress, and responding to cancel/pause actions.

A bug affecting NTLM negotiation with some servers has been fixed.

A bug which occasionally caused the Proxy history filter panel to become uneditable has been fixed.

A bug affecting the generation of per-host SSL certificates using a custom CA certificate that has been imported from another tool, has been fixed.

The function to save and restore state now provides verbose debug output on error, to facilitate debugging of problems.

A bug affecting the parsing of some ASP.NET ViewState structures has been resolved.
