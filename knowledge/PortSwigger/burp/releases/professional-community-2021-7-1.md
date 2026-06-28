# Professional / Community 2021.7.1

Source: https://portswigger.net/burp/releases/professional-community-2021-7-1
Fetched: 2026-06-28T09:16:35.919121+00:00

This release includes improvements to DOM Invader, a Scanner speed increase, a change to the message inspector UI, and a bug fix.

DOM Invader improvements

DOM Invader has a new option to automatically add the canary to all sources. This saves you time and means that you can discover vulnerabilities by just browsing through a site. The option is off by default; you can turn it on from the DOM Invader settings.

You can now discover parameters that use the URLSearchParams API. Sites use this API to extract client-side parameters from URLs, and DOM Invader can now expose more attack surface when these parameters appear in a sink.

Scanner speed increase

Based on user feedback and our own analysis, we have changed Burp Scanner's default settings to speed up scans without compromising coverage.

Message inspector UI change

A message inspector UI change we made in 2021.7 was causing problems, so we reverted it. You can once again edit names and values in-line in the message inspector by double clicking a field. You can also select a single field with a single click, or multiple fields with a single click and drag.

Bug fix

We fixed a bug where the innerText setter was not being called correctly in DOM Invader.
