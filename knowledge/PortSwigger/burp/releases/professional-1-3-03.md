# Professional 1.3.03

Source: https://portswigger.net/burp/releases/professional-1-3-03
Fetched: 2026-06-28T09:16:23.053778+00:00

This release addresses a number of stability issues, particularly on non-Sun JRE platforms like Apple and OpenJDK:

Occasional UI freezes during updates to the site map (during spidering, content discovery etc.).

Occasional UI freezes when toggling Proxy interception during display of large responses.

Complete failure to run on OpenJDK.

The moral of this story has been: don't assume that thread synchronization works the same way on all JREs. It's difficult to promise that there won't be any more of these issues, but initial feedback from Mac users has been positive. If you do encounter any more stability issues, please do let me know.

There are some minor bugfixes affecting all users. And the changes to the thread synchronization model have made some of Burp's functionality run a fair bit faster than previously.

The Sun JRE remains the only offically supported platform for Burp, but this release should make life much easier for users of other platforms.
