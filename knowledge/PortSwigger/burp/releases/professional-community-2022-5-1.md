# Professional / Community 2022.5.1

Source: https://portswigger.net/burp/releases/professional-community-2022-5-1
Fetched: 2026-06-28T09:16:38.608408+00:00

This release adds a number of enhancements to Burp Scanner, including several new JWT-based scan checks and an option to skip unauthenticated crawling when you've provided application logins. The BApp Store now also provides in-app feedback on how much load BApps are placing on your system.

JWT scan checks

JWT implementations often contain serious vulnerabilities, but these can be tricky to thoroughly audit. Burp Scanner can now detect 8 common JWT-based vulnerabilities - saving you time, and making it easier to secure sites that use JWTs.

For more details, please see the individual issue definitions in Burp on the Target > Issue definitions tab.

Feedback on BApp performance impact

On the Extender > BApp store tab, we now display an indication of how much load we estimate that each BApp places on your system.

The estimated system impact is divided into the following categories:

Memory shows what impact the BApp is likely to have on Burp Suite's memory usage.

CPU shows an estimate of how much additional load the BApp places on your CPU.

Time shows the BApp's impact on the speed of Burp Suite. This includes the responsiveness of the interface and how long tools take to complete tasks.

Scanner shows the likely impact on how long scans take to complete.

Overall shows the highest impact rating across all of these categories.

If you think that Burp is performing slower than it should be, we recommend checking these estimates for any BApps that you have loaded and removing those that you're not actively using. This should help you to extend Burp's capabilities without impairing performance.

Using multiple extensions at the same time has a cumulative effect on performance. The bar at the top of the screen shows the cumulative impact of all of the BApps that are currently loaded.

Skip unauthenticated crawling during scans

You can now choose to skip unauthenticated crawling in cases where you have provided application logins for Burp Scanner to use. This helps to reduce the crawl time.

To enable this option, go to the Crawl Optimization settings in your scan configuration and select Crawl using my provided logins only. Note that if you do not provide any application logins, the crawler automatically reverts to performing an unauthenticated crawl instead.

Set headers in session handling options

You can now use Burp Suite's session handling options to add headers and values to requests. When you create a session handling rule using the new Set a specific header value action, the header and value pair you provide are added to any requests that are within the rule's scope.

Verify upstream TLS

Burp Suite has always used fully verified TLS to connect to known services, such as portswigger.net and the public Burp Collaborator server. However, when communicating with arbitrary websites, it does not verify upstream TLS certificates and supports weak ciphers by default. This maximizes compatibility at the expense of protection against active man-in-the-middle (MITM) attacks.

If you're concerned about the possibility of an active MITM attack on your communication with the site that you're testing, you can now configure Burp to verify upstream TLS certificates. To do this, go to Project settings > TLS and select the Verify upstream TLS checkbox.

In this scenario, we recommend also selecting the Use default protocols and ciphers of your Java installation option to prevent Burp from using weak ciphers.

Please note that additional hardening is planned for this feature in the future.

Improved Repeater tab behavior

We have made several minor tweaks to the appearance and behavior of tabs in Burp Repeater. These will pave the way for some additional features in the future.

When Repeater tabs overflow onto a new row, these now stay the same size rather than stretching to fill the entire row. This makes it easier to keep track of where tabs are.

From the context menu, you now have options for renaming tabs and deleting all tabs to the left or right of the current tab.

There is a new actions menu (3 dots) in the upper-right corner of the screen. At the moment, this provides a limited range of options, but we'll continue to add to this in the future.

Browser upgrade

We have upgraded Burp's browser to Chromium 102.0.5005.61

Other improvements

We have added a range of common Google Analytics cookies to the list of ignored insertion points for scans.

We have improved the performance of Burp Scanner by tweaking the way we identify locations to audit after the crawl is completed.

In your scan configuration, you can now define separate timeout settings for the crawl and audit phases of a scan, overriding the global project setting.

Changes to Java requirements

Burp Suite now requires Java 11 or later to run. This change should not impact you unless you installed Burp Suite as a .jar file, as the installer includes a bundled private Java Runtime Environment so that you don't need to worry about installing or updating Java. However, any extensions written in a version of Java earlier than 11 may not run correctly from this release onward.

Bug fixes

We have resolved some performance issues that some users faced when using Intruder with large resource pools.

We have fixed an issue whereby Intruder's Copy attack config menu item was sometimes unresponsive.

We have fixed an issue with scan configurations whereby the Crawl using my provided logins only setting was not displaying correctly on the edit configuration menu. This setting was showing as unselected even for configurations where it had been selected during the initial setup process.

We have fixed an issue whereby the live passive crawl task was not automatically processing responses pushed from Repeater.
