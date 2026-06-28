# LDAP injection

Source: https://portswigger.net/kb/issues/00100500_ldap-injection
Fetched: 2026-06-28T09:17:05.374046+00:00

Support Center

Issue Definitions

LDAP injection

LDAP injection

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: LDAP injection

LDAP injection arises when user-controllable data is copied in an unsafe way into an LDAP query that is performed by the application. If an attacker can inject LDAP metacharacters into the query, then they can interfere with the query's logic. Depending on the function for which the query is used, the attacker may be able to retrieve sensitive data to which they are not authorized, or subvert the application's logic to perform some unauthorized action.

Note that automated difference-based tests for LDAP injection flaws can often be unreliable and are prone to false positive results. Scanner results should be manually reviewed to confirm whether a vulnerability is actually present.

Remediation: LDAP injection

If possible, applications should avoid copying user-controllable data into LDAP queries. If this is unavoidable, then the data should be strictly validated to prevent LDAP injection attacks. In most situations, it will be appropriate to allow only short alphanumeric strings to be copied into queries, and any other input should be rejected. At a minimum, input containing any LDAP metacharacters should be rejected; characters that should be blocked include ( ) ; , * | & = and whitespace.

Vulnerability classifications

CWE-90: Improper Neutralization of Special Elements used in an LDAP Query ('LDAP Injection')

CWE-116: Improper Encoding or Escaping of Output

CAPEC-136: LDAP Injection

Typical severity

High

Type index (hex)

0x00100500

Type index (decimal)

1049856

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
