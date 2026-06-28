# Professional / Community 1.6.25

Source: https://portswigger.net/burp/releases/professional-community-1-6-25
Fetched: 2026-06-28T09:16:30.164867+00:00

This release adds a new scan check for external service interaction and out-of-band resource load via injected XML stylesheet tags. Burp now sends payloads like:

<?xml version='1.0'?><?xml-stylesheet type="text/xml" href="http://tqnm38srfkzw67vux9rred.burpcollaborator.net"?>

and reports an appropriate issue based on any observed interactions (DNS or HTTP) that reach the Burp Collaborator server.

The release also fixes some issues:

A bug that caused the file path traversal scan check to produce false negatives in some edge cases has been fixed.

A bug that could cause the list of loaded extensions to become corrupted or deadlocked when restarting Burp with a large number of extensions configured has been fixed.

A bug that caused some items in the site map to be incorrectly placed after restoring state has been fixed.

A bug that caused changes made to the cookie jar configuration to be not applied until the next restart has been fixed.
