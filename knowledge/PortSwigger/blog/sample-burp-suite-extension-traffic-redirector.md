# Sample Burp Suite extension: traffic redirector

Source: https://portswigger.net/blog/sample-burp-suite-extension-traffic-redirector
Fetched: 2026-06-28T09:15:24.498557+00:00

Sample Burp Suite extension: traffic redirector

Dafydd Stuttard |

Friday, 14 December 2012 at 14:31 UTC

burp extender

This extension demonstrates how to redirect outgoing HTTP requests from one host to another. This task might arise, for example, if you have mapped out an application which then moves to a different staging URL. By simply redirecting traffic to the new hostname, you can continue to drive your testing from the original site map.

The extension works as follows:

It registers itself as an HTTP listener.

For outgoing request messages, it retrieves the HTTP service for the request.

If the HTTP service host matches the "from" host, it uses a helper method to build a new HTTP service using the "to" host, and other details unchanged.

It updates the HTTP request with the new HTTP service.

Note: The sample code uses "host1.example.org" and "host2.example.org" as the "from" and "to" hostnames. You should edit the code to use your own hostnames before using it.

Download the traffic redirector extension. The download includes source code for Java and Python.

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
