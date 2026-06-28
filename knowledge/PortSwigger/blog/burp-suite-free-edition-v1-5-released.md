# Burp Suite Free Edition v1.5 released

Source: https://portswigger.net/blog/burp-suite-free-edition-v1-5-released
Fetched: 2026-06-28T09:15:09.745392+00:00

Burp Suite Free Edition v1.5 released

Dafydd Stuttard |

Wednesday, 31 October 2012 at 14:21 UTC

Burp Suite Free Edition v1.5 is now available to download.

This is a significant upgrade with a wealth of new features added since v1.4. The most notable of these are described below.

User Interface

Burp's UI has been completely overhauled, to improve looks and usability:

Fonts are now scalable throughout the UI, with corresponding resizing of all UI elements (tables, dialogs, buttons, etc.).

There are configurable hotkeys for all common functions.

Intruder and Repeater now have smart tabs, which you can drag to reorder, and click to create, close or rename.

Tables are natively sortable everywhere, except where the row ordering is part of the options you are configuring.

Text fields now have context-aware auto-complete memory.

Burp Proxy

You can now add comments and highlighting to items as they appear in the Proxy intercept window. This is useful when manually stepping through an application, allowing you to annotate interesting requests as they are made, and then return to these in the Proxy history for further investigation.

You can now bind Proxy listeners to specific IP addresses, in addition to the loopback interface and all interfaces.

Burp now implements sslstrip-style functionality, allowing you to use non-SSL-capable tools against HTTPS applications, or to perform active MITM attacks against users who begin browsing using HTTP:

You can force the Proxy to use HTTPS in outgoing requests, even if the incoming request did not use HTTPS. This is configured per-listener, in the request redirection settings.

You can configure the Proxy to convert all HTTPS links in responses and redirects to use HTTP.

You can configure the Proxy to remove the secure flag on set cookies, so that browsers will still submit them over HTTP.

You can disable the Proxy web interface (at http://burp) and suppress Burp error messages in responses. These options can be useful to mask the presence of Burp from users who connect via it.

Burp Intruder

There is a new ECB Block Shuffler payload type. This is designed for testing ECB-encrypted tokens and other data, to check their vulnerability to block shuffling attacks.

Burp Intruder now has improved extract grep functionality, which lets you define each extract grep location simply by selecting into the base response, or, during a live attack, by selecting into any result response that contains interesting content (such as an error message).

JSON is now fully supported, with automatic placement of payload positions and syntax colorizing in the message viewer.

Burp Repeater

The context menu now has a Paste URL as request item. This configures Repeater to make a GET request using the URL on the clipboard. The headers included within this request are taken from the request headers defined in the Spider options.

The context menu now has an Add to site map item, to facilitate manual content mapping.

Networking / HTTP

Burp now supports streaming HTTP responses, and handles these in a way that lets you and the application continue working. Streaming responses are often used for functions like continuously updating price data in trading applications, where the server keeps the response stream open, pushing further data in real time as this becomes available. Because intercepting proxies use a store-and-forward model, they can break these applications - the proxy waits indefinitely for the streaming response to finish, and none of it is ever forwarded to the client. Burp now lets you specify which URLs return streaming responses. The Proxy tool will pass these responses straight through to the client as data is received. The Repeater tool will update the response panel in real time as data is received. Other Burp tools will ignore streaming responses and will close the connections.

There is a new option to drop all out-of-scope requests. Using this option prevents Burp from issuing any requests to out-of-scope URLs, even if they are requested via the Proxy, Repeater etc. You can use this option based on the defined suite-wide scope or on a custom scope.

Burp now handles Android SSL connections, implementing a workaround to accommodate the non-standard CONNECT requests issued by Android devices and the Android emulator.

Session handling

Various features have been added to the session handling support:

You can now define custom parameter locations within macro responses. In today's Ajax-heavy applications, items such as anti-CSRF tokens are often transmitted to the client within JavaScript or JSON structures; client-side code then processes the item and sends it within the relevant parameter in subsequent requests. You can now configure arbitrary named parameter locations within a macro response. For example, this allows you to specify that a particular JavaScript string contains a parameter with a specific name. When updating parameters in subsequent requests, Burp will update any parameter with that name using the value extracted from the configured location in the prior response

In the "Run macro" action, there is a new, default-off option to tolerate a mismatched URL when attempting to match parameters from the final macro response. This is useful for URL-agnostic anti-CSRF tokens, and enables you to configure a single macro to retrieve a valid token, which you can use in requests to multiple URLs, considerably simplifying the necessary Burp configuration in some applications.

In the "Run macro" action, there is a new, default-on option to URL-encode parameter values in the current request that have been derived from the final macro response.

The session handling cookie jar now tracks cookie expiration times.

Documentation

Burp now includes full help documentation within the software itself:

New help documentation is completely rewritten and up to date.

Comprehensive - 65,000 words.

Logically organized into 300 individual sections.

Includes every Burp function and configuration option.

Step-by-step "getting started" help for newbies.

Detailed help on using Burp in your testing methodology.

Advanced topics for Burp power users.

You can open the main help window via the Help menu. Contextual help is also provided throughout Burp. Next to any function or option, you can click the "?" button to view relevant help in a pop-up. And if necessary, you can drill down from there into the main help itself.

Download Burp Suite now.

Dafydd Stuttard

@DafyddStuttard

Latest Posts

Burp Extensibility 2026: Awards, Talks, and Highlights

19 June 2026

Burp Extensibility 2026: Awards, Talks, and Highlights

The beast needs a cage: What's next for AppSec post-Mythos

12 May 2026

The beast needs a cage: What's next for AppSec post-Mythos

3 ways custom scan checks turn practitioner knowledge into scalable automation

01 May 2026

3 ways custom scan checks turn practitioner knowledge into scalable automation

Senior pentesters have a deeply refined intuition about what is vulnerable in an environment. The problem? That expertise is often siloed with an individual and trapped in their notes or Python scripts.
