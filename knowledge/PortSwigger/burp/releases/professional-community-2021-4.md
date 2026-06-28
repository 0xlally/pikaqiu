# Professional / Community 2021.4

Source: https://portswigger.net/burp/releases/professional-community-2021-4
Fetched: 2026-06-28T09:16:34.896468+00:00

This release provides a native logging tool to Burp Suite. It also allows saving settings for Burp's embedded browser and message editor's search bar, and the ability to turn off Repeater's line ending normalization. The release also provides several bug fixes.

Logger

Burp Suite now has a native logging tool called Logger, which is available from the main row of tool tabs. Some highlights of Logger are:

You can view traffic made by all Burp tools, analyze messages, and send them to other Burp tools.

You can configure separate capture and view filters to focus on the messages that you are interested in.

Logger is optimised for performance and limits the amount of memory that is used. The default limit is 50MB (or 100MB if you give Burp Suite at least 1GB of memory), but you can change this. Once the memory limit has been reached, Logger will keep a rolling log of entries.

You can turn off Logger if you prefer.

Here is a short video showing Logger in action:

Embedded browser settings

When using Burp's embedded Chromium browser, your history and any changes you make to the browser settings are now saved even after you close Chromium. This means you no longer need to reconfigure your preferences each time you use the browser and can even keep any extensions that you install.

By default, your settings and history will be persisted. If you'd prefer to disable this behavior, go to User options > Misc and deselect the corresponding checkbox in the "Embedded browser" section.

Message editor search settings

You can now configure the default settings of the message editor's search bar. Change the defaults by going to User options > Misc and selecting the check boxes under "Message search".

Normalized line endings in Repeater

Repeater usually normalizes the line endings of requests. However, this behaviour may not always be useful, especially when you are testing request smuggling. You can now turn off normalizing line endings by going to the Repeater menu and unchecking "Normalize line endings".

Bug fixes

This release provides several minor improvements and bug fixes, including:

Message inspector buttons now work correctly when you paste content into a "Decoded from" panel.

Burp Collaborator server now responds to CAA queries with a NOERROR rather than a SERVFAIL response code.

Burp Collaborator server now supports custom CNAME and TXT records.

Burp Suite is not entirely compatible with Java 16. It will now warn you if you try to launch it with Java 16, and provide a workaround to enable you to use both together.
