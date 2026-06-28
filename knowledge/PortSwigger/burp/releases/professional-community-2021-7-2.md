# Professional / Community 2021.7.2

Source: https://portswigger.net/burp/releases/professional-community-2021-7-2
Fetched: 2026-06-28T09:16:35.850955+00:00

This release contains DOM Invader improvements, an embedded browser update, and several bug fixes.

DOM Invader improvements

We have made the following improvements to DOM Invader:

DOM Invader can now find more vulnerable event listeners. Automated messages sent by DOM Invader now work with event listeners that have been implemented with JavaScript's strict mode.

You now have more control over DOM Invader's behavior when injecting a canary in all sources. A new option lets you exclude specific sources when automatically injecting. This means you can avoid damaging fragile sites by excluding problematic sources (e.g., location.pathname).

When you inject a canary into all sources, DOM Invader now appends a different random string to the canary for each source it is injected into. This makes it easier to see which source inputs are passed into a sink.

Chromium version update

We have updated Burp Suite's embedded browser to Chromium 92.0.4515.107, which fixes several security issues that Google has classified as high.

Bug fixes

This release fixes several minor bugs.
