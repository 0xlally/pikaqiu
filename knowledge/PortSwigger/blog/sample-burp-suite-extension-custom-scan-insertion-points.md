# Sample Burp Suite extension: custom scan insertion points

Source: https://portswigger.net/blog/sample-burp-suite-extension-custom-scan-insertion-points
Fetched: 2026-06-28T09:15:24.259827+00:00

Sample Burp Suite extension: custom scan insertion points

Dafydd Stuttard |

Tuesday, 18 December 2012 at 15:20 UTC

burp extender

In the previous example, we saw how a simple Burp extension could be used to render and edit a custom message data format, within the Burp UI. For the purpose of demonstrating this capability, we used a trivial serialization format, in which user-supplied input is Base64-encoded within a request parameter value.

That example contained a rather obvious XSS vulnerability: the raw input contained within the serialized data is echoed unfiltered in the application's response. But although this type of bug might be obvious to a human, automated scanners will not (in general) identify any kinds of input-based vulnerabilities in cases where the raw input needs to be embedded within an unsupported serialization format. Since the scanner does not understand the format, it has no means of submitting its usual scan payloads in the way that is needed for the application to unpack and process the payloads and trigger any bugs. This means that in this situation, equipped only with the previous example of a custom editor tab extension, you would be restricted to manual testing for input-based bugs, which is a tedious and time-consuming process.

The new extensibility API lets you tackle this problem by registering your extension as a provider of custom scanner insertion points. For each actively scanned request, Burp will call out to your extension, and ask it to provide any custom insertion points that are applicable to the request. Each insertion point that you provide is responsible for the job of constructing validly-formed requests for specific scan payloads. This lets your extension work with any data format, and embed the scanner's payloads within the request in the correct way.

Here, we can see Burp reporting the XSS vulnerability, which it has found via the custom "Base64-wrapped input" insertion point:

Here is the request that Burp made, and which was generated for Burp by our custom insertion point:

Here, via our custom message editor tab, is the literal scan payload that is embedded in the request:

So, with a few lines of extension code, we have taught Burp Scanner how to work with the unsupported serialization format. All of Burp's built-in scan checks can now place their payloads correctly into the application's requests, and bugs like this can be quickly found.

Download the custom scan insertion points extension. The download includes source code for Java and Python, and the compiled JAR file for Java. It also includes an ASP.NET page that implements the serialization format on the client and server side, so that you can send serialized data from your browser, send the request for active scanning within Burp, and find the vulnerability. Note: the sample ASP.NET page uses the JavaScript btoa() function to perform Base64-encoding on the client side. This function is not supported by Internet Explorer, but works on most other browsers.

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
