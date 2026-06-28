# Invisible proxying

Source: https://portswigger.net/burp/documentation/desktop/tools/proxy/invisible
Fetched: 2026-06-28T09:16:06.899310+00:00

Support Center

Documentation

Desktop editions

Tools

Burp Proxy

Invisible proxying

ProfessionalCommunity Edition

Invisible proxying

Last updated:

June 18, 2026

Read time:

4 Minutes

Burp's support for invisible proxying allows non-proxy-aware clients to connect directly to a Proxy listener. This is useful if the target application uses a thick client component that runs outside of the browser, or a browser plugin that makes HTTP requests outside of the browser's framework. Often, these clients don't support HTTP proxies, or don't provide an easy way to configure them.

Redirecting inbound requests

You can force the non-proxy-aware client to connect to Burp. Modify your DNS resolution to redirect the relevant hostname, and set up invisible Proxy listeners on the ports used by the application.

For example, if the application uses the domain name example.org, and HTTP and HTTPS on the standard ports, add an entry to your hosts file that redirects the domain name to your local machine:

127.0.0.1 example.org

To receive the redirected requests, create invisible Burp Proxy listeners on 127.0.0.1:80 and 127.0.0.1:443. The non-proxy-aware client then resolves the domain name to your local IP address, and sends requests directly to your listeners on that interface.

Invisible proxy mode

It's easy to use DNS to redirect client requests to the local listeners, but the need for a special invisible proxy mode arises because the resulting requests will not be in the form that is expected by an HTTP proxy.

When you use plain HTTP, a proxy-style request looks like this:

GET http://example.org/foo.php HTTP/1.1

Host: example.org

The corresponding non-proxy-style request looks like this:

GET /foo.php HTTP/1.1

Host: example.org

Normally, web proxies use the full URL in the first line of the request to determine the destination host. They do not look at the Host header to determine the destination. If you enable invisible proxying, when Burp receives any non-proxy-style requests it parses out the contents of the Host header. It uses the Host header as the destination host for that request.

If you use HTTPS with a proxy, clients send a CONNECT request that identifies the destination host and then perform TLS negotiation. However, non-proxy-aware clients proceed directly to TLS negotiation, believing they are communicating directly with the destination host. If you enable invisible proxying, Burp tolerates direct negotiation of TLS by the client, and parses out the contents of the Host header from the decrypted request.

Redirecting outbound requests

In invisible mode, Burp forwards requests to destination hosts based on the Host header parsed out of each request. However, because you have modified the hosts file entry for the relevant domain, Burp resolves the hostname to the local listener address. Unless configured differently it forwards the request back to itself. This creates an infinite loop.

There are two methods for resolving this problem:

In some cases, all the invisibly proxied traffic heads for a single domain. The non-proxy-aware client only ever contacts a single domain. You can use the Proxy listener's redirection settings to force the outgoing traffic to go to the correct IP address.

In some cases, the proxied traffic heads for multiple domains. You can use Burp's own hostname resolution settings to override the hosts file and redirect each domain individually back to its correct original IP address.

A related problem arises if the non-proxy-aware client does not include a Host header in its requests. If Burp processes non-proxy-style requests without this header, it cannot determine which destination host to forward the requests to.

There are two methods for resolving this problem. If all requests should be forwarded to the same destination host, you can use the Proxy listener's redirection settings to force the outgoing traffic to go to the correct IP address.

If different requests should be forwarded to different hosts, you need to use multiple Proxy listeners:

Create a separate virtual network interface for each destination host. Most operating systems let you create additional virtual interfaces with loopback-like properties. Alternatively, this is possible in virtualized environments.

Create a separate Proxy listener for each interface, or two listeners if HTTP and HTTPS are both in use.

Use your hosts file to redirect each destination hostname to a different listener.

Configure the listener on each interface to redirect all traffic to the IP address of the host whose traffic was redirected to it.

Handling TLS certificates

You can use various configurations for the server TLS certificates used by Burp Proxy listeners. The default configuration automatically generates a certificate for each destination host. This may not work with invisible proxying. Non-proxy-aware clients negotiate TLS directly with the listener, without first sending a CONNECT request to identify the destination host.

Many clients, including browsers, support the "server_name" extension in the Client Hello message. This identifies the destination host that the client wishes to negotiate with. If this extension is present, Burp uses it to generate a certificate for that host in the normal way. If the extension is not present, Burp fails over to use a static self-signed certificate instead.

There are two methods to resolve this problem:

If all HTTPS requests are to the same domain, you can configure the invisible listener to generate a CA-signed certificate with the specific hostname used by the application.

If HTTPS requests are to different domains, create an invisible Proxy listener with a different virtual network interface for each destination host. Configure each listener to generate a CA-signed certificate with the specific hostname that traffic is being redirected to.
