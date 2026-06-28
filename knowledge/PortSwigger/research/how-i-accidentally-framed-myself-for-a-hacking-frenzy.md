# How I accidentally framed myself for a hacking frenzy

Source: https://portswigger.net/research/how-i-accidentally-framed-myself-for-a-hacking-frenzy
Fetched: 2026-06-28T09:17:25.642882+00:00

How I accidentally framed myself for a hacking frenzy

James Kettle

Director of Research

@albinowax

Published: Monday, 21 August 2017 at 13:49 UTC

Updated: Monday, 23 April 2018 at 15:25 UTC

It’s well known that some websites are vulnerable to IP address spoofing because they trust a user-supplied HTTP header like X-Forwarded-For to accurately specify the visitor’s IP address. However, until recently there was no widely known reliable way of identifying this vulnerability. During my recent Cracking the Lens research, I noticed that it was possible to identify this vulnerability by spoofing a domain name instead of a raw IP address, and observing whether the server attempts to resolve this domain to an IP address.

Burp Suite already ships with a server designed to record DNS lookups called Burp Collaborator, so to help the community hunt down this vulnerability I released Collaborator Everywhere, an open source extension that automatically applies this technique to all outbound traffic. For example, a simple request to http://example.com/ would be rewritten as:

GET / HTTP/1.1

Host: example.com

X-Forwarded-For: uniq-id.burpcollaborator.net

True-Client-IP: uniq-id.burpcollaborator.net

X-Real-IP: uniq-id.burpcollaborator.net

Given the title of this blog post, you may have already spotted my mistake. Shortly after releasing this tool, we received an email titled “Your Amazon EC2 Abuse Report” claiming that burpcollaborator.net was attempting to hack someone’s website by bruteforcing a password.

This claim was clearly false as Burp Collaborator never initiates connections to external servers, but on further thought it made perfect sense. Someone had used Burp Suite to bruteforce a password on a website, which is a completely valid use case. The problem was, the user had Collaborator Everywhere installed, and the server was vulnerable to IP spoofing so it misattributed the attack to id.burpcollaborator.net which resolves to our server at 52.16.21.24. The user may have been authorised to conduct that attack, but 52.16.21.24 certainly wasn’t and as such an abuse report was generated.

Burp Suite is an offensive security tool, so by releasing Collaborator Everywhere I’d effectively framed burpcollaborator.net for hundreds of simultaneous attacks across thousands of websites. Even worse, some of those websites would be hosted on private internal networks, so an apparent attack on them from burpcollaborator.net would make it look like we’d hacked our way into their infrastructure and were now trying to pivot.

To resolve this issue I’ve made Collaborator Everywhere use a special keyword subdomain - spoofed.uniq-id.burpcollaborator.net. This domain always resolves to 127.0.0.1 to ensure that abuse reports don’t get sent to us or innocent bystanders, and also provides a visual indication that it can’t be trusted. Due to the potential of this issue to harm burpcollaborator.net, we’ve revoked the old Collaborator Everywhere extension. This means that if you’re a Collaborator Everywhere user, you’ll need to restart Burp and install the fixed version via the BApp store.

This design flaw is obvious in hindsight, but serves as a personal lesson; when research is successful it’s all too easy to let enthusiasm eclipse potential hazards and side effects.

Back to all articles

Related Research

05 February 2026

06 January 2026

The Fragile Lock:

Novel Bypasses For SAML Authentication

10 December 2025

The Fragile Lock:

Novel Bypasses For SAML Authentication

Introducing HTTP Anomaly Rank

11 November 2025

Introducing HTTP Anomaly Rank
