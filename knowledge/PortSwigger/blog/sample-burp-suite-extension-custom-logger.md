# Sample Burp Suite extension: custom logger

Source: https://portswigger.net/blog/sample-burp-suite-extension-custom-logger
Fetched: 2026-06-28T09:15:24.048327+00:00

Sample Burp Suite extension: custom logger

Dafydd Stuttard |

Friday, 14 December 2012 at 16:12 UTC

burp extender

This extension provides something that has often been requested: a suite-wide HTTP logger within the main Burp UI. It provides a great example of how you can add some really useful functionality to Burp with a very small amount of code or effort.

The extension uses the following techniques, which are made possible by the new extensibility API:

It creates a custom tab within the main Burp UI, in which to display the message log.

It creates two instances of Burp's own HTTP message editor, in which to display the selected request and response (as in the Proxy history).

It provides an implementation of IMessageEditorController, which the message editors can query to obtain additional details about the displayed messages (to support context menu actions, etc.).

It asks Burp to customize its own UI components, in line with Burp's UI style.

It adds an HTTP listener, to receive details of requests and responses made by all Burp tools.

It uses an extension helper method to analyze the URL in each request.

In approximately 200 lines of fairly simple code, this extension adds a useful new feature, with all of the fiddly work (handling and rendering of HTTP messages) being done by Burp itself via the API.

Download the custom logger extension. The download includes source code for Java and Python, and the compiled JAR file for Java.

[Disclaimer: My Python fu is weak. In fact, this series of Burp extensions is the only Python code I've ever written. This extension is a bit more complicated than the earlier ones. Apologies to any Python heads if my code makes you cringe.]

burp extender

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
