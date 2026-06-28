# Professional / Community 2025.7

Source: https://portswigger.net/burp/releases/professional-community-2025-7
Fetched: 2026-06-28T09:16:55.299099+00:00

This release introduces improved tab group management in Repeater, improved form handling, and a number of quality of life improvements.

Improved Repeater tab group management

You can now choose from a wider range of colors when organizing Repeater tab groups. This gives you more flexibility to visually separate your work.

In addition, when you create a new group, it's now given the next available color. This helps you keep your workspace organized and easy to navigate.

Improved form handling

We've improved how forms are detected and displayed in Burp, helping you identify more attack surface:

By default, Burp's live passive crawl now processes forms in HTML and adds them to the site map.

When Burp adds a form to the site map, it now generates a request which is representative of what the form would send if submitted. This makes it easier to understand what the form includes at a glance.

API update for writing extensions and Bambda scripts

You can now access Organizer contents using the OrganizerItem interface in the Montoya API. This makes it easier to automate workflows and programmatically extract Organizer data.

Quality of life improvements

We've made the following quality of life improvements:

We've replaced the term "Bambda" with "script" in some locations across Burp to make our language clearer and more intuitive. To learn more about the different types of scripts you can use in Burp, see our Bambdas documentation.

When creating a request from scratch, Burp now includes all headers typically sent by Chrome. This helps reduce issues with bot-detection systems and improves compatibility with modern websites.

We've added a setting for Linux and Windows users that enables you to choose whether to merge Burp's menu bar with the system title bar. This may help Burp fit better with your system's styling. Find the setting under Settings > Display > Title bar appearance.

We've updated the layout of the Proxy > Intercept empty state, so all buttons remain visible and accessible on smaller screens.

Burp now supports streaming responses over HTTP/2

.

Bug fixes

We've fixed the following bugs:

We've fixed a bug that caused project files to become corrupted when sending certain streaming responses to Organizer.

We've fixed a bug where Repeater didn't automatically highlight the next WebSocket message in the History panel when Select next message received was selected.

We've fixed a bug where, when loading Match and Replace scripts from the Bambda library with Response Bambda selected, request scripts were incorrectly listed.

Java update

We've updated Burp's Java version to Java 24

. This improves compatibility for users running Burp on Linux VMs on M4 Macs.

Browser upgrade

We've upgraded Burp's browser to Chromium 138.0.7204.100/.101 for Windows & Mac, and 138.0.7204.100 for Linux. For more information, see the Chromium release notes.
