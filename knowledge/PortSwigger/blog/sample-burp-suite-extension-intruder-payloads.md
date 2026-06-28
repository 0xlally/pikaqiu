# Sample Burp Suite extension: Intruder payloads

Source: https://portswigger.net/blog/sample-burp-suite-extension-intruder-payloads
Fetched: 2026-06-28T09:15:24.403649+00:00

Sample Burp Suite extension: Intruder payloads

Dafydd Stuttard |

Friday, 21 December 2012 at 15:29 UTC

burp extender

This example shows how you can use an extension to:

Generate custom Intruder payloads

Apply custom processing to Intruder payloads (including built-in ones)

When an extension registers itself as an Intruder payload provider, this will be available within the Intruder UI for the user to select as the payload source for an attack. When an extension registers itself as a payload processor, the user can create a payload processing rule and select the extension's processor as the rule's action.

When Burp calls out to a payload provider to generate a payload, it passes the base value of the payload position as a parameter. This allows you to create attacks in which a whole block of serialized data is marked as the payload position, and your extension places payloads into suitable locations within that data, and re-serializes the data to create a valid request. Hence, you can use Intruder's powerful attack engine to automatically manipulate input deep within complex data structures.

This example is artificially simple, and generates two payloads: one to identify basic XSS, and one to trigger the ficititious vulnerability that was used in the previous custom scanner check example. It then uses a custom payload processor to reconstruct the serialized data structure around the custom payload.

Download the Intruder payloads extension. The download includes source code and the compiled JAR file for Java. It also includes an ASP.NET page that extends the serialization example to add some fictitious bugs so that you can test the custom payloads, and see that the two vulnerabilities are triggered. After loading the extension, you'll need to select the custom payloads as your Intruder payloads type, and add a payload processing rule that invokes the extension-provided processor. Note: the sample ASP.NET page uses the JavaScript btoa() function to perform Base64-encoding on the client side. This function is not supported by Internet Explorer, but works on most other browsers.

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
