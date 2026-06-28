# Input returned in response (stored)

Source: https://portswigger.net/kb/issues/00400b00_input-returned-in-response-stored
Fetched: 2026-06-28T09:17:12.984975+00:00

Support Center

Issue Definitions

Input returned in response (stored)

Input returned in response (stored)

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Input returned in response (stored)

Retrieval of stored input arises when user input is stored and later embedded into the application's responses.

Input being returned in application responses is not a vulnerability in its own right. However, it is a prerequisite for many client-side vulnerabilities, including cross-site scripting, open redirection, content spoofing, and response header injection. Additionally, some server-side vulnerabilities such as SQL injection are often easier to identify and exploit when input is returned in responses. In applications where input retrieval is rare and the environment is resistant to automated testing (for example, due to a web application firewall), it might be worth subjecting instances of it to focused manual testing.

Vulnerabilities resulting from retrieval of stored input are typically more serious than the equivalent reflected vulnerabilities because they do not require a separate delivery mechanism in order to reach target users. Depending on the affected functionality, ordinary users may be exploited during normal use of the application. Note that automated detection of stored data retrieval cannot reliably determine whether input that is persisted within the application can be retrieved by any other user, only by authenticated users, or only by the attacker themselves. You should review the functionality in which the vulnerability appears to determine whether the application's behavior can feasibly be used to compromise other application users.

Vulnerability classifications

CWE-20: Improper Input Validation

CWE-116: Improper Encoding or Escaping of Output

Typical severity

Information

Type index (hex)

0x00400b00

Type index (decimal)

4197120

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
