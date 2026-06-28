# Main DOM Invader settings

Source: https://portswigger.net/burp/documentation/desktop/tools/dom-invader/settings/main
Fetched: 2026-06-28T09:16:03.020095+00:00

Support Center

Documentation

Desktop editions

Tools

DOM Invader

Settings

Main

ProfessionalCommunity Edition

Main DOM Invader settings

Last updated:

June 18, 2026

Read time:

1 Minute

To access the DOM Invader settings menu, click the Burp Suite logo in the upper-right corner of the browser, then switch to the DOM Invader tab.

From the Main settings section, you have the following options.

Enable DOM Invader

This is the global toggle for enabling DOM Invader. DOM Invader is disabled by default as some of its features may interfere with the target website's functionality in a way that impacts your other testing activities. When enabled, you can access DOM Invader from its tab in the browser's DevTools panel.

Postmessage interception

When this setting is enabled, you can use the Messages view in the DevTools panel to test for DOM XSS in the site's web messages. For more information on DOM Invader's web message features, see Testing for DOM XSS using web messages.

There are also a few sub-settings that let you fine-tune this behavior. For more information, see Web message settings.

Customizing sources and sinks

To open the sources and sink settings, click the cog icon next to the main DOM Invader switch. From here, you can control which sources and sinks DOM Invader instruments. By default, all sources are hidden and only the most interesting sinks are instrumented.

You might want to disable instrumentation of a particular sink if it is preventing the site from working correctly. For example, instrumenting eval() can change its behavior and break the related functionality.
