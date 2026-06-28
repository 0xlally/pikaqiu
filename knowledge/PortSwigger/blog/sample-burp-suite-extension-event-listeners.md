# Sample Burp Suite extension: event listeners

Source: https://portswigger.net/blog/sample-burp-suite-extension-event-listeners
Fetched: 2026-06-28T09:15:24.155420+00:00

Sample Burp Suite extension: event listeners

Dafydd Stuttard |

Thursday, 13 December 2012 at 12:17 UTC

burp extender

This extension demonstrates how to register listeners for various runtime events:

HTTP requests and responses for all Burp tools.

HTTP messages intercepted by the Proxy.

Addition of new scan issues.

The extension being unloaded by the user.

The sample extension simply prints a message to its output stream when an event occurs.

Registering an extension state listener is particularly important for any extension that starts background threads or opens system resources (such as files or database connections). The extension should listen for itself bring unloaded by the user, and should terminate any background threads or close any open resources when this event occurs. This good practice enables the user to fully unload the extension via the Burp UI.

Download the event listeners extension. The download includes source code for Java and Python, and the compiled JAR file for Java.

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
