# Pentagrid Scan Controller

Source: https://portswigger.net/bappstore/e3dde890bdce4ae4bcef0d97019f5d46
Fetched: 2026-06-28T09:15:02.438713+00:00

Support Center

BApp Store

Pentagrid Scan Controller

Professional

Pentagrid Scan Controller

Download BApp

Pentagrid Scan Controller enhances automated and semi-automated active scanning by intelligently filtering and preprocessing requests. It aims to reduce unnecessary scans, such as those targeting static files or non-repeatable requests, by assessing repeatability and injecting Hackvertor tags when needed. The extension provides transparency for each decision, allowing users to adjust behaviors as necessary.

Features

Identifies and filters out non-repeatable or irrelevant requests from active scanning.

Attempts to make non-repeatable requests repeatable using Hackvertor tags.

Displays detailed reasons for scanning decisions, enabling user review and customization.

Improves performance by minimizing redundant or ineffective scan traffic.

Usage

Add the target website to the scope.

Enable Proxy requests under Scan -> Options -> Requests to process.

Browse the application using Burp's built-in browser to generate traffic.

Open the extension's tab to view which requests have been actively scanned.

Review requests with a high "Interesting" rating that haven't been scanned (indicated by Scanned: false).

Sort by the "Reason" column to understand why certain requests were or were not scanned.

Check the Dashboard for active scan findings.

Note: This extension requires the Hackvertor extension to be installed and active.

Author

Author

Tobias 'floyd' Ospelt, @floyd_ch

Version

Version

0.2

Rating

Rating

Popularity

Popularity

Last updated

Last updated

13 June 2025

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
