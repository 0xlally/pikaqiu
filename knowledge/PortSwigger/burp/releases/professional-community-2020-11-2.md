# Professional / Community 2020.11.2

Source: https://portswigger.net/burp/releases/professional-community-2020-11-2
Fetched: 2026-06-28T09:16:33.069105+00:00

This release updates the look of Burp's UI and adds an option for watching crawls in a headed browser.

UI refresh

This release gives Burp's UI a make-over, with a cleaner, more modern look.

You can choose between light or dark theme at User options / Display / User interface.

Crawling with a headed browser

You can now choose to start scans using a headed browser. In this case, when the crawl starts, a new browser window will open in which you can watch the crawler navigating around the target website in real time. This is useful for troubleshooting any issues.

You can enable this option from the miscellaneous crawl settings of your scan configuration.

If you enable this option, please note that Burp Scanner will occasionally open additional browser windows during the crawl and stop using the previous window. This is perfectly normal. Any redundant windows will automatically be closed after a period of time.

Other improvements

This release also provides the following improvements:

A new search function has been added to the BApp Store tab.

If you add a user.vmoptions file in the same folder as the BurpSuitePro.vmoptions file, Burp will load these settings instead. This file will not be changed by Burp, which means you no longer have to manually back up your custom vmoptions when updating Burp.

Burp's embedded browser has been upgraded to Chromium version 87.0.4280.66.

Bug fixes

All keyboard shortcuts now work as expected on the Intercept tab.
