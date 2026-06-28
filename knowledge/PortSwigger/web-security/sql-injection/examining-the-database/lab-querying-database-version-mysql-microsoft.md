# Lab: SQL injection attack, querying the database type and version on MySQL and Microsoft

Source: https://portswigger.net/web-security/sql-injection/examining-the-database/lab-querying-database-version-mysql-microsoft
Fetched: 2026-06-28T09:18:03.432524+00:00

Web Security Academy

SQL injection

Examining the database

Lab

Lab: SQL injection attack, querying the database type and version on MySQL and Microsoft

This lab contains a SQL injection vulnerability in the product category filter. You can use a UNION attack to retrieve the results from an injected query.

To solve the lab, display the database version string.

Hint

You can find some useful payloads on our SQL injection cheat sheet.

Solution

Use Burp Suite to intercept and modify the request that sets the product category filter.

Determine the number of columns that are being returned by the query and which columns contain text data. Verify that the query is returning two columns, both of which contain text, using a payload like the following in the category parameter:

'+UNION+SELECT+'abc','def'#

Use the following payload to display the database version:

'+UNION+SELECT+@@version,+NULL#

Community solutions

z3nsh3ll

Rana Khalil

Michael Sommer

Find SQL injection vulnerabilities using Burp Suite

Try for free
