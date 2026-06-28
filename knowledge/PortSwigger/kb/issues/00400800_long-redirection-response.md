# Long redirection response

Source: https://portswigger.net/kb/issues/00400800_long-redirection-response
Fetched: 2026-06-28T09:17:12.280185+00:00

Support Center

Issue Definitions

Long redirection response

Long redirection response

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Long redirection response

The application returned a redirection response containing a "long" message body. Ordinarily, this content is not displayed to the user, because the browser automatically follows the redirection.

Occasionally, redirection responses contain sensitive data. For example, if the user requests a page that they are not authorized to view, then an application might issue a redirection to a different page, but also include the contents of the prohibited page.

You should review the contents of the response to determine whether it contains anything sensitive.

Remediation: Long redirection response

In cases where the application handles requests for unauthorized content by redirecting to a different URL, the application should ensure that no sensitive content is included within the redirection response. Depending on the application and the platform, this might involve checking for proper authorization earlier in the request handling logic, or using a different API to perform the redirection.

References

Web Security Academy: Information disclosure

Vulnerability classifications

CWE-698: Execution After Redirect (EAR)

CAPEC-37: Retrieve Embedded Sensitive Data

Typical severity

Information

Type index (hex)

0x00400800

Type index (decimal)

4196352

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Burp Scanner

This issue - and many more like it - can be found using our

web vulnerability scanner

Read more

Get Burp

Scan your web application from just $499.00

Find out more
