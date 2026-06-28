# Using Hackability to uncover a Chrome infoleak

Source: https://portswigger.net/research/using-hackability-to-uncover-a-chrome-infoleak
Fetched: 2026-06-28T09:17:31.810766+00:00

Using Hackability to uncover a Chrome infoleak

Gareth Heyes

Researcher

@garethheyes

Published: Thursday, 1 September 2022 at 13:00 UTC

Updated: Thursday, 1 September 2022 at 13:32 UTC

I've been hacking browsers for over 15 years and one of the challenges I set myself was to find a SOP bypass or info leak in every major browser. Chrome was the last browser standing…until now. This post will walk you through how I exploited a flaw that had been buried for nearly 5 years.

It all started when one of our Academy labs on dangling markup injection stopped working. I've blogged about this previously which led to a CSP bypass. The technique involves setting an iframe location to about:blank which enables you to read the name property of the cross domain window. Normally you wouldn't be allowed to do this because cross domain windows are protected by Same Origin Policy (SOP). SOP is a browser feature that prevents different websites from reading data off each other, for example facebook.com from reading data from google.com.

Bypassing CSP was great but I thought there could be more vulnerabilities to find as lots of properties were being leaked when the about:blank location was set. The first step was to use my Hackability Inspector - a security-focused enumerator. I added an iframe to a different domain which also contained another iframe. Next, in the main inspector window I set the location of the subframe on the cross domain window:

x.contentWindow[0].location='about:blank';

Then once I had set the location I inspected the cross domain window, I changed the input of the main inspector window to inspect the cross domain iframe window and hit return:

x.contentWindow[0]

Look at all those properties! There must be some data leaking somewhere. I scrolled down the list of properties but there were too many. So I started filtering by properties I knew contained interesting information. I found I could access the document object:

x.contentWIndow[0].document

I continued filtering for known properties like document.URL which was set to "about:blank" obviously no good. Then I remembered the baseURI property and filtered for it and to my delight it contained cross domain information:

This property contained information about the full URL and you could get that from a different subdomain. Imagine attachments.example.com could read the entire URL of oauth.example.com and steal OAuth tokens provided they have at least one iframe and was frameable. I confirmed that if the external URL was modified with hash or query string parameters they could be read from the different subdomain and decided to report it to Google.

Google investigated the issue after I'd simplified my proof of concept and found the baseURI problem was known since 2017:

// TODO(tkent): Referring to ParentDocument() is not correct.  See

// crbug.com/751329.

if (Document* parent = ParentDocument())

return parent->BaseURL();

The baseURI property was reporting an incorrect URL but nobody had managed to demonstrate a security vulnerability until now. Using a framed page with an existing iframe I could use this bug to obtain cross domain information. Google awarded me $2000 for this vulnerability.

Proof of concept

Conclusion

This issue demonstrates that minor bugs such as incorrectly assigned properties can be chained together with existing techniques to expose cross domain information. When enumerating it's a good idea to look for properties that contain external URLs as they can lead to cross domain information disclosure.

Timeline

2022-06-16 9:37 AM GMT+1 - Reported to Google

2022-07-08 7:15 PM GMT+1 - Google patches issue

2022-08-18 - Google awards $2000 bounty for this issue

2022-08-30 - Chrome released

2022-09-01 14:00 PM GMT - Blog post published

Browser hacking

Infoleak

SOP

browser security

Back to all articles
