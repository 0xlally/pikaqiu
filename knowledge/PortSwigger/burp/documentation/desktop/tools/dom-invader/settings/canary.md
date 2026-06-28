# DOM Invader canary settings

Source: https://portswigger.net/burp/documentation/desktop/tools/dom-invader/settings/canary
Fetched: 2026-06-28T09:16:02.727886+00:00

Support Center

Documentation

Desktop editions

Tools

DOM Invader

Settings

Canary

ProfessionalCommunity Edition

DOM Invader canary settings

Last updated:

June 18, 2026

Read time:

1 Minute

From the DOM Invader settings menu, you can modify and update the canary string that DOM Invader injects into the target site.

To access the DOM Invader settings menu, click the Burp Suite logo in the upper-right corner of the browser, then switch to the DOM Invader tab.

At the bottom of the settings menu, you can see the current canary string that DOM Invader is tracking. You have the following options.

Copying the canary

You can click Copy to copy the current canary string to your clipboard. This is useful for manually injecting the string into different sources.

Changing the canary

You can replace the randomly generated default canary at any time and instead track your own custom canary string.

To change the canary:

Enter the string that you want to use in place of the default canary. Alternatively, click Randomize to generate a new random string.

Click Update canary.

Click Reload to refresh the browser. This is necessary for your changes to take effect. DOM Invader will now track the new canary string instead.

Note

To avoid false positives, make sure that the string you use doesn't occur naturally on the page.
