# Professional 1.6.13

Source: https://portswigger.net/burp/releases/professional-1-6-13
Fetched: 2026-06-28T09:16:26.742723+00:00

This release contains various bugfixes and minor enhancements:

The previous release introduced some bugs into the Target site map, causing scope-based view filters to be sometimes misapplied, and orphaned tree nodes to occasionally appear. These have now been fixed. In recent months, we have been extensively reworking the site map to support a number of planned new features, and we apologize that these bugs slipped through into the public release. We welcome further feedback about any site map problems and will aim to resolve these quickly.

Some Scanner issues that are reported on a per-host basis (for example, Flash cross-domain policy) were previously reported on the root host node of the Scanner results tree. These are now correctly reported at the node for a specific URL where applicable (e.g. /crossdomain.xml).

Relatedly, where a Scanner issue is created at a URL file node that does not exist in the Target site map, the corresponding item is added to the site map, including the actual request and response for that item. This change is useful in its own right, because the site map now contains more content that Burp has obtained from the target. It also paves the way for a planned enhancement to the site map, in which it will become a unified dashboard of both discovered content and Scanner issues. In the meantime, one behavioral quirk which arises is that if you restore a state file and select only to import Scanner issues, some new content corresponding to these issues may also be added to the site map. We believe that this interim behavioral change is relatively harmless, and will become fully desired behavior once the transition to the new site map is completed.

Some users have reported problems with certain extensions that cause a deadlock in the Burp UI when they are reloaded on startup. Burp now tries to detect this situation, and on the subsequent startup will skip the automatic reload of extensions. (Note that a further, existing, workaround for this problem is to add "usedefaults" to the Burp command line, to prevent reloading of any saved settings.)

When Burp fails to delete its temporary files on shutdown, because the OS does not release locks on those files, Burp now remembers the affected items and automatically deletes them on the subsequent startup, without the need to prompt the user. The old prompt will still be shown if unexpected temporary files are detected on startup.

A bug which prevented column resizing in the Intruder results table has been fixed.

A bug which made certain configured options cause problems when saving state files has been fixed.

A bug where multiple Proxy history views shared the same underlying view filter, preventing the use of different filters on each view, has been fixed.
