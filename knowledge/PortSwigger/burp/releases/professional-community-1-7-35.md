# Professional / Community 1.7.35

Source: https://portswigger.net/burp/releases/professional-community-1-7-35
Fetched: 2026-06-28T09:16:33.059005+00:00

This release includes a number of fixes and minor enhancements:

Further enhancements have been made to Burp's project repair function based on feedback from the previous release. We welcome further feedback of any situations in which data cannot be recovered from a corrupted Burp project file.

A fix has been applied to prevent Burp's filter popups from appearing in the task switcher on some Linux window managers.

The hardening of SSL validation that was added in 1.7.34 unfortunately didn't work correctly for some users who access the web via a network proxy. This affected Collaborator polling, Burp updates, and the BApp Store. Users with a configured upstream proxy who have already updated to 1.7.34 and have encountered this problem will not receive the update notification for this release. Those users will need to either (a) remove the upstream proxy configuration temporarily; or (b) run an older version of Burp to obtain the update.
