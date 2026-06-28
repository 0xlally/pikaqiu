# CORS and the Access-Control-Allow-Origin response header

Source: https://portswigger.net/web-security/cors/access-control-allow-origin
Fetched: 2026-06-28T09:17:43.090756+00:00

Web Security Academy

CORS

CORS and ACAO

CORS and the Access-Control-Allow-Origin response header

In this section we explain what the Access-Control-Allow-Origin header is in respect of CORS, and how it forms part of CORS implementation.

The cross-origin resource sharing specification provides controlled relaxation of the same-origin policy for HTTP requests to one website domain from another through the use of a collection of HTTP headers. Browsers permit access to responses to cross-origin requests based upon these header instructions.

What is the Access-Control-Allow-Origin response header?

The Access-Control-Allow-Origin header is included in the response from one website to a request originating from another website, and identifies the permitted origin of the request. A web browser compares the Access-Control-Allow-Origin with the requesting website's origin and permits access to the response if they match.

Implementing simple cross-origin resource sharing

The cross-origin resource sharing (CORS) specification prescribes header content exchanged between web servers and browsers that restricts origins for web resource requests outside of the origin domain. The CORS specification identifies a collection of protocol headers of which Access-Control-Allow-Origin is the most significant. This header is returned by a server when a website requests a cross-domain resource, with an Origin header added by the browser.

For example, suppose a website with origin normal-website.com causes the following cross-domain request:

GET /data HTTP/1.1

Host: robust-website.com

Origin : https://normal-website.com

The server on robust-website.com returns the following response:

HTTP/1.1 200 OK

...

Access-Control-Allow-Origin: https://normal-website.com

The browser will allow code running on normal-website.com to access the response because the origins match.

The specification of Access-Control-Allow-Origin allows for multiple origins, or the value null, or the wildcard *. However, no browser supports multiple origins and there are restrictions on the use of the wildcard *.

Handling cross-origin resource requests with credentials

The default behavior of cross-origin resource requests is for requests to be passed without credentials like cookies and the Authorization header. However, the cross-domain server can permit reading of the response when credentials are passed to it by setting the CORS Access-Control-Allow-Credentials header to true. Now if the requesting website uses JavaScript to declare that it is sending cookies with the request:

GET /data HTTP/1.1

Host: robust-website.com

...

Origin: https://normal-website.com

Cookie: JSESSIONID=<value>

And the response to the request is:

HTTP/1.1 200 OK

...

Access-Control-Allow-Origin: https://normal-website.com

Access-Control-Allow-Credentials: true

Then the browser will permit the requesting website to read the response, because the Access-Control-Allow-Credentials response header is set to true. Otherwise, the browser will not allow access to the response.

Relaxation of CORS specifications with wildcards

The header Access-Control-Allow-Origin supports wildcards. For example:

Access-Control-Allow-Origin: *

Note

Note that wildcards cannot be used within any other value. For example, the following header is not valid:

Access-Control-Allow-Origin: https://*.normal-website.com

Fortunately, from a security perspective, the use of the wildcard is restricted in the specification as you cannot combine the wildcard with the cross-origin transfer of credentials (authentication, cookies or client-side certificates). Consequently, a cross-domain server response of the form:

Access-Control-Allow-Origin: *

Access-Control-Allow-Credentials: true

is not permitted as this would be dangerously insecure, exposing any authenticated content on the target site to everyone.

Given these constraints, some web servers dynamically create Access-Control-Allow-Origin headers based upon the client-specified origin. This is a workaround for CORS constraints that is not secure. We'll show you how this can be exploited later.

Pre-flight checks

The pre-flight check was added to the CORS specification to protect legacy resources from the expanded request options allowed by CORS. Under certain circumstances, when a cross-domain request includes a non-standard HTTP method or headers, the cross-origin request is preceded by a request using the OPTIONS method, and the CORS protocol necessitates an initial check on what methods and headers are permitted prior to allowing the cross-origin request. This is called the pre-flight check. The server returns a list of allowed methods in addition to the trusted origin and the browser checks to see if the requesting website's method is allowed.

For example, this is a pre-flight request that is seeking to use the PUT method together with a custom request header called Special-Request-Header:

OPTIONS /data HTTP/1.1

Host: <some website>

...

Origin: https://normal-website.com

Access-Control-Request-Method: PUT

Access-Control-Request-Headers: Special-Request-Header

The server might return a response like the following:

HTTP/1.1 204 No Content

...

Access-Control-Allow-Origin: https://normal-website.com

Access-Control-Allow-Methods: PUT, POST, OPTIONS

Access-Control-Allow-Headers: Special-Request-Header

Access-Control-Allow-Credentials: true

Access-Control-Max-Age: 240

This response sets out the allowed methods (PUT, POST and OPTIONS) and permitted request headers (Special-Request-Header). In this particular case the cross-domain server also allows the sending of credentials, and the Access-Control-Max-Age header defines a maximum timeframe for caching the pre-flight response for reuse. If the request methods and headers are permitted (as they are in this example) then the browser processes the cross-origin request in the usual way. Pre-flight checks add an extra HTTP request round-trip to the cross-domain request, so they increase the browsing overhead.

Does CORS protect against CSRF?

CORS does not provide protection against cross-site request forgery (CSRF) attacks, this is a common misconception.

CORS is a controlled relaxation of the same-origin policy, so poorly configured CORS may actually increase the possibility of CSRF attacks or exacerbate their impact.

There are various ways to perform CSRF attacks without using CORS, including simple HTML forms and cross-domain resource includes.

Find CORS vulnerabilities using Burp Suite

Try for free
