# Professional / Community 1.7.05

Source: https://portswigger.net/burp/releases/professional-community-1-7-05
Fetched: 2026-06-28T09:16:30.882688+00:00

This release introduces native platform installers for Windows, Linux and OS X. These install Burp together with a private Java runtime environment, so you don't need to worry about installing or updating Java. The installation of Burp is fully integrated with standard OS features (start menu, dock, taskbar etc.), making it easier to launch Burp without use of the command line.

Pro edition users can obtain Burp platform installers in two ways:

Log in to your account and choose which installer to download.

Use the existing update feature to obtain the latest Burp JAR file, run that, and choose "Download other installers" from the Help menu.

Free edition installers can be obtained directly from the download page.

Note that although the platform installers have been extensively tested on various platforms, these are officially experimental and we welcome users' feedback about how they perform in real-world conditions. We will continue to distribute plain JAR files for people who prefer those.

There is also improved handling of updates. When an update is available, Burp lets you view full details of the release, and choose which installer type to download. When a release is flagged as beta, you can choose whether to download the beta release or the latest stable release.

A number of other enhancements have also been made:

The performance of the Proxy history view filter has been considerably improved, and changes to the filter are applied much faster on very large histories.

Some instances where redundant data is saved to Burp project files have been fixed.

The options to select font size now permit selection of very large font sizes, as a workaround for lack of proper support for HiDPI screens on Java 8 and earlier.
