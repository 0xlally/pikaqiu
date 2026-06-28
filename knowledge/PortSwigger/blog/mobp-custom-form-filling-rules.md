# [MoBP] Custom form filling rules

Source: https://portswigger.net/blog/mobp-custom-form-filling-rules
Fetched: 2026-06-28T09:15:20.254411+00:00

[MoBP] Custom form filling rules

Dafydd Stuttard |

Wednesday, 12 November 2008 at 07:29 UTC

MoBP

burp

One cool feature that Burp Spider always had was the ability to submit HTML forms whilst spidering, either by prompting the user to supply suitable values, or by automatically filling in text fields with a default value.

This feature is now getting more flexible, with the ability to configure customised rules for filling in forms, by specifying the value that should be used based on the name of the individual form field:

Supplying valid input in forms is particularly important when spidering a web application, to increase the likelihood that the input is accepted by the application, enabling the spider to access the content that is reached by submitting the form. Burp comes with a set of default rules that have proven successful when automatically submitting form data to a wide range of applications. Of course, you can modify these or add your own rules if you encounter form field names that you want to submit specific values in.

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
