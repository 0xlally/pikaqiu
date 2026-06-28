# Professional 1.2.07

Source: https://portswigger.net/burp/releases/professional-1-2-07
Fetched: 2026-06-28T09:16:22.217427+00:00

Burp Scanner is updated to allow the severity and confidence levels of scanner issues to be modified by the user. Issues can also be marked as false positives, and deleted.

To reclassify issues, select the desired issues in the Results tab, and use the right-click context menu to adjust the severity and confidence levels.

To delete issues, select the desired issues and use the context menu or the 'del' key to delete them.

Note that if you delete an issue, and Burp rediscovers the same issue (for example, if you rescan the same request), the issue will be reported again. If instead you mark the issue as a false positive, then this will not happen. Therefore, deletion of issues is best used for cleaning up the Results tree to remove hosts or paths you are not interested in. For unwanted issues within the functionality you are still working on, you should use the false positive flag.
