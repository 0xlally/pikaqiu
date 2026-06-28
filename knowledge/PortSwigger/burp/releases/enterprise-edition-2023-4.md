# Enterprise Edition 2023.4

Source: https://portswigger.net/burp/releases/enterprise-edition-2023-4
Fetched: 2026-06-28T09:16:19.083715+00:00

This release gives you more control over your site scope, so you can refine the URLs that you want to enable Burp Scanner to visit. We've also made some other improvements and fixed some bugs.

Improvements to site scope and start URLs

It's now much easier to define your site scope, so that Burp Scanner only scans the URLs you want it to. You can now see how we derive the site scope from your start URLs, and we've added the ability to define additional in-scope URL prefixes, and out-of-scope prefixes.

SPA scanning improvements

This release includes changes that improves Burp Scanner’s form submission handling, to support future single-page application (SPA) developments.

Other improvements

We've improved the user interface for managing application logins for your sites. Under the Scan settings menu, we now have separate menus for:

Usernames and passwords

Recorded login sequences

Bug fixes

This release fixes a number of bugs:

If you use a Kubernetes deployment, you'll no longer need to upload your license key after you install Burp Suite Enterprise Edition updates.

If you configure Burp Suite Enterprise Edition to automatically delete old scans, we no longer leave some items behind.

When you enable HSTS, we make sure that the header is added to all resources.
