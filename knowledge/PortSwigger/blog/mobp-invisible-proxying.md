# [MoBP] Invisible proxying

Source: https://portswigger.net/blog/mobp-invisible-proxying
Fetched: 2026-06-28T09:15:20.850411+00:00

[MoBP] Invisible proxying

Dafydd Stuttard |

Wednesday, 5 November 2008 at 06:54 UTC

MoBP

burp

Standard intercepting proxies generally work fine in almost any situation where you are using a standard web browser to access an application. You simply need to configure your browser to use the proxy listening on your loopback interface, and you are away.

Things get trickier if the application employs a thick client component that runs outside of the browser, or makes its own HTTP requests outside of the browser's framework. Sometimes, these clients don't support HTTP proxies, or don't provide an easy way to configure them to use one.

In this situation, you face two distinct problems. The first is that the client's requests are being sent straight to the destination host, rather than to your loopback interface (or wherever your intercepting proxy is listening). This problem can usually be quickly resolved by redirecting the client's requests lower down the stack - e.g. by adding an entry to your hosts file, or changing your routing configuration.

The second problem is that the client typically generates standard HTTP requests rather than proxy-style requests. A proxy-style request looks like this:

GET http://myapp.com/foo.php HTTP/1.1

Host: myapp.com

whereas the corresponding non-proxy request looks like this:

GET /foo.php HTTP/1.1

Host: myapp.com

HTTP proxies need to receive the full URL on the first line of the request in order to determine which destination host to forward the request to. Proxies do not (if they follow the standards) look at the Host header to determine the destination.

This means that if your intercepting proxy complies with the standards, it will fail to process non-proxy style requests. And this is what the currently available version of Burp does. So even if you can redirect your thick client's requests to the Burp Proxy listener, it will ignore them.

In the new version, you can configure Burp to support invisible proxying, meaning that it will tolerate non-proxy style requests. When such a request is received, Burp will by default parse out the contents of the Host header, and use that as the destination host for that request. Alternatively, you can specify a host and port to which all requests should be forwarded, regardless of the Host header. You can also use this redirection function even for regular proxy-style requests, if you want to redirect all traffic to a different host than the one the browser seeks to connect to.

The UI for configuring proxy listeners now looks like this, with an example of an invisible proxy listener and redirector configured on port 8888:

More perceptive readers may have wondered: what about SSL? If a non-proxy-aware client uses SSL, it obviously won't issue CONNECT requests to the Burp Proxy listener, but will attempt to negotiate SSL directly with the listener. Does this mean we need to configure the listener to expect SSL or plain HTTP connections?

Actually, you don't. When operating in invisible proxy mode, Burp is clever enough (what else would you expect?!) to figure out whether each incoming request is HTTP or HTTPS, and to handle the SSL negotiation seamlessly in the latter case. You can even configure a different server SSL certificate for each proxy listener, if your thick client requires a particular server certificate.

If the client you are testing issues both HTTP and HTTPS requests, to different ports, you will need to configure a separate Proxy listener on each relevant port. Again, not a problem now that Burp supports multiple listeners.

In summary, this is a feature that will hardly ever be required, but will occasionally be a life saver and enable you to continue using Burp with many kinds of unusual thick client components.

MoBP

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
