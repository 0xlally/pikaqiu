# [MoBP] Spidering authenticated applications

Source: https://portswigger.net/blog/mobp-spidering-authenticated-applications
Fetched: 2026-06-28T09:15:21.060351+00:00

[MoBP] Spidering authenticated applications

Dafydd Stuttard |

Thursday, 13 November 2008 at 08:08 UTC

MoBP

burp

Related to yesterday's post is a further enhancement to the way the Spider handles form submission. In the new version, you can control how Burp handles login forms, separately from the configuration for forms in general. You can tell the Spider to perform one of four different actions when a login form is encountered:

You can ignore the login form, if you don't have credentials, or are concerned about spidering sensitive protected functionality.

You can prompt for guidance interactively, enabling you to specify credentials on a case-by-case basis.

You can treat login forms as any other form, using the configuration and auto-fill rules you have configured for those.

You can automatically submit specific credentials in every login form encountered.

In the last case, any time Burp encounters a form containing a password field, it will submit your configured password in that field, and will submit your configured username in the text input field whose name most looks like a username field. The UI for configuring application login looks like this:

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
