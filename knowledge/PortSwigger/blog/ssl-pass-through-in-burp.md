# SSL pass through in Burp

Source: https://portswigger.net/blog/ssl-pass-through-in-burp
Fetched: 2026-06-28T09:15:24.612315+00:00

SSL pass through in Burp

Dafydd Stuttard |

Monday, 9 September 2013 at 16:15 UTC

SSL

burp

The latest version of Burp has a new feature: SSL pass through. You can use this feature to specify destination web servers for which Burp Proxy will directly pass through SSL connections:

This feature can be useful in cases where it is not straightforward to eliminate SSL errors on the client - for example, in mobile applications that perform SSL certificate pinning. Of course, if you pass through SSL connections, then Burp will not break the SSL tunnel, and no details about requests or responses made via these connections will be available in the Proxy intercept view or history. Nonetheless, using SSL pass through can sometimes enable you to perform some limited testing. If the application uses multiple domains, or uses a mix of HTTP and HTTPS connections, then passing through SSL connections to specific problematic servers still enables you to work on other traffic using Burp in the normal way.

As an example, suppose you encounter a domain where you are not able to get your client device to negotiate SSL correctly. This should be obvious enough in the client, and Burp will also alert you:

To work around this problem, you can add the problematic server to Burp's SSL pass through list:

Requests to this server will now pass straight through Burp, and your client can connect in the normal way.

The option to automatically add entries to the SSL pass through list on client SSL negotiation failure can be useful if you aren't sure exactly which domains the application is using, and don't want to have to manually populate the list. If you enable this option, then if your client fails to negotiate SSL connections with any other servers, these will be automatically added to the list, and Burp will alert you:

It is not recommended to generally enable the automatic addition of pass through servers automatically, because if your client happens to encounter a one-off problem that causes it to fail an negotiation, then no further SSL connections to that host will be intercepted, until you remove the server from the pass through list.

SSL

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
