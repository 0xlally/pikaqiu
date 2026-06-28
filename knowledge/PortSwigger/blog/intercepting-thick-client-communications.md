# Intercepting thick client communications

Source: https://portswigger.net/blog/intercepting-thick-client-communications
Fetched: 2026-06-28T09:15:17.821404+00:00

Intercepting thick client communications

Dafydd Stuttard |

Friday, 10 April 2009 at 15:00 UTC

thick clients

burp

I've written before about how Burp's invisible proxying mode can help you intercept requests from non-proxy-aware thick clients. Burp Suite Pro now contains a new feature which makes this task even easier.

If you are using a thick client component which cannot be configured to use a proxy, you can force it to talk to Burp Proxy instead of the actual destination host by performing the following steps:

Modify your operating system hosts file to resolve the relevant destination hostnames to your loopback address (127.0.0.1), for example:

127.0.0.1 www.example.org

127.0.0.1 secure.example.org

For each destination port used by the application (typically 80 and 443), start a proxy listener on this port of your loopback interface, and configure the listener to support invisible proxying.

With this set-up, the thick client will talk directly to Burp Proxy, thinking it is talking to the destination application, and Burp will accept and process the non-proxy-style requests it receives. When Burp processes these requests, it determines which actual destination host to forward them to based on the Host header in the requests. And this can lead to a problem if you have modified your hosts file as described above: Burp will resolve the hostnames to your loopback address, and will forward them back to itself, creating an infinite loop.

Previously, you could work around this problem by getting Burp to rewrite the Host header, or by using multiple machines with different DNS configurations for your testing. Now, things are much easier, because you can configure hostname resolution within Burp, to override the resolution provided by your operating system:

With this configuration, Burp will redirect outbound requests to the correct destination IP addresses, based on the Host header within each request. All being well, you should be able to intercept and forward traffic to multiple external domains, despite the thick client not itself supporting proxy connections.

One further complication may arise if your client does not include a Host header in its requests. If you are only dealing with one destination host, this is easily resolved: you can configure your proxy listener to redirect all traffic to a specific IP address. If you are dealing with multiple destination hosts, things get trickier again. You may be able to use Burp Extender to figure out the host based on the URL or other features of the request, and insert the correct Host header. Or you may be left with running Burp on multiple machines, and using your hosts file to redirect traffic for each destination host to a different intercepting machine.

thick clients

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
