# Professional 1.2.12

Source: https://portswigger.net/burp/releases/professional-1-2-12
Fetched: 2026-06-28T09:16:22.407236+00:00

1. This release adds a new "find references" feature, which you can access via the context menus throughout Burp:

Anywhere you see an HTTP request, URL, domain, etc., you can use the "find references" function to search all of Burp's tools for HTTP responses which link to that item. When you view an individual search result, the response is automatically highlighted to show where the linking reference occurs:

Note that this feature treats the original URL as a prefix when searching for links, so if you select a host, you will find all references to that host; if you select a folder, you will find all references to items within that folder or deeper.

The new "find references" feature effectively serves the same purpose as the "linked from" list that existed in earlier versions of Burp Spider, but is much more powerful.

2. There is a new autosave feature, which saves a backup of Burp's state in the background at a configurable interval:

This setting persists across reloads of Burp. So you can configure Burp to always save its state to a local temp directory, and know that every time you use Burp you will have a backup copy of your work.

3. The HTTP message editor now has an option to URL-encode relevant characters as you type. If this option is turned on (via the context menu) then characters like & and = will be automatically replaced with their URL-encoded equivalents as you type:

4. The live active scanning feature has been modified to ignore requests for media resources (images, etc.) where the request does not contain any non-cookie parameters. Requests like these are virtually always for static resources which do not have any security significance, and so can be safely ignored by the scanner.

Note that despite this change to the live scanning feature, if you manually select items like these and send them for active scanning, then they will of course be scanned in the normal way.
