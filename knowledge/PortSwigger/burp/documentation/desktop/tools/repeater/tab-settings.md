# Configuring tab-specific settings

Source: https://portswigger.net/burp/documentation/desktop/tools/repeater/tab-settings
Fetched: 2026-06-28T09:16:08.729789+00:00

Support Center

Documentation

Desktop editions

Tools

Repeater

Configuring tab-specific settings

ProfessionalCommunity Edition

Configuring tab-specific settings

Last updated:

June 18, 2026

Read time:

1 Minute

You can override the global Repeater settings selected in the Settings dialog for an individual tab.

To configure tab-specific settings:

Select the tab you want to configure.

Click the settings icon next to the Send button to display a context menu containing Repeater settings. The available settings are the same as those found in the Settings dialog.

Select the required settings from the menu.

If you select a setting on the tab-specific menu then Repeater ignores all global settings for that tab. Make sure that all settings are configured correctly on the tab-specific menu before you send requests from the tab. For example, if you select Process cookies in redirections on the global Repeater menu, and Enable HTTP/1 connection reuse on a tab-specific menu, the global Process cookies in redirections setting is ignored.

If you modify settings for a tab, the tab's settings icon turns blue. To return a tab to the global Repeater settings, click its settings icon next to the Send button and select Restore global default from the context menu.

If you use a project file, any tab-specific settings you configure for open tabs are retained when you re-open Burp Suite.
