# Professional 1.6.26

Source: https://portswigger.net/burp/releases/professional-1-6-26
Fetched: 2026-06-28T09:16:27.827493+00:00

This release adds the ability to detect blind server-side XML/SOAP injection by triggering interactions with Burp Collaborator.

Previously, Burp Scanner has detected XML/SOAP injection by submitting some XML-breaking syntax like:

]]>>

and analyzing responses for any resulting error messages.

Burp now sends payloads like:

<nzf xmlns="http://a.b/"

xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://a.b/ http://kuiqswhjt3era6olyl63pyd.burpcollaborator.net/nzf.xsd">

nzf</nzf>

and reports an appropriate issue based on any observed interactions (DNS or HTTP) that reach the Burp Collaborator server.

Note that this type of technique is effective even when the original parameter value does not contain XML, and there is no indication within the request or response that XML/SOAP is being used on the server side.

The new scan check uses both schema location and XInclude to cause the server-side XML parser to interact with the Collaborator server.

In addition, when the original parameter value does contain XML being submitted by the client, Burp now also uses the schema location and XInclude techniques to try to induce external service interactions. (We believe that Burp is now aware of all available tricks for inducing a server-side XML parser to interact with an external network service. But we would be very happy to hear of any others that people know about.)
