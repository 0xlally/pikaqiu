# The single-packet attack: making remote race-conditions 'local'

Source: https://portswigger.net/research/the-single-packet-attack-making-remote-race-conditions-local
Fetched: 2026-06-28T09:17:30.318677+00:00

The single-packet attack: making remote race-conditions 'local'

James Kettle

Director of Research

@albinowax

Published: Wednesday, 18 October 2023 at 12:54 UTC

Updated: Wednesday, 18 October 2023 at 12:59 UTC

The single-packet attack is a new technique for triggering web race conditions. It works by completing multiple HTTP/2 requests with a single TCP packet, which effectively eliminates network jitter and means the requests get processed extremely close together. This makes remote race conditions just as easy to exploit as if they were local.

It's been great to see the community having a lot of success finding race conditions with the single-packet attack over the last two months. One person even used it to exploit a website I made myself. Quite a few people have asked what other network protocols it might work on, so in this post I'll explore protocols including HTTP/3, HTTP/1.1, WebSockets, and SMTP. Where it's not viable, I'll look at what the best alternatives are. I'll also provide guidelines for adapting it to your protocol of choice.

Single-packet attack recap

I introduced the single-packet attack in Smashing the state machine: the true potential of web race conditions. If you're already familiar with it, you can skip this section.

Why jitter hides race conditions

To trigger a race condition, you typically need a website to receive and process multiple HTTP requests in a very small time-window. Requests sent to remote systems simultaneously don't reliably arrive simultaneously thanks to network jitter; unpredictable, network-induced delays in packet transmission:

This makes detecting race conditions on remote systems much harder than on local systems.

Solving jitter with the single-packet attack

The single-packet solves network jitter by adapting and combining the 'last byte sync' and 'timeless timing attack' techniques:

Issue all the requests over a single HTTP/2 connection, withholding a tiny fragment from each so the server doesn't start to process it

Wait for a short time for the packets to arrive on the target server

Issue the final fragment of each of the requests

Your operating system will group these into a single TCP packet

You can visualise the result as something like this:

The use of a single TCP packet to complete all the requests means that they always get processed at the same time, regardless of how much network jitter delayed their delivery. This approach easily scales to 20-30 requests, and is shockingly easy to implement. It's available in Burp Suite's Repeater via the tab group functionality, and also in my open source extension Turbo Intruder.

If you'd like to try the technique out for yourself, try out our free race condition labs.

For further details on the development and implementation of this technique, and some benchmarks, check out the original whitepaper or this presentation clip.

Applying the single-packet attack to other protocols

Given how powerful the single-packet attack is, it's natural to wonder if it can be adapted to other network protocols, perhaps enabling an HTTP/3 login limit-overrun, a WebSocket race condition, or an SMTP timing attack. Let's take a look and see.

HTTP/3

First off, let's take a look at HTTP/3. The main difference between HTTP/2 and HTTP/3 is that HTTP/2 is layered on top of TLS and TCP, whereas HTTP/3 is built on QUIC and UDP.

To apply the single-packet attack over HTTP/3, we need to complete multiple HTTP requests with a single UDP datagram. HTTP/3's support for multiplexing means this is definitely possible, but there's one limitation. UDP has a maximum packet size of ~1,500 bytes, as opposed to TCP's 65,535. This might make HTTP/3 sound terrible for the single-packet attack, but in practice, TCP has a soft limit of 1,500 bytes as well and I never explored how to push beyond this because 20-30 requests is sufficient for most race conditions.

Ultimately, HTTP/3 does support the single-packet attack but it's probably not worth the development effort right now. If you want to push the state of the art of race condition exploits over HTTP forward, you'd probably be better off trying to improve the HTTP/2 implementation to get closer to TCP's max packet size. This could enable around 800 requests completed simultaneously, which would be quite entertaining.

HTTP/1.1

HTTP/1.1 lets you send multiple requests over a single TCP connection, and thanks to TCP buffering on many servers you don't need to wait for a response before sending the next message. Stuffing multiple requests down a connection without waiting for a reply is known as pipelining, and it's the key feature that makes Turbo Intruder so fast. Using pipelining, it's technically possible to stuff multiple entire HTTP requests into a single TCP packet.

Unfortunately, the RFC dictates that the server must send the responses in the order that the requests were received in. This means that although it's technically possible for a HTTP server to process multiple pipelined requests simultaneously, it wouldn't give the server much of a speed boost since the response to the first request would end up blocking the response to the second. This is sometimes referred to as the 'head of line blocking' problem.

Thanks to this problem, I think you'll find that although plenty of webservers support pipelined requests, they'll get processed sequentially and if you want to do a race condition attack you'd be better off using parallel connections with last-byte sync. Burp Repeater will do this automatically for HTTP/1.1 connections.

SMTP

Just like HTTP/1.1, you can stuff multiple SMTP messages into a single packet, using the pipelining extension as defined in RFC 2920. Unfortunately, once again the responses must be sent in order, so it's unlikely that any implementations would process these requests in parallel.

This is a shame, because I expect there's some interesting race conditions hidden behind SMTP handlers.

WebSocket

The WebSocket protocol is much more promising than HTTP/1.1 because there's no concept of a 'response'. This means servers can process multiple messages sent over a single connection concurrently without worrying about what order to send any resulting messages in. Of course, some implementations may still choose not to do this, to avoid the complexity.

Unlike HTTP/2, you can't abuse fragmentation to increase the number of messages you can complete with the critical packet. This is because although you're allowed to fragment messages, you can't have multiple fragmented messages in-flight at the same time:

The fragments of one message MUST NOT be interleaved between the fragments of another message RFC6455

The good news is, there's a solution waiting in RFC 8441 - Bootstrapping WebSockets with HTTP/2. This proposes nesting WebSocket connections inside HTTP/2 streams, and would enable full power single-packet attacks on servers that support it.

I think WebSocket race conditions are widely overlooked due to little tooling targeting this niche, so the area has a lot of potential even without the single-packet attack.

Other protocols?

The key feature that enables the single-packet attack is multiplexing - support for multiple concurrent messages on a single connection. Many protocols support multiple sequential messages in a single packet, sometimes unintentionally, but they're generally let down by server implementation choices.

Support for interleaved fragments is a crucial performance factor, as it increases the number of messages that can be squeezed into a packet. The other major performance factor is the maximum packet size of the underlying protocol.

Coalescing at different layers

Coalescing the final request fragments into a single TCP packet isn't the only viable option. You could alternatively place the final fragments in a single TLS record. Since TLS is layered over TCP, this would work even if the record was delivered via multiple distinct TCP packets.

I believe this would enable the attack to work reliably through non-decrypting tunnels like SOCKS proxies. However, it would probably require a customised TLS implementation so ultimately it'd be trickier to implement than the classic TCP approach.

Conclusion

Right now, there's a bunch of web race conditions on HTTP/2 websites that were near-impossible to detect and exploit are now ripe for the taking. We've used RFC-based analysis to evaluate which other protocols might support the variants of single-packet attack. The next step for any of these would be to create a proof of concept tool, and then do some probing on popular server implementations to see if they're compatible. As ever, if there's no proof of concept, it's not really proven!

New tooling would potentially expose a bunch more vulnerabilities affecting WebSockets, and perhaps some more HTTP-based ones that require over 30 simultaneous requests to detect.

If you missed it, you might also like building custom scanners for web security automation.

race condition

Back to all articles

Related Research

WebSocket Turbo Intruder: Unearthing the WebSocket Goldmine

17 September 2025

WebSocket Turbo Intruder: Unearthing the WebSocket Goldmine

How to build custom scanners for web security research automation

03 October 2023

How to build custom scanners for web security research automation

Smashing the state machine

the true potential of web race conditions

09 August 2023

Smashing the state machine

the true potential of web race conditions

Cracking reCAPTCHA, Turbo Intruder style

20 November 2019

Cracking reCAPTCHA, Turbo Intruder style
