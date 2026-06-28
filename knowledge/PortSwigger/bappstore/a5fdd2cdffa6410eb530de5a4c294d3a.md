# NGINX Alias Traversal

Source: https://portswigger.net/bappstore/a5fdd2cdffa6410eb530de5a4c294d3a
Fetched: 2026-06-28T09:14:54.347167+00:00

Support Center

BApp Store

NGINX Alias Traversal

Professional

NGINX Alias Traversal

Download BApp

This extension detects NGINX alias traversal due to misconfiguration.

The technique is based on Orange Tsai's BlackHat USA 2018

Presentation

A server is assumed to be vulnerable if a request to an existing path like https://example.com/static../ returns the same response as https://example.com/. To eliminate false positives the misconfiguration has to be confirmed by successfully requesting an existing resource via path traversal. This is done as follows:

For the URL https://example.com/folder1/folder2/static/main.css it generates the following links:

https://example.com/folder1../folder1/folder2/static/main.css

https://example.com/folder1../%s/folder2/static/main.css

https://example.com/folder1/folder2../folder2/static/main.css

https://example.com/folder1/folder2../%s/static/main.css

https://example.com/folder1/folder2/static../static/main.css

https://example.com/folder1/folder2/static../%s/main.css

Where %s are common directories used in alias paths based on around 9500 nginx configuration files from GH (thanks @TomNomNom), see directories.txt.

Author

Author

Martin Bajanik (@_bayotop)

Version

Version

1.1

Rating

Rating

Popularity

Popularity

Last updated

Last updated

03 December 2021

Estimated system impact

Estimated system impact

Overall impact:

Low

Memory

Low

CPU

Low

General

Low

Scanner

Low

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
