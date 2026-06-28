# Professional / Community 2.1.04

Source: https://portswigger.net/burp/releases/professional-community-2-1-04
Fetched: 2026-06-28T09:16:33.032309+00:00

This release includes a number of minor enhancements and bugfixes.

In Burp Repeater, there are new options to close a tab, close all other tabs, and reopen a closed tab. You can access these actions via the context menu on the tab header, or by assigning hotkeys.

There is a new (default-on) scan option to ignore the protocols of URLs to scan. This is to avoid a  common user error where the scan is configured for http://example.com only, while it needs also to include https://example.com.

When a Burp update is available, there are options to mute the update notification for one week, for the currently offered update, or for all beta updates.

A bug affecting use of PKCS#11 smart cards affecting Burp 2.x has been fixed.
