# [MoBP] Intelligent MIME type recognition

Source: https://portswigger.net/blog/mobp-intelligent-mime-type-recognition
Fetched: 2026-06-28T09:15:20.289348+00:00

[MoBP] Intelligent MIME type recognition

Dafydd Stuttard |

Tuesday, 11 November 2008 at 07:03 UTC

MoBP

burp

The new version of Burp employs heuristic rules to recognize most types of content commonly used in web applications. Information about response MIME types is used in various ways, for example:

Display filters in various locations allow you to show or hide different MIME types.

The Spider uses MIME type information to perform tailored content parsing.

You can define Proxy interception rules based on MIME type.

Vulnerability analysis performs different checks and actions based on a response's MIME type.

Applications typically include a Content-type header in their responses, which announces the MIME type of the content in the response body. However, it is good not to trust this header, because it is often wrong. Look at the following very common example. The response's Content-type header states that it contains HTML. However, in the MIME type column of the proxy history, the content is correctly identified as JavaScript. If we trusted the MIME type stated by the application, we would handle the response incorrectly, potentially missing some interesting vulnerabilities.

MoBP

burp

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
