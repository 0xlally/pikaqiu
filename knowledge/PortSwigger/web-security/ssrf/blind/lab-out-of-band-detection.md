# Lab: Blind SSRF with out-of-band detection

Source: https://portswigger.net/web-security/ssrf/blind/lab-out-of-band-detection
Fetched: 2026-06-28T09:18:04.427454+00:00

Web Security Academy

SSRF

Blind

Lab

Lab: Blind SSRF with out-of-band detection

This site uses analytics software which fetches the URL specified in the Referer header when a product page is loaded.

To solve the lab, use this functionality to cause an HTTP request to the public Burp Collaborator server.

Note

To prevent the Academy platform being used to attack third parties, our firewall blocks interactions between the labs and arbitrary external systems. To solve the lab, you must use Burp Collaborator's default public server.

Solution

Visit a product, intercept the request in Burp Suite, and send it to Burp Repeater.

Go to the Repeater tab. Select the Referer header, right-click and select "Insert Collaborator Payload" to replace the original domain with a Burp Collaborator generated domain. Send the request.

Go to the Collaborator tab, and click "Poll now". If you don't see any interactions listed, wait a few seconds and try again, since the server-side command is executed asynchronously.

You should see some DNS and HTTP interactions that were initiated by the application as the result of your payload.

Community solutions

Rana Khalil

Michael Sommer (no audio)

Find SSRF vulnerabilities using Burp Suite

Try for free
