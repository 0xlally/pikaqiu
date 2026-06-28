# Professional / Community 2026.4

Source: https://portswigger.net/burp/releases/professional-community-2026-4
Fetched: 2026-06-28T09:16:56.804548+00:00

This release introduces a combined installer for Burp Suite Professional and Community Edition, greater extension control over HTTP traffic, Markdown support in Notes, and collection-level notes in Organizer, plus other improvements and some bug fixes.

Combined installer

We've introduced a combined installer file for Burp Suite Professional and Community Edition, making it easier to get started. Your setup, configuration, and licensing continue to work as before, so you can upgrade and carry on without interruption.

As a hardening measure, we've removed the Java binary. If this affects your workflow, please contact us at support@portswigger.net.

Extended extension control over HTTP traffic

Extensions can now stop requests from being sent or handle them entirely within Burp by returning custom responses.

Previously, extensions could only modify traffic before it was sent or after the response was receieved. This removes the need for common workarounds and gives extensions full control over HTTP traffic.

Markdown support in Notes

You can now format notes using Markdown, making it easier to structure longer write-ups with headings, lists, links, and inline formatting.

Collection-level notes in Organizer

You can now add notes to collections using the new About tab, providing a dedicated space to capture context, goals, or summaries for each collection.

Quality of life improvements

We've made the following quality of life improvements:

You can now add a description to upstream proxy rules in Settings > Network > Connections. This helps you identify rules more easily, especially when working with multiple upstream proxies.

You can now clear Burp's DNS cache from Settings > Network > DNS. Click Clear DNS cache to remove cached entries.

You can now use Send to in Comparer to send selected content to other tools.

Requests sent to Organizer now include response timing data, making it easier to identify delays and test for time-based behaviour.

You can now send multiple selected items from the site map to Repeater and Organizer.

Bug fixes

We've fixed the following bugs:

Intruder now applies payload processing rules correctly across all payload types when using Copy config from last tab.

Messages now keep their applied highlights when sent between Burp tools.

The Console panel in the Custom Actions test dialog now holds its size and position when running tests, so you don't need to resize it each time.

Burp now correctly recognizes SSE responses even when the Content-Type header doesn't include a space after the semicolon.

You can now poll private Collaborator servers when using certificates with a blank subject.
