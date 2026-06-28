# Enabling DOM Invader

Source: https://portswigger.net/burp/documentation/desktop/tools/dom-invader/enabling
Fetched: 2026-06-28T09:16:02.858555+00:00

Support Center

Documentation

Desktop editions

Tools

DOM Invader

Enabling DOM Invader

ProfessionalCommunity Edition

Enabling DOM Invader

Last updated:

June 18, 2026

Read time:

1 Minute

DOM Invader is preinstalled in Burp's browser, but is disabled by default as some of its features may interfere with your other testing activities.

To enable DOM Invader:

Go to the Proxy > Intercept tab and open Burp's browser.

In the upper-right corner of the browser window, click the Burp Suite logo. If you can't see this logo, click the jigsaw icon first. A panel opens containing tabs for the Burp Suite Navigation Recorder and DOM Invader settings menu.

From the DOM Invader settings, toggle the switch so that DOM Invader is on.

Click Reload to refresh the browser. This is necessary for your changes to take effect.

Right-click anywhere in the main browser window and select Inspect to open the browser's DevTools panel. Note that this now contains the DOM Invader tab. For the best experience, we recommend docking the panel to the bottom of the browser window.

Note

By default, DOM Invader remembers your previous settings, including whether it was on or off. Keep this in mind if you close Burp's browser while DOM Invader is still enabled. To disable this behavior, go to Settings > Tools > Burp's browser and deselect Store settings and history after closing.
