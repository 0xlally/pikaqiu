# Professional / Community 2021.4.2

Source: https://portswigger.net/burp/releases/professional-community-2021-4-2
Fetched: 2026-06-28T09:16:35.131126+00:00

This release provides a native logging tool to Burp Suite, which allows for logging global and individual task traffic. It also strengthens support for HTTP/2, allows saving settings for Burp's embedded browser and message editor's search bar, and allows you to turn off Repeater's line ending normalization. The release provides some minor improvements, an update to Burp Suite's embedded browser, and fixes several bugs.

Logger

Burp Suite now has a native logging tool called Logger, which is available from the main row of tool tabs. Some highlights of Logger are:

You can view traffic made by all Burp tools, analyze messages, and send them to other Burp tools.

You can configure separate capture and view filters to focus on the messages that you are interested in.

Logger is optimised for performance and limits the amount of memory that is used. The default limit is 50MB (or 100MB if you give Burp Suite at least 1GB of memory), but you can change this. Once the memory limit has been reached, Logger will keep a rolling log of entries.

You can turn off Logger if you prefer.

Here is a short video showing Logger in action:

Task logger

You can also view log traffic for individual tasks (such as scans). This allows you to analyze what's happening if one of your tasks shows unexpected behavior, or to monitor a task's progress.

To see the log for a task, click on the task's "View details" icon and then select the "Logger" tab. Logging for each task has its own memory limit, separate from the main Logger.

HTTP/2 support

We have strengthened support for HTTP/2 within Burp Suite. HTTP/2 support is now turned on by default and is no longer considered experimental. Burp will interact with targets via HTTP/2 when a target supports it.

HTTP/2 support brings a significant performance improvement to the network layer, benefiting Scanner and Intruder speed. It also provides future compatibility with any site that no longer supports HTTP/1.1.

If you prefer not to use HTTP/2, you can disable its use under Project Options / HTTP.

Message editor search settings

You can now configure the default settings of the message editor's search bar. Change the defaults by going to User options > Misc and selecting the check boxes under "Message search".

Normalized line endings in Repeater

Repeater usually normalizes the line endings of requests. However, this behaviour may not always be useful, especially when you are testing request smuggling. You can now turn off normalizing line endings by going to the Repeater menu and unchecking "Normalize line endings".

Improved DNS records in Burp Collaborator

We have added support for single custom CNAME and multiple custom TXT DNS records within Burp Collaborator, which can optionally contain specific TTL values. You can read more here.

Embedded browser settings

When using Burp's embedded Chromium browser, your history and any changes you make to the browser settings are now saved even after you close Chromium. This means you no longer need to reconfigure your preferences each time you use the browser and can even keep any extensions that you install.

By default, your settings and history will be persisted. If you'd prefer to disable this behavior, go to User options > Misc and deselect the corresponding checkbox in the "Embedded browser" section.

Embedded browser update

This release includes an update of Burp Suite's embedded browser to Chromium 90.0.4430.85, which fixes several security issues that Google have classified as high.

Minor improvements

This release provides several minor improvements, including:

We have improved the heuristics of the crawler to better fill out text fields in forms.

Custom menu items added by extensions are now shown in a sub-menu of the context menu, to avoid cluttering.

The hash algorithm list within Burp Decoder is now sorted alphanumerically.

The resource pool button is now disabled when configuring a live passive crawl, as this crawl does not make requests.

We have added "Clear all payload markers", for Intruder, to the list of actions that you can assign a hotkey to.

Bug fixes

This release provides several bug fixes, including:

Filter dialogs now work correctly when you use the settings button to restore defaults or load a configuration.

The crawler now correctly clears session data held in local storage when it is no longer needed.

The crawler no longer produces an error when it encounters request bodies that contain JSON literals when it is crawling OpenAPI definitions.

Burp Suite now shuts down correctly on macOS.

The number of characters selected now shows in the message inspector when selecting non-editable messages.

The automatic backup progress dialog box no longer appears if Burp Suite is minimized.

Message inspector buttons now work correctly when you paste content into a "Decoded from" panel.

Burp Collaborator server now responds to CAA queries with a NOERROR rather than a SERVFAIL response code.

Burp Suite is not entirely compatible with Java 16. It will now warn you if you try to launch it with Java 16, and provide a workaround to enable you to use both together.

Requests to restore Proxy default settings no longer fail to restore Proxy filter configuration defaults.

When you load an existing project, the Proxy filter settings now are correctly honored.

You can now cancel Proxy filters.

The message inspector no longer sends spurious HTTP messages.
