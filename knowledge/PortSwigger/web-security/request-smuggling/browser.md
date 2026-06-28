# Browser-powered request smuggling

Source: https://portswigger.net/web-security/request-smuggling/browser
Fetched: 2026-06-28T09:18:01.502649+00:00

Web Security Academy

Request smuggling

Browser-powered

Browser-powered request smuggling

In this section, you'll learn how you can craft high-severity exploits without relying on malformed requests that browsers will never send. Not only does this expose a whole new range of websites to server-side request smuggling, it enables you to perform client-side variations of these attacks by inducing a victim's browser to poison its own connection to a vulnerable web server.

PortSwigger Research

The materials and labs in this section are based on Browser-Powered Desync Attacks: A New Frontier in HTTP Request Smuggling by PortSwigger Research. This research also led to the discovery of a bypass technique for Host header filters, using connection-state flaws.

CL.0 request smuggling

Back-end servers can sometimes be persuaded to ignore the Content-Length header, which effectively means they ignore the body of incoming requests. This paves the way for request smuggling attacks that don't rely on chunked transfer encoding or HTTP/2 downgrading.

Learn more

LEARN CL.0 request smuggling

LAB CL.0 request smuggling

Client-side desync attacks

Request smuggling is traditionally considered a server-side issue because it can only be exploited using specialist tools like Burp Repeater - standard browsers simply won't send the kinds of requests needed to trigger the desync. However, building on the lessons learned from CL.0 attacks, it's sometimes possible to cause a desync using fully browser-compatible HTTP/1 requests.

You can use these browser-compatible requests to trigger a client-side desync (CSD) between a browser and vulnerable web server, enabling attacks on single-server sites, which are otherwise immune to request smuggling, and intranet sites that you can't access directly.

Learn more

LEARN Client-side desync attacks

LAB Client-side desync

Pause-based desync attacks

Seemingly secure websites may contain hidden desync vulnerabilities that only reveal themselves if you pause mid-request. By sending the headers, promising a body, and then just waiting, you can sometimes find additional desync vulnerabilities that can be used for both server-side and client-side exploits.

Learn more

LEARN Pause-based desync attacks

LAB Server-side pause-based request smuggling

Find HTTP request smuggling vulnerabilities using Burp Suite

Try for free
