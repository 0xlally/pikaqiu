# All your header are belong to us

Source: https://portswigger.net/blog/all-your-header-are-belong-to-us
Fetched: 2026-06-28T09:15:06.778735+00:00

All your header are belong to us

Dafydd Stuttard |

Friday, 13 July 2007 at 07:52 UTC

XSS

First there came XMLHttpRequest, and then came Flash. This week, Alex released some great research demonstrating a new technique for spoofing browser HTTP headers.

The original problem with Flash was that it could be used to spoof any HTTP header within the browser of a user who invoked the Flash object. The fix that was applied to Flash did not make the problem go away altogether. It prevented Flash being used to spoof certain built-in browser headers, such as Referer and User-Agent. However, if a vulnerable page echoes the contents of all the headers that it received (as often happens in diagnostic error messages), then Flash is still a viable delivery mechanism for a reflected XSS attack.

What Alex has noticed is that many programming languages use underscores instead of hyphens when naming a header whose value they wish to access. For example, in PHP the following will retrieve the value of the User-Agent header:

$_SERVER['HTTP_USER_AGENT']

Predictably enough, a Flash object can be used to spoof a header containing the non-standard name:

req.addRequestHeader("User_Agent", "<script>alert('xss')</script>");

This is not blocked by the fix to the original problem, and yet in many languages (most notably PHP, Perl, Ruby and ColdFusion) the application will process the attacker's payload instead of the browser's built-in header. Very nice.

Alex also discusses some other attacks, which are well worth a read.

There is an important lesson in all of this, beyond the detail of the actual attack. The subject of request header spoofing arises in all kinds of situations, including XSS, XSRF and DNS pinning. Some people do not realise there is a problem at all, and many others think it has gone away through fixes to Flash and other client-side technologies. Even if the new hole is ultimately plugged, I'd bet that another one will be found soon enough. But regardless of that, we should in general make the working assumption that a malicious web site can spoof any request header of a user who accesses that site. If your application contains XSS when echoing request headers, then fix the bug. If your application trusts request headers when defending against other attacks, then find a more robust defence, before someone else finds a way to bypass it.

XSS

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
