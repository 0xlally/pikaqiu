# Professional / Community 2023.2.2

Source: https://portswigger.net/burp/releases/professional-community-2023-2-2
Fetched: 2026-06-28T09:16:41.946526+00:00

This release upgrades Burp’s browser to a later version of Chromium and fixes a bug with the Intruder attack results window.

Browser update

This release upgrades Burp's browser to Chromium 110.0.5481.177 / 178. This upgrade contains a critical security fix, as well as several high-severity fixes.

Bug fix

This release fixes a bug in which Intruder attack results windows sometimes displayed requests and responses from multiple Intruder attacks that were launched from the same tab. Each window now only displays requests and responses relating to the originating attack.

Note for Windows Server 2012 and Windows 7/8/8.1 users

Due to a recent Chrome upgrade, Burp Scanner is no longer compatible with the Windows Server 2012 and Windows 7/8/8.1 operating systems. For more information, see the related Chrome announcement.
