# Professional / Community 1.6.28

Source: https://portswigger.net/burp/releases/professional-community-1-6-28
Fetched: 2026-06-28T09:16:30.371665+00:00

This release adds the ability to annotate the active scan queue with comments and highlights, as is already possible in the Proxy history and Target site map:

Recently, we removed the ability to delete items from the active scan queue. This was done in preparation for some planned new capabilities that will enable the Scanner to retrospectively report issues for scan queue items that have finished scanning. For this capability to work, we needed to retain the full scan queue history. Some users have complained that they were using the deletion of items as part of their testing workflow. To address this issue, we have added the ability to apply comments and highlights to scan queue items. This provides an improved alternative to the previous workflow that these users were following.

A number of other changes have been made:

The performance of the Target site map when selecting tree branches containing very large numbers of scan issues has been dramatically improved.

The process of configuring Burp to use a PKCS#11 certificate has been improved. You can now manually select the required card slot during installation, swap cards at runtime, and reload configuration from state files more easily.

There is a new Scanner option to create an insertion point for the entire request body, for relevant content types. This currently applies to requests with XML or JSON content in the request body. This insertion point is enabled by default, and should allow detection of some additional edge-case vulnerabilities (e.g. server-side JavaScript injection where an entire request body containing JSON is passed to the JavaScript eval function).

The Scanner insertion point type that was previously called "REST-style URL parameters" has been replaced with two insertion point types, covering URL path folders and the final URL filename. The filename insertion point is enabled by default, while folder insertion points are still disabled. This change should improve Burp's detection of some issues in its default configuration, such as XSS through reflection of the full URL path excluding the query string.

A bug that caused occasional corruption of saved state files and prevented them from correctly reloading has been fixed.

Scanner issues that are reported by Burp extensions are now identified as such within the UI and scan reports. This was primarily done to reduce the number of support tickets relating to defects in the wording of extension-generated issues.

The temporary directories created by Burp should now not be world-readable on any platforms, to prevent direct access to Burp's temporary files from other users on a multi-user machine. Note that by default such users can in any case access a large quantity of sensitive data, and interfere with Burp's operation, via the default Proxy listener on 127.0.0.1:8080. Users are encouraged not to use Burp on a machine that is shared with untrusted users.
