# Professional / Community 2020.12.1

Source: https://portswigger.net/burp/releases/professional-community-2020-12-1
Fetched: 2026-06-28T09:16:34.068747+00:00

This release provides performance and user interface improvements, a JavaScript analysis improvement, and several bug fixes.

Performance improvements

We have made significant improvements in both speed and memory usage in the message editor when handling large messages.

User interface improvements

We have improved several aspects of the user interface. There are new colors for various buttons, icons, check boxes, and radio buttons, to be in line with the new branding of Burp Suite. There are now tooltips for scan phases and issue counts in the scan task Audit Items view.

Processing dynamically created scripts

Burp Scanner's dynamic JavaScript analysis will now load dynamically created scripts, such as document.write('<script src="…">') or document.createElement('script’).

Bug fixes

This release also provides the following bug fixes:

In Burp Proxy, the message editor now consistently displays the correct view when switching between items in the HTTP history.

When using the context menu in the "Issue activity" section of Burp's dashboard, options provided by extensions are now displayed correctly.

Long payload lists in Burp Intruder now correctly include all entries from the corresponding short list, as well as extra items.
