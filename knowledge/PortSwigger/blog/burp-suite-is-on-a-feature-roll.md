# Burp Suite is on a feature roll!

Source: https://portswigger.net/blog/burp-suite-is-on-a-feature-roll
Fetched: 2026-06-28T09:15:09.872112+00:00

Burp Suite is on a feature roll!

Dafydd Stuttard |

Tuesday, 12 March 2013 at 14:23 UTC

Over the past month, we've added a wealth of new features to Burp Suite Professional. The most notable of these additions are:

A new cross-site request forgery (CSRF) technique using cross-domain XmlHttpRequest, to enable CSRF file upload, and other attacks.

DNS tunnelling over a SOCKS proxy (to access TOR hidden services, etc.).

Support for automatic decompression of compressed request bodies.

Support for .NET DeflateStream compression.

Summary of parameter values in Target Analzyer.

Ability to load scope configuration items from a text file.

Ability to import and export Burp Proxy's CA certificate.

Fine-grained options for configuring SSL protocols and ciphers.

Auto-selection of compatible SSL parameters on negotiation failure.

Optional re-enabling of SSL algorithms blocked by Java 7 security policy.

Per-host SSL certificates in invisible proxy mode, via the server_name extension in the Client Hello message.

Workaround to prevent OS X from deleting Burp's temporary files when Burp is left running for long periods.

Fast-reload of extensions (via ctrl+click) to facilitate development.

Several new Burp Extender APIs.

Command-line license activation for use in headless mode.

Numerous important bugfixes.

All of these changes were directly requested by Burp users, via the user forum, email, or Twitter. Now, we need more meat for the feature request sausage machine, so we encourage everyone who uses Burp to send us your own wish list.

Our queue of items for development uses a highly complex algorithm based on a fusion of FIFO, LIFO and can-we-be-arsed technologies. If you've asked for something before and it hasn't appeared yet, please ask us again. Even if you think something is too trivial or too complex, ask us anyway. The more people who request something, the more likely it will be to happen.

Burp is only as awesome as it is today because of feedback from our users. Thanks to everyone for your help!

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
