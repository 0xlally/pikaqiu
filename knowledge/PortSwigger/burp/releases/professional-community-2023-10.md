# Professional / Community 2023.10

Source: https://portswigger.net/burp/releases/professional-community-2023-10
Fetched: 2026-06-28T09:16:39.944617+00:00

This release introduces the ability to unpack Brotli-compressed messages in the Proxy and Repeater tools, and adds Organizer functionality to the Montoya API.

In Burp Scanner, we have introduced some new features to help keep you better informed of the progress of your scans, and reduced the overall load time of pages.

We've also made some minor improvements and fixed a few bugs.

Brotli-compression now supported

We've added Brotli to our list of supported compression types. This means you can now unpack Brotli-compressed messages in the Proxy and Repeater tools.

Montoya API changes

You can now send requests and responses to Burp Organizer via the Montoya API.

Scanner improvements

We've made a number of improvements to Burp Scanner, including:

Overall load time breakdown

On the Crawl paths tab, we've added a hover-over that shows a breakdown of the overall load time of a page to show initial load time, time waiting for background requests, and time waiting for page to stabilize.

Scan progress indicators

We've added some new features to help keep you better informed of the progress of your scans:

The current crawl depth and the number of pending actions have been added to the First crawl path to location panel of the Crawl paths tab.

Pending URLs (links that the crawler has found but not yet sent a request to) have been added to the Tree view panel of the Site map tab.

Other Scanner improvements

We've made a number of additional improvements to the Scanner, including:

Reducing the time it takes to wait for a page to stabilize, which has decreased the overall load time of pages.

Improving the functionality of recorded login sequences.

Bug fixes

We've fixed some minor bugs, including:

A bug that caused some extensions to return an incorrect indexOf() value when using the Montoya or Wiener APIs.

A bug that caused hidden tabs to remain hidden when requests or responses were sent to them.

A bug in Burp's search that said there were 0 highlights in the request and response panels, even when results had been found.
