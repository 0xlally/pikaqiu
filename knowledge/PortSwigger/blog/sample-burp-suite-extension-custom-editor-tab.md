# Sample Burp Suite extension: custom editor tab

Source: https://portswigger.net/blog/sample-burp-suite-extension-custom-editor-tab
Fetched: 2026-06-28T09:15:24.943597+00:00

Sample Burp Suite extension: custom editor tab

Dafydd Stuttard |

Monday, 17 December 2012 at 14:25 UTC

burp extender

This extension demonstrates how you can extend Burp's own HTTP message editor to handle the display and editing of unsupported data formats. This capability can let you handle custom serialization implemented by specific applications, or any other data format that Burp does not natively support.

In the past, some extensions have handled unsupported serialization formats by hooking into Burp's HTTP stack, and modifying incoming and outgoing messages, in order to unpack and repack the serialized data. Although this approach can work, it is quite restricted in the type of data it can handle. And it is also inelegant: it would be preferable to customize Burp to understand the custom format itself, rather than tampering with the integrity of HTTP messages.

The new extensibility API lets you add custom tabs to Burp's HTTP message editor. When a message is about to be displayed, Burp will ask the tab whether it can handle the message. If so, the custom tab will be shown in the editor, and can support rendering and editing of the message within its own UI:

The sample extension uses an artificially simple serialization format: the serialized data is simply Base64-encoded within a request parameter. This example was chosen so as to keep the code that handles the serialization as simple as possible. But the format itself isn't the point: what matters is that you can now easily extend Burp to understand any format that you may encounter in a test.

As well as the new API for adding message editor tabs, this example also makes use of Burp's new helper methods, to carry out common tasks such as parsing and updating request parameters, encoding and decoding data in different formats, and conversion of data between String and byte forms.

Download the custom editor tab extension. The download includes source code for Java and Python, and the compiled JAR file for Java. It also includes an ASP.NET page that implements the serialization format on the client and server side, so that you can send serialized data from your browser, edit this on the fly within Burp, and see the effect in the server's response. Note: the sample ASP.NET page uses the JavaScript btoa() function to perform Base64-encoding on the client side. This function is not supported by Internet Explorer, but works on most other browsers.

[Really astute testers might spot a deliberate vulnerability in the sample ASP.NET page. More on that soon.]

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
