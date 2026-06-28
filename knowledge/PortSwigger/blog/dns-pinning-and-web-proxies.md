# DNS pinning and web proxies

Source: https://portswigger.net/blog/dns-pinning-and-web-proxies
Fetched: 2026-06-28T09:15:13.929017+00:00

DNS pinning and web proxies

Dafydd Stuttard |

Tuesday, 10 July 2007 at 13:10 UTC

xsrf

browser security

dns pinning

DNS-based attacks against browsers have been known about for years. These attacks have received increased attention recently, following the discovery of defects within browser-based DNS pinning defences.

So far, discussion has focused on browser issues. However, the same attacks can also be performed against web proxies. Browser-based DNS pinning does not apply when a web proxy is being used, because the DNS look-ups occur on the proxy, not the browser. Hence, even if DNS-based attacks are completely addressed within browsers, the problem is not going to go away altogether.

The most significant opportunities for DNS-based attacks are against web users on internal corporate networks, as a means of gaining unauthorised access to sensitive information and web applications on internal intranets. Given that a large proportion of these users access the Internet via a proxy server, attacks against web proxies may represent at least as significant a threat as those against browsers.

I've written a short paper which explains the problem, examines possible software-based solutions, and describes the defences that organisations and individuals can use to prevent attacks against them. In summary:

DNS-based attacks affect web proxies as well as browsers.

Today's proxies are vulnerable.

The problem is not straightforward to fix in software.

You can protect your own infrastructure against these attacks.

xsrf

browser security

dns pinning

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
