# DNS Exfilnspector

Source: https://portswigger.net/bappstore/0e9c1b7acd25422ab1fd1df5d1f09bbd
Fetched: 2026-06-28T09:14:31.799349+00:00

Support Center

BApp Store

DNS Exfilnspector

Professional

DNS Exfilnspector

Download BApp

DNS Exfilnspector automatically decodes DNS exfiltration queries captured through Burp Collaborator, converting

blind remote code execution into visible output. The extension continuously monitors Collaborator interactions and

decodes exfiltrated data in real-time, eliminating the need for manual decoding.

Features

Automatic generation and reuse of Burp Collaborator links for multiple exfiltration sessions

Real-time monitoring and decoding of DNS queries with support for hex, base64, and base32 encoding

Configurable base64 character substitution for DNS-safe exfiltration (handles special characters like =, /, and

+)

Multi-line output support with automatic duplicate filtering and sequential ordering

Export functionality to save both raw DNS queries and decoded output locally

Usage

Navigate to the DNS Exfilnspector tab and click "Get New Link" to generate a Burp Collaborator domain

Select the encoding format (hex, base64, or base32) that matches your exfiltration method

For base64 exfiltration, configure the character substitution settings to match your DNS-safe replacements

(default: eqls for =, slash for /, plus for +)

Use the generated Collaborator link in your DNS exfiltration payload on the target system

The extension automatically monitors for DNS interactions, stops listening when data transmission completes, and

displays the decoded output

Click "Continue Listening" to reuse the same Collaborator link for additional exfiltration, or "Get New Link" to

generate a fresh domain

Use "Save Raw" or "Save Decoded" buttons to export the captured data to a local file

Author

Author

LazyTitan

Version

Version

1.3.0

Rating

Rating

Popularity

Popularity

Last updated

Last updated

07 January 2026

Estimated system impact

Estimated system impact

Overall impact:

Empty

Memory

Empty

CPU

Empty

General

Empty

Scanner

Empty

You can install BApps directly within Burp, via the BApp Store feature in the Burp Extender tool. You can also download them from here, for offline installation into Burp.

You can view the source code for all BApp Store extensions on our

GitHub page.

Follow

@BApp_Store on Twitter to receive notifications of all BApp releases and updates.

Please note that extensions are written by third party users of Burp, and PortSwigger Web Security makes no warranty about their quality or usefulness for any particular purpose.

Go back to

BappStore

Note:

Please note that extensions are written by third party users of Burp, and PortSwigger Web Security makes no warranty about their quality or usefulness for any particular purpose.
