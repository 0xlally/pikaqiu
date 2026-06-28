# Professional / Community 2026.2

Source: https://portswigger.net/burp/releases/professional-community-2026-2
Fetched: 2026-06-28T09:16:56.541941+00:00

This release adds Organizer collections with secure sharing, a split request and response view in Intruder, Proxy search, plus performance improvements, bug fixes, and a browser upgrade.

Get more from Organizer with collections

We've upgraded Burp Organizer to give you a smarter way to triage and organize HTTP messages as your testing progresses.

Messages now land in a dedicated inbox, where you can quickly review and group them into collections that match how you work.

In Burp Suite Professional, you can securely share collections with other users via encrypted links, offering a straightforward way to pass on reproduction steps

or proof-of-concept traffic without manual workarounds.

Split request and response view in Intruder

Intruder now supports a split request and response view when reviewing attack results.

You can see both side-by-side, so you no longer need to switch between tabs to compare them.

This makes reviewing attack results faster and more straightforward, especially for larger attacks.

Quality of life improvements

We've made the following quality of life improvements:

Changes to SOCKS proxy settings (under Network > Connections

) are now only applied when you click OK

, not while you're still editing them.

You can now delete selected interactions from Collaborator to keep your results focused and manageable.

We've added a search bar to the Proxy HTTP and WebSocket history views, making it easier to find specific messages.

We've added a URL-encode key characters (unicode)

option to the Convert selection context menu. This gives you more control over how spaces and other characters are encoded.

Bug fixes

We've fixed the following bugs:

A display issue on Windows where selected text in the message editor didn't match the actual highlight, especially with custom scaling or larger fonts.

A certificate issue that caused some .NET applications to fail when proxying traffic through Burp.

An issue where the Next button in reported issues could highlight the wrong characters.

An issue where the wrong extension name could be shown when selecting from a filtered list in the Extensions tab.

An issue where WebSocket connections could fail after reopening a project if match and replace rules were enabled when the project was closed.

An issue where large HTTP requests sent to Burp AI from Repeater could fail with a generic error message. These requests now handle timeouts more reliably and avoid unnecessary credit usage.

Browser upgrade

We've upgraded Burp's browser to Chromium 145.0.7632.46 for Windows & macOS and 145.0.7632.45 for Linux.

For more information, see the Chromium release notes.
