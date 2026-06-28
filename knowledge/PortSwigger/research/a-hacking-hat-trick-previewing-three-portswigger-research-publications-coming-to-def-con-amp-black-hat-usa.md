# A hacking hat-trick: previewing three PortSwigger Research publications coming to DEF CON & Black Hat USA

Source: https://portswigger.net/research/a-hacking-hat-trick-previewing-three-portswigger-research-publications-coming-to-def-con-amp-black-hat-usa
Fetched: 2026-06-28T09:17:19.922585+00:00

A hacking hat-trick: previewing three PortSwigger Research publications coming to DEF CON & Black Hat USA

James Kettle

Director of Research

@albinowax

Published: Tuesday, 2 July 2024 at 12:57 UTC

Updated: Wednesday, 3 September 2025 at 07:38 UTC

We're delighted to announce three major research releases from PortSwigger Research will be published at both Black Hat USA and DEF CON 32. In this post, we'll offer a quick teaser of each talk, info on accompanying tools and labs, and suggested pre-reading to get the most out of them.

If you won't be there, we've still got you covered - every talk will be accompanied by a whitepaper published to /research within a few days of release, and talk recordings from DEF CON typically land on YouTube in September. Follow us on X, LinkedIn, RSS, or r/websecurityresearch to get notified as soon as they're available.

Listen to the whispers: web timing attacks that actually work

Author: James Kettle

Black Hat: 7th August, 10:20

DEF CON: 9th August, 11:30

Websites are riddled with timing oracles eager to divulge their innermost secrets. It's time we started listening to them.

In this session, I'll unleash novel attack concepts to coax out server secrets, including masked misconfigurations, blind data-structure injection, hidden routes to forbidden areas, and a vast expanse of invisible attack-surface.

This is not a theoretical threat; every technique will be illustrated with multiple real-world case studies on diverse targets. Unprecedented advances have made these attacks both accurate and efficient; in the space of ten seconds, you can now reliably detect a sub-millisecond differential with no prior configuration or 'lab conditions' required. In other words, I'm going to share timing attacks you can actually use.

To help, I'll equip you with a suite of battle-tested open-source tools enabling both hands-free automated exploitation, and custom attack scripting. I'll also share a little CTF to help you hone your new skillset.

Want to take things further? I'll help you transform your own attack ideas from theory to reality, by sharing a methodology refined through testing countless concepts on thousands of websites. We've neglected this omnipresent and incredibly powerful side-channel for too long.

Suggested pre-reading:

Timeless timing attacks

Smashing the state machine

Splitting the email atom: exploiting parsers to bypass access controls

Author: Gareth Heyes

Black Hat: 7th August, 13:30

DEF CON: 11th August, 10:00

Websites often parse users' email addresses to identify their organisation. Unfortunately, parsing emails is far from straightforward thanks to a collection of ancient RFCs that everyone knows are crazy. You can probably see where this is going...

In this session, I'll introduce techniques for crafting RFC-compliant email addresses that bypass virtually all defences leading to broken assumptions, parser discrepancies and emails being routed to wildly unexpected destinations. I'll show you how to exploit multiple applications and libraries to spoof email domains, access internal systems protected by 'Zero Trust', and bypass employee-only registration barriers.

Then I'll introduce another class of attack - harmless-looking input transformed into malicious payloads by unwitting libraries, leading to yet more misrouted emails, and blind CSS injection on a well-known target.

I'll leave you with a full methodology and toolkit to identify and exploit your own targets, plus a CTF to develop your new skillset.

Suggested pre-reading:

Beyond the @ symbol

Email domain-validation bypass

Blind CSS exfiltration

Gotta cache em all: bending the rules of web cache exploitation

Author: Martin Doyhenard

Black Hat: 8th August. 10:20

DEF CON: 10th August, 10:30

In recent years, web cache attacks have become a popular way to steal sensitive data, deface websites, and deliver exploits. We've also seen parser inconsistencies causing critical vulnerabilities like SSRF and HTTP Request Smuggling. This raises the question: what happens if we target web caches' URL-parsers?

In this session, I'll introduce two powerful new techniques that exploit RFC ambiguities to bypass the limitations of web cache deception and poisoning attacks and inflict some serious damage.

First, I'll introduce Static Path Deception, a novel technique to completely compromise the confidentiality of an application. I'll illustrate this with a case study showing how such a breach can be replicated in environments like Nginx behind Cloudflare and Apache behind CloudFront, using just their default configurations.

Next, I'll present Cache Key Confusion, and show how to exploit URL parsing inconsistencies in major platforms, including Microsoft Azure Cloud. I'll then show how to achieve arbitrary cache poisoning and full denial of service in OpenAI and countless platforms.

Finally, I'll reveal how to supercharge these vulnerabilities with a live demo that blends Cache Key Confusion with a "non-exploitable" open redirect. By modifying the response of a static javascript file, I'll show how to execute arbitrary JS code cross-domain.

Attendees will depart armed with a set of innovative techniques for uncovering concealed bugs, along with a definitive methodology to find and exploit these and other URL or HTTP discrepancies. To facilitate this, I'll provide an open-source tool to detect all discussed vulnerabilities, plus a lab to level-up your cache exploitation skills!

Suggested pre-reading:

Web cache poisoning

Web cache deception

Cached and confused

Will there be accompanying labs and Academy topics?

Yes!

Listen to the whispers will be accompanied by a hosted CTF.

Splitting the email atom will come with a Web Security Academy lab.

Gotta cache em all will come with an entire Web Security Academy topic on Web Cache Deception!

From Interest to Insight: How to Identify and Explore Your Research Topic

Presenters: James Kettle, Natalie Silvanovich, Stefano Zanero

Black Hat: 8th August. 11:20

Have you always wanted to share your security knowledge at conferences like Black Hat, but aren't sure where to begin? Creating a compelling submission starts with the content itself. This panel explores how to select targets for research, based on your own expertise and interests. Learn how to turn an idea into a conference-worthy talk!

Chat research with the team

If you'd like to meet the team and chat research, we'll also be holding a meet & greet in the newly formed Bug Bounty Village at DEF CON:

Meet the minds behind a decade of acclaimed web security research. Whether you'd like to query our thoughts on technical matters or career decisions, share something cool you've found, flood us with Burp Suite feature requests, or simply say hi, this is your chance! We're also giving three presentations at DEF CON so if you'd like to treat this as an extended Q&A for those, that's cool too. Please note this session may be chaotic.

Also if you see us around, do say hi - we have some extremely exclusive swag to give out.

Finally, there's one more exciting thing coming that we aren't quite ready to announce yet.

We'd better get back to our slides now. Hope to see you there!

DEF CON

Back to all articles

Related Research

06 August 2025
