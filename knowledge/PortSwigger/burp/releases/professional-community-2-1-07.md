# Professional / Community 2.1.07

Source: https://portswigger.net/burp/releases/professional-community-2-1-07
Fetched: 2026-06-28T09:16:33.098864+00:00

This release considerably improves Burp's SSL/TLS coverage.  Historically, quirks in different server-side implementations together with bugs in the client-side Java stack led to problems connecting to some web sites. These have now been virtually eliminated.

The Venn diagram below shows how Burp's coverage now compares with Google Chrome for the Alexa top 100,000 sites. Burp achieves substantial overlap with Chrome. Burp can connect to 1,696 sites that Chrome does not, and only fails to connect to 125 sites that Chrome can connect to.

(Note that Burp's additional coverage is largely because Burp tolerates some older and weaker protocols and ciphers, in the interests of maximizing connectivity.)

Various improvements have been made to the crawling phase of scans:

The event log contains improved feedback regarding account self-registration and login.

Crawling is more efficient, with substantially fewer requests needed to discover the same range of locations.

Various minor bugs have been fixed.
