# Professional / Community 2022.6.1

Source: https://portswigger.net/burp/releases/professional-community-2022-6-1
Fetched: 2026-06-28T09:16:38.548541+00:00

This release introduces several improvements to the Intruder and Repeater tab bars, including the ability to select between a scrolling or wrapped tab view and, for Repeater, the ability to organize tabs into groups. It also introduces HTTP/1 keep-alive, in which Burp Suite can now reuse a single TCP connection to send multiple HTTP/1 requests, and adds a selection of preset scan modes to the Scan Configuration menu. Finally, we have released several key improvements for DOM Invader, including the ability to test for client-side prototype pollution.

Grouped Tabs

You can now organize Repeater tabs into color-coded groups. Grouping tabs makes it easier than ever to work with large numbers of open tabs and keep track of related requests.

We have also added a search function to the tab bar, which you can use to search for individual tabs or groups.

Scrollable tab view

Intruder and Repeater now provide two views for tabs. As well as the standard wrapped view, you can now also display tabs as a single, scrollable row. This can help to free up on-screen real estate, especially on smaller displays.

DOM Invader improvements

This release provides the following key improvements to DOM Invader:

You can now use DOM Invader to test for client-side prototype pollution.

The augmented DOM view now displays additional information to help you analyze vulnerabilities and potentially craft exploits. This includes the frame path, the outer HTML of the element, and the event that occurred when your payload was passed to the sink. Similarly, the Messages view now tells you both the frame that each message was sent from and the frame that it was sent to.

You can now set a callback function for each sink, source, and message that DOM Invader finds. This enables you to log the results using custom JavaScript code.

You can now prevent DOM Invader from consolidating messages with duplicate values. This is useful in cases where you want to see every single message being sent.

You can now disable specific sources and sinks to reduce noise.

For an overview of how to use these new features from PortSwigger researcher and creator of DOM Invader, Gareth Heyes, check out the following video:

HTTP/1 keep-alive

You can now send multiple HTTP/1 requests using the same TCP connection. Previously, Burp always closed the connection after each request / response pair, even if the server supported connection reuse.

Reusing connections in this way brings significant benefits in terms of request speed and timing accuracy.

To enable HTTP/1 keep-alive, go to Project options > HTTP > HTTP/1 and select the Use keep-alive for HTTP/1 if the server supports it option. You can override this setting in Repeater using the Enable HTTP/1 keep-alive reuse menu option.

Preset scan modes

You can now select from four preset scan modes when configuring a scan. These preset scan modes offer a quick way to adjust how the scan balances speed and coverage, without requiring you to set up a custom scan configuration.

To use these new scan modes, select Use a preset scan mode from the Scan Configuration menu and choose one of the available options.

Other improvements

We have made numerous improvements to Burp Scanner to improve stability, performance, and progress estimation.

Security fixes

This release provides the following security improvements:

This release upgrades Burp's browser to Chromium 103.0.5060.53, which patches a critical security issue. It also fixes several minor bugs related to Repeater tabs.

We have resolved a low-severity security issue that could lead to Repeater and Intruder disclosing URLs due to incorrectly interpreting a crafted response as a redirect. This issue was privately reported to us via our bug bounty program.

We have hardened Burp’s Referer calculation, bringing it in line with the default Referrer-Policy settings used in modern browsers.

Bug fixes

This release also provides a number of bug fixes. Most notably:

Burp's browser no longer issues unnecessary requests to Google on launch.

We have fixed an issue whereby Repeater responses could be overwritten by long-running requests.

We have fixed an issue with logging in headless mode, whereby the log file was being created but no data was being written to the log.
