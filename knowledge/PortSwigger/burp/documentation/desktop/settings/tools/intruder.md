# Intruder settings

Source: https://portswigger.net/burp/documentation/desktop/settings/tools/intruder
Fetched: 2026-06-28T09:15:56.438601+00:00

Support Center

Documentation

Desktop editions

Settings

Tools

Intruder

ProfessionalCommunity Edition

Intruder settings

Last updated:

June 18, 2026

Read time:

2 Minutes

The Intruder page in the Settings dialog contains settings for the following:

Default Intruder side panel layout.

Automatic payload placement.

New tab configuration.

Behavior when closing result windows.

Payload list location.

The Intruder settings are all user settings. They apply to all installations of Burp on your machine.

Note

To configure a Burp Intruder attack, you can modify the attack configuration settings in the Intruder tab. For more information, see

Burp Intruder attack settings.

Default Intruder side panel layout

These settings enable you to set the default layout of the Intruder side panel.

You can set the panel's default position as Left or Right.

You can set the panel's display mode:

Auto-expand - By default, the side panel expands and collapses with the available screen space.

Always collapsed - Enable this setting to keep the side panel collapsed.

Related pages

For information on how to set the default layout for the side panels in all tools except Burp Intruder, see

Side panel settings - Default side panel layout.

Automatic payload placement

These settings control how Burp Intruder places automatic payload markers. The available options are:

Replace base parameter value.

Append to base parameter value.

Related pages

Burp Intruder payload positions.

New tab configuration

This setting controls the attack configuration used when you open a new tab. The available options are:

Use default attack configuration.

Copy configuration from first tab.

Copy configuration from last tab.

Related pages

Managing Burp Intruder attack tabs.

Behavior when closing result windows

These settings control what happens to an attack when you close a results window.

You can select what happens when you close an attack that is in progress. The available options are:

Continue my attack in the background.

Delete my attack.

Ask me what to do each time.

You can also select what happens to your attack data if you select to close a finished attack. The available options are:

Save my attack to the project file.

Keep in memory.

Delete my attack.

Ask me what to do each time.

Related pages

Saving attacks.

Payload list location

These settings enable you to specify whether you use Burp's built-in payload lists or add your own custom payload lists:

Use built-in lists - Use Burp's built-in payload lists.

Load custom lists from directory - Click Select directory and select the folder with your custom lists.

To copy all of Burp's preconfigured payload lists into your custom directory, load a custom directory and select Copy.

Related pages

Predefined payload lists.
