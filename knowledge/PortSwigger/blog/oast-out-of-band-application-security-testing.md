# OAST (Out-of-band Application Security Testing)

Source: https://portswigger.net/blog/oast-out-of-band-application-security-testing
Fetched: 2026-06-28T09:15:22.448281+00:00

OAST (Out-of-band Application Security Testing)

Dafydd Stuttard |

Friday, 14 July 2017 at 16:45 UTC

OAST

Speaking to a couple of “thought leader” types this week, I realized that not everyone has fully appreciated the power and innovation of Out-of-band Application Security Testing (OAST).

At PortSwigger, we don’t go in for marketing hype, and prefer to release phenomenal features, describe them accurately, and let users make up their own minds. When we first released Burp Collaborator, the immediate positive feedback soon turned into a deluge of praise when our users saw just how powerful it was in uncovering real-world vulnerabilities.

The most skilled manual penetration testers have been using out-of-band testing techniques for many years, but this generally involved setting up some custom private infrastructure, and manually correlating any network interactions with the tester’s activities. Further, little research had been published on how to coax vulnerable applications into initiating out-of-band network interactions in different situations.

Burp Collaborator was revolutionary in three ways:

It made OAST available to the masses, just working out-of-the-box with zero configuration and no need for any private infrastructure.

The Burp Suite research team developed innovative techniques for reliably triggering out-of-band interactions in the presence of a wide range of vulnerabilities, including blind SQL injection, blind cross-site scripting, blind XXE, blind server-side XML/SOAP injection, blind OS command injection, and SMTP header injection.

With a bit of magic, Burp Collaborator correlates every out-of-band interaction with the exact request and payload that caused it, even if the interaction is deferred and happens days later due to an asynchronous vulnerability.

The landscape of application security testing is commonly divided into dynamic (DAST), static (SAST), and interactive (IAST) techniques. Marketing aside, the relative strengths and weaknesses of these approaches are well understood. But it appears that not everyone has taken on board the sheer power of out-of-band (OAST) techniques, and the strong advantages that OAST has over the other approaches. So we decided that maybe it is time to spell these out explicitly, so that everyone can think about them.

But first, what exactly is OAST?

OAST combines the delivery mechanism of conventional DAST with the detective power of IAST. It operates dynamically, sending payloads to a running application. These payloads pass through the application’s processing in the normal way. If a payload is ever handled in an unsafe manner, it effectively performs some in-place instrumentation to change the application’s behavior, causing it to make a network interaction (typically DNS) with an external system. The contents of that interaction allow the OAST tool to report the precise type of vulnerability and the input point that can be used to trigger it.

Here is an example of an OAST payload that, if it is ever used unsafely in a SQL query against an Oracle database, will cause a connection to the Burp Collaborator server:

'||(select extractvalue(xmltype('<?xml version="1.0" encoding="UTF-8"?>

<!DOCTYPE root [ <!ENTITY % ekiom SYSTEM

"http://pibw1f1nhjh3vpkgtx6mtfnt8kea2eq8dy1n.burpcollab'||'orator.net/">

%ekiom;]>'),'/l') from dual)||'

So how does OAST outperform the other approaches to application security testing?

DAST is unable to detect numerous vulnerabilities that are completely invisible in application responses, where successful payloads cause no difference in response content or timing. Nor can it detect vulnerabilities that are triggered asynchronously after scanning is completed. Conversely, OAST is able to find completely invisible and deferred vulnerabilities.

SAST is notoriously prone to generating noise through false positives. Although it can often find obscure vulnerabilities that are invisible to DAST, these are unfortunately lost in the haystack of findings that require manual investigation. Conversely, OAST has virtually zero false positives. If the payload above causes an interaction, then we injected into an Oracle SQL query.

IAST involves making invasive changes to the running application to inject instrumentation. This is liable to introduce defects, impair performance, and create new attack surface. It certainly shouldn’t be used in production systems. Conversely, OAST involves no modification to the system under test, because the instrumentation is self-contained within the payload, and is performed in-place only at the point where the payload reaches a vulnerability.

Additionally, like DAST, OAST has the benefit of being agnostic as to the language and platform used in the application under test. The OAST payload above works on any application that uses Oracle in the relevant way, and doesn’t care whether that application is written in Java, .NET, PHP, or anything else. Conversely, SAST and IAST are both closely bound to specific technologies, and the tools in question need to be largely rewritten and maintained for each language and platform that they target. From the perspective of the creator of testing tools, it is far more realistic to provide good technology coverage for DAST and OAST tools. There is an evident trend among tool vendors in the direction of OAST, with both Acunetix and Netsparker making moves in the same direction.

We hope this post helps to communicate the sheer power and innovation of OAST, and how it differs in nature and capability from other approaches to application testing.

OAST

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
