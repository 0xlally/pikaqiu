# Manual application mapping

Source: https://portswigger.net/burp/documentation/desktop/tools/target/manual-app-map
Fetched: 2026-06-28T09:16:08.875352+00:00

Support Center

Documentation

Desktop editions

Tools

Target

Manual Application mapping

ProfessionalCommunity Edition

Manual application mapping

Last updated:

June 18, 2026

Read time:

1 Minute

You can choose between manual and automated application mapping. Consider the type of application and how you intend to use the results.

For some use cases, Burp's automated crawler is superior to manual mapping. The crawler captures the navigational paths in a way that lets Burp Scanner automatically maintain session when it audits the application.

If you map the application manually, you can guide the process and avoid potentially dangerous functionality. You can also make sure that navigational actions work as you expect, and familiarize yourself with the application.

To manually map the application:

Launch Burp's browser.

Browse the entire application manually.

Follow every link, submit every form, step through every multi-stage process, and log in to all protected areas.

This manual mapping process populates the Target site map with the content requested via the Proxy. In addition, you can use live passive crawling to map content that can be inferred from application responses, such as from links or forms. This process builds up a fairly complete record of all the visible application content.
