# Client-side SQL injection (stored DOM-based)

Source: https://portswigger.net/kb/issues/00200332_client-side-sql-injection-stored-dom-based
Fetched: 2026-06-28T09:17:07.697453+00:00

Support Center

Issue Definitions

Client-side SQL injection (stored DOM-based)

Client-side SQL injection (stored DOM-based)

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Client-side SQL injection (stored DOM-based)

Stored DOM-based vulnerabilities arise when user input is stored and later embedded into a response within a part of the DOM that is then processed in an unsafe way by a client-side script. An attacker can leverage the data storage to control a part of the response (for example, a JavaScript string) that can be used to trigger the DOM-based vulnerability.

Client-side SQL injection arises when a script incorporates controllable data into a client-side SQL query in an unsafe way. An attacker may be able to use the vulnerability to construct a URL that, if visited by another application user, will execute an arbitrary SQL query within the local SQL database of the user's browser.

The potential impact of the vulnerability depends on the application's usage of the SQL database. If the database is used to store sensitive data (such as messages in a social networking application), then the attacker may be able to retrieve this data. If the database is used to store pending user actions (such as outgoing messages in an email application), then the attacker may be able to modify this data and carry out actions on the user's behalf.

Burp Suite automatically identifies this issue using dynamic and static code analysis. Static analysis can lead to false positives that are not actually exploitable. If Burp Scanner has not provided any evidence resulting from dynamic analysis, you should review the relevant code and execution paths to determine whether this vulnerability is indeed present, or whether mitigations are in place that would prevent exploitation.

Remediation: Client-side SQL injection (stored DOM-based)

The most effective way to avoid DOM-based client-side SQL injection vulnerabilities is to use parameterized queries (also known as prepared statements) for all database access. This method uses two steps to incorporate potentially tainted data into SQL queries: first, the application specifies the structure of the query, leaving placeholders for each item of user input; second, the application specifies the contents of each placeholder. Because the structure of the query has already been defined in the first step, it is not possible for malformed data in the second step to interfere with the query structure. In the JavaScript executeSql() API, parameterized items can be designated within the query string using the query character (?), and for each parameterized item, an additional parameter is passed to the API containing the item's value. It is strongly recommended that you parameterize every variable data item that is incorporated into database queries, even if it is not obviously tainted, to prevent oversights occurring and avoid vulnerabilities being introduced by changes elsewhere within the code base of the application.

References

Web Security Academy: SQL injection

Web Security Academy: Client-side SQL injection (DOM-based)

Vulnerability classifications

CWE-89: Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection')

CWE-116: Improper Encoding or Escaping of Output

CWE-159: Failure to Sanitize Special Element

CAPEC-66: SQL Injection

Typical severity

High

Type index (hex)

0x00200332

Type index (decimal)

2097970

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
