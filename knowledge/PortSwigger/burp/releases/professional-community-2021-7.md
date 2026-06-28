# Professional / Community 2021.7

Source: https://portswigger.net/burp/releases/professional-community-2021-7
Fetched: 2026-06-28T09:16:35.630329+00:00

This release adds DOM Invader, a powerful new tool for testing DOM XSS. It also provides improvements to Burp Scanner's navigation of single page applications, a new learning resource, and some minor improvements.

DOM Invader

DOM Invader is a powerful new tool to make testing DOM XSS much simpler. Implemented as an extension to Burp Suite's embedded browser, DOM Invader instruments your target's DOM. It intercepts JavaScript sources and sinks, and organizes them into a clear tree view for you to test.

DOM Invader works by putting a canary (a definable string) into sources and looking for the canary in sinks. It can automatically put canaries into URLs and form elements to speed up testing.

DOM Invader also lets you test for web message vulnerabilities by intercepting web messages and providing detailed information about them. You can then manipulate a web message or spoof its origin, manually or automatically.

Check out Gareth Heyes' blog post introducing this awesome tool, and read the full documentation here. DOM Invader is available in both Professional and Community Edition.

Improved Burp Scanner navigation of SPAs

We have improved the way that Burp Scanner navigates single page applications (SPAs). The embedded browser can now interact with more DOM elements that can cause JavaScript-triggered navigation, including anchor links and buttons.

This functionality also lays a foundation for auditing asynchronous traffic, which we will be adding soon (see the roadmap). This will allow Burp Scanner to target a bigger attack surface in SPAs.

Learn

We've made it easier to quickly learn more about Burp Suite. The Learn tab contains links to tutorials and other useful resources to help your Burp Suite journey. You'll find it on the main interface bar.

If you've already mastered Burp Suite, you can hide the new tab, if you prefer.

Minor improvements

This release contains the following small improvements:

You can now set a project option to stop Burp Suite's embedded browser using GPUs. This avoids an issue in some environments where GPUs are not available.

You can now edit names and values in-line with a single click in the message inspector table view without having to drill down. In the inspector drill down view non printable characters will be displayed in the same way as in the message editor.
