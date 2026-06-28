# [V13P] SSL pain relief

Source: https://portswigger.net/blog/v13p-ssl-pain-relief
Fetched: 2026-06-28T09:15:27.402750+00:00

[V13P] SSL pain relief

Dafydd Stuttard |

Sunday, 22 November 2009 at 10:02 UTC

V13P

In v1.2.11, Burp introduced a new method of generating the server SSL certificates which are presented to your browser when you connect via Burp Proxy. This involved creating a root CA certificate (per user), which you can install into your browser, and using this to sign each host certificate, thus enabling you to eliminate SSL certificate errors. Read more here.

Unfortunately, in v3.5 Firefox changed the way it handles root CA certificates, which stopped Burp's root CA certificate from working. This problem has now been fixed, and Firefox should accept Burp's certificates again:

Note that if you have previously installed Burp's CA certificate into any of your browsers, you may need to remove this before you can install the new root certificate, as described here.

Another occasional source of SSL pain happens when Burp fails to negotiate connections using the combination of protocols offered by the destination web server. The Java SSL stack contains a few gremlins, and fails to work with certain unusual server configurations. To help you troubleshoot this problem, Burp now lets you specify which protocols should be offered to servers during SSL negotiations:

Note that Burp already implements a few workarounds for SSL issues, and if a negotation fails with the protocols you have configured, Burp will still try some alternative combinations of protocols which often work. So you shouldn't use this new feature as a method of testing which protocols are actually supported by the server. People often ask if Burp can perform these checks, but Java is a bit too far removed from the SSL action for this to be done reliably, so you are better off sticking to a dedicated tool for investigating server SSL configurations.

V13P

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
