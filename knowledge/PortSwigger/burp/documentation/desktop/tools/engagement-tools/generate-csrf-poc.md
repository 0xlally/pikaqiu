# Generate CSRF PoC

Source: https://portswigger.net/burp/documentation/desktop/tools/engagement-tools/generate-csrf-poc
Fetched: 2026-06-28T09:16:03.499969+00:00

Support Center

Documentation

Desktop editions

Tools

Engagement tools

Generate CSRF PoC

Professional

Generate CSRF PoC

Last updated:

June 18, 2026

Read time:

3 Minutes

You can use this function to generate a proof-of-concept (PoC) cross-site request forgery (CSRF) attack for a given request.

To access this function:

Select a URL or HTTP request from anywhere in Burp.

Right-click and select Engagement tools > Generate CSRF PoC.

Burp shows the full request you selected in the top panel, and the generated CSRF HTML in the lower panel. The HTML uses a form and/or JavaScript to generate the required request in the browser.

You can edit the request manually. Click Regenerate to regenerate the CSRF HTML based on your edited request.

To test the effectiveness of the generated PoC in Burp's browser:

Click Test in browser.

Copy and paste the unique URL into Burp's browser. The browser request is served by Burp with the currently displayed HTML.

To determine whether the PoC is effective, monitor the requests that are made through the Proxy.

Some points should be noted regarding CSRF techniques:

The cross-domain XmlHttpRequest (XHR) technique only works on modern HTML5-capable browsers that support cross-origin resource sharing (CORS). The technique has been tested on current versions of Firefox and Chrome. The browser must have JavaScript enabled. With this technique, the application's response is not processed by the browser in the normal way, so it is not suitable for making cross-domain requests to deliver reflected cross-site scripting (XSS) attacks. Cross-domain XHR is subject to various restrictions which may prevent it from working with some request features. Burp will display a warning in the CSRF PoC generator if this is likely to occur.

Some requests have bodies (such as XML or JSON) that can only be generated using either a form with plain text encoding, or a cross-domain XHR. In the former case, the resulting request will include the header Content-Type: text/plain. In the latter case, the request can include any Content-Type header, but will only qualify as a simple cross-domain request if the Content-Type header has one of the standard values that may be specified for normal HTML forms. This avoids the need for a pre-flight request, which can break the attack. In some cases, although the message body exactly matches that required for the attack request, the application may reject the request due to an unexpected Content-Type header. Such CSRF-like conditions might not be practically exploitable. Burp will display a warning in the CSRF PoC generator if this is likely to occur.

If you manually select a CSRF technique that cannot be used to produce the required request, Burp generates a best effort at a PoC and displays a warning.

If the CSRF PoC generator uses plain text encoding, the request body must contain an equals character. This is necessary for Burp to generate an HTML form which results in that exact body. If the original request does not contain an equals character, you may be able to introduce one at a suitable position in the request, without affecting the server's processing of it.

CSRF PoC options

To access the options, click Options:

CSRF technique - Specify the type of CSRF technique to use in the HTML that generates the CSRF request. The Auto option is generally preferred, and causes Burp to select the most appropriate technique capable of generating the required request.

Include auto-submit script - Burp includes a script in the HTML that causes a JavaScript-enabled browser to automatically issue the CSRF request when the page is loaded.
