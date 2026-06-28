# Same-origin policy (SOP)

Source: https://portswigger.net/web-security/cors/same-origin-policy
Fetched: 2026-06-28T09:17:43.787199+00:00

Web Security Academy

CORS

Same-origin policy

Same-origin policy (SOP)

In this section we explain what the same-origin policy (SOP) is and how it is implemented.

What is the same-origin policy?

The same-origin policy is a web browser security mechanism that aims to prevent websites from attacking each other.

The same-origin policy restricts scripts on one origin from accessing data from another origin. An origin consists of a URI scheme, domain and port number. For example, consider the following URL:

http://normal-website.com/example/example.html

This uses the scheme http, the domain normal-website.com, and the port number 80. The following table shows how the same-origin policy will be applied if content at the above URL tries to access other origins:

URL accessed

Access permitted?

http://normal-website.com/example/

Yes: same scheme, domain, and port

http://normal-website.com/example2/

Yes: same scheme, domain, and port

https://normal-website.com/example/

No: different scheme and port

http://en.normal-website.com/example/

No: different domain

http://www.normal-website.com/example/

No: different domain

http://normal-website.com:8080/example/

No: different port*

*Internet Explorer will allow this access because IE does not take account of the port number when applying the same-origin policy.

Why is the same-origin policy necessary?

When a browser sends an HTTP request from one origin to another, any cookies, including authentication session cookies, relevant to the other domain are also sent as part of the request. This means that the response will be generated within the user's session, and include any relevant data that is specific to the user. Without the same-origin policy, if you visited a malicious website, it would be able to read your emails from GMail, private messages from Facebook, etc.

How is the same-origin policy implemented?

The same-origin policy generally controls the access that JavaScript code has to content that is loaded cross-domain. Cross-origin loading of page resources is generally permitted. For example, the SOP allows embedding of images via the <img> tag, media via the <video> tag, and JavaScript via the <script> tag. However, while these external resources can be loaded by the page, any JavaScript on the page won't be able to read the contents of these resources.

There are various exceptions to the same-origin policy:

Some objects are writable but not readable cross-domain, such as the location object or the location.href property from iframes or new windows.

Some objects are readable but not writable cross-domain, such as the length property of the window object (which stores the number of frames being used on the page) and the closed property.

The replace function can generally be called cross-domain on the location object.

You can call certain functions cross-domain. For example, you can call the functions close, blur and focus on a new window. The postMessage function can also be called on iframes and new windows in order to send messages from one domain to another.

Due to legacy requirements, the same-origin policy is more relaxed when dealing with cookies, so they are often accessible from all subdomains of a site even though each subdomain is technically a different origin. You can partially mitigate this risk using the HttpOnly cookie flag.

It's possible to relax same-origin policy using document.domain. This special property allows you to relax SOP for a specific domain, but only if it's part of your FQDN (fully qualified domain name). For example, you might have a domain marketing.example.com and you would like to read the contents of that domain on example.com. To do so, both domains need to set document.domain to example.com. Then SOP will allow access between the two domains despite their different origins. In the past it was possible to set document.domain to a TLD such as com, which allowed access between any domains on the same TLD, but now modern browsers prevent this.

Find CORS vulnerabilities using Burp Suite

Try for free
