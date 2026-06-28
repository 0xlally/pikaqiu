# Beware the false false-positive: how to distinguish HTTP pipelining from request smuggling

Source: https://portswigger.net/research/how-to-distinguish-http-pipelining-from-request-smuggling
Fetched: 2026-06-28T09:17:26.363927+00:00

Beware the false false-positive: how to distinguish HTTP pipelining from request smuggling

James Kettle

Director of Research

@albinowax

Published: Tuesday, 19 August 2025 at 14:30 UTC

Updated: Tuesday, 19 August 2025 at 14:31 UTC

Sometimes people think they've found HTTP request smuggling, when they're actually just observing HTTP keep-alive or pipelining. This is usually a false positive, but sometimes there's actually a real vulnerability there! In this post I'll explore how to tell the two apart.

This post was triggered by the publication of http1mustdie.com which resulted in me getting a bunch of messages from people confused and intrigued by connection reuse. The answer is too nuanced to put into a quick reply so I'm writing it up here instead.

Connection reuse false-positives

If you see a request smuggling proof of concept that only works when you reuse connections, it's probably a false positive. Here are some common examples of connection reuse:

Turbo Intruder PoCs where requestsPerConnection is greater than 1

Burp Intruder when HTTP/1 Connection Reuse is enabled

Burp Repeater when using 'Send group in sequence (single connection)' or 'Enable connection reuse'

Burp Repeater attacks that show two HTTP/1 responses in one

However, it's not always a false positive. There are three valid closely related vulnerability classes where connection reuse is required:

Connection-locked request smuggling

Connection state attacks (not technically request smuggling)

Client-side desync attacks

So, when creating a request smuggling proof of concept, always disable connection reuse where possible. If this breaks your attack, you have a choice - give up, or dive deeper.

To help you distinguish between these two scenarios, I have published a Custom Action called Smuggling or pipelining? - you can install it into Burp Repeater using copy+paste, or import via the Extensibility Helper extension in the BApp store.

HTTP/1 connection reuse

Most tools represent HTTP/1 requests as individual, isolated entities. This is usually a convenient abstraction, but request smuggling attempts to break it, so it's crucial to understand the layer below.

To help, we just launched HTTP Hacker - a new Burp Suite extension which exposes low-level HTTP behaviour. To get the most out of these examples, install HTTP Hacker from Extensions->BApp Store and use it to follow along.

Under the hood, HTTP/1.1 reuses connections by concatenating requests and responses on the underlying TCP/TLS socket. This is known as HTTP connection reuse, pipelining, or keep-alive. Here's an example:

POST / HTTP/1.1

Host: hackxor.net

Connection: keep-alive

Content-Length: 5

12345GET /robots.txt HTTP/1.1

Host: hackxor.net

Pipelining is a sub-type of connection reuse where the client sends all their requests in one go and relies on the responses coming back in the correct order. Most servers support pipelined requests, but few real clients send them - it's what makes Turbo Intruder so fast.

Now we understand the fundamentals, let's consider what happens when we sent this CL.0 attack twice, and reuse the connection:

POST / HTTP/1.1

Host: hackxor.net

Content_Length: 47

GET /robots.txt HTTP/1.1

X: Y

Response one:

HTTP/1.1 200 OK

Content-Type: text/html

Response two:

HTTP/1.1 200 OK

Content-Type: text/plain

User-agent: *

Disallow: /settings

We can see that at least one server has ignored the malformed Content_Length header. You might think you've created a desync between the front-end and back-end webserver:

However, all you've actually done is cause a desync between your HTTP client, and the target server:

Here's the underlying request stream:

POST / HTTP/1.1

Host: hackxor.net

Content_Length: 47

GET /robots.txt HTTP/1.1

X: YPOST / HTTP/1.1

Host: hackxor.net

Content_Length: 47

GET /robots.txt HTTP/1.1

X: Y

This is useless. In fact, hackxor doesn't even have a back-end so it's immune to request smuggling.

Hopefully that helps clarify why reusing client connections can cause false positives - please let me know if you have any lingering questions.

Connection-locked request smuggling

It would be nice if I could simply say "never reuse connections when testing for request smuggling", but life is never that simple.

Some front-end servers only reuse the upstream connection if the client connection was reused. This means you can end up with request smuggling vulnerabilities that can only be triggered via client-side connection reuse. I call this scenario connection-locked request smuggling.

To confirm this, see if you can send a request over HTTP/2 that triggers a response containing a separate HTTP/1 response nested inside it. This proves it's not a false positive, and means it's worth investing time in trying to build an exploit. Alternatively, you can often distinguish connection-locked request smuggling using partial requests.

However, to prove a vulnerability is really present, you need to obtain evidence of real impact beyond "an attacker can make themselves receive a surprising response". Connection-locked request smuggling can't be used for direct cross-user attacks, but you can still:

Exploit other users by poisoning the server cache, if it has one

Exploit an input reflection to disclose internal HTTP headers

Bypass any security controls applied by the front-end server

This is your pathway to a valid report! If you think you've found a connection-locked request smuggling, I would suggest the following steps. You can explore these in Turbo Intruder with requestsPerConnection=2, or using a Repeater tab group via 'Send group in sequence (single connection)'.

First, identify whether there is a cache layer and if so, poison it - this is an easy high-impact attack.

If there's no cache, look for an input reflection gadget and use it to reveal any headers the front-end is injecting. Sometimes internal headers enable complete authentication bypass!

If there are any visible front-end security measures, such as requests to certain paths being blocked, see if you can use the request smuggling to bypass them.

Finally, explore how the application responds to host-header tampering, both directly and in smuggled requests. You may be able to use connection-locked request smuggling to gain access to some previously off-limits internal systems, or launch other host-header attacks.

Connection state attacks

When exploring connection-locked request smuggling, you might also uncover connection-state attacks such as first-request routing.

These occur because some servers treat the first request on each connection differently from subsequent requests on the same connection. They are not technically request smuggling vulnerabilities, and can even occur on targets with no front-end server, but ultimately the impact is very similar to connection-locked request smuggling.

HTTP Request Smuggler supports a 'connection-state probe' which will attempt to automatically identify these.

Client-side desync attacks

There is one other scenario where connection reuse is exploitable, and that is client-side desync attacks. Note that this comes with a major restriction - the attack request must be something you can get the victims' web browser to send, cross-domain! In practice, this means you can't use any header obfuscation techniques. For further information, refer to Browser-Powered Desync Attacks, and our client-side desync Academy topic.

Conclusion

I hope you found that useful! Request smuggling is a topic with immense depth and this is just a taster. If you'd like to master it, check out all our desync research, and our full Academy topic with 20+ interactive labs.

Request Smuggling

Back to all articles

Related Research

06 August 2025

Making desync attacks easy with TRACE

19 March 2024

Making desync attacks easy with TRACE

Making HTTP header injection critical via response queue poisoning

22 September 2022

Making HTTP header injection critical via response queue poisoning

How to turn security research into profit

06 September 2022

How to turn security research into profit
