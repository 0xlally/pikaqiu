# Token Extractor

Source: https://portswigger.net/bappstore/f24211fa6fcd4bbea6b21f99c5cad27a
Fetched: 2026-06-28T09:15:04.609703+00:00

Support Center

BApp Store

Token Extractor

Professional

Community

Token Extractor

Download BApp

This extension allows tokens to be extracted from a response and replaced in requests.

It can use useful for dealing with anti-CSRF tokens, updated expiration times, sessions in an authorization header, etc.

Using Burp Extractor

If a request requires a value from a response, right click on that request and select "Send to Extractor". Then find a response where the client

receives this value from, and select "Send to Extractor".

Go to the Extractor tab to view a Comparer-like interface, and select the request and response needed, then click "Go".

Within the newly created tab, highlight the content of the request which needs to be replaced, and the content of the response which

contains the value to be inserted. Adjust the scope as necessary, and click "Turn Extractor on".

Once turned on, Extractor will look for occurrences of the regex listed in the request and response panels, and extract or insert data appropriately.

It will also update the "Value to insert" field with the newest value extracted.

Please consult the extension's Github page for a more complete tutorial.

Author

Author

Will Strei

Version

Version

1.3.2a

Rating

Rating

Popularity

Popularity

Last updated

Last updated

10 February 2022

Estimated system impact

Estimated system impact

Overall impact:

Low

Memory

Low

CPU

Low

General

Low

Scanner

Low

You can install BApps directly within Burp, via the BApp Store feature in the Burp Extender tool. You can also download them from here, for offline installation into Burp.

You can view the source code for all BApp Store extensions on our

GitHub page.

Follow

@BApp_Store on Twitter to receive notifications of all BApp releases and updates.

Please note that extensions are written by third party users of Burp, and PortSwigger Web Security makes no warranty about their quality or usefulness for any particular purpose.

Go back to

BappStore

Note:

Please note that extensions are written by third party users of Burp, and PortSwigger Web Security makes no warranty about their quality or usefulness for any particular purpose.
