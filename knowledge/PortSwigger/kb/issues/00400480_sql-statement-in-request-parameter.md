# SQL statement in request parameter

Source: https://portswigger.net/kb/issues/00400480_sql-statement-in-request-parameter
Fetched: 2026-06-28T09:17:11.737143+00:00

Support Center

Issue Definitions

SQL statement in request parameter

SQL statement in request parameter

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: SQL statement in request parameter

HTTP requests sometimes contain SQL syntax. If this is incorporated into a SQL query and executed by the server, then the application is almost certainly vulnerable to SQL injection.

When SQL-like syntax is observed, you should verify whether the request contains a genuine SQL query and whether this is being executed by the server.

Remediation: SQL statement in request parameter

Applications should not incorporate any user-controllable data directly into SQL queries. Parameterized queries (also known as prepared statements) should be used to safely insert data into predefined queries. In no circumstances should users be able to control or modify the structure of the SQL query itself.

References

Web Security Academy: SQL injection

Using Burp to Test for Injection Flaws

Web Security Academy: SQL Injection Cheat Sheet

Vulnerability classifications

CWE-598: Information Exposure Through Query Strings in GET Request

CAPEC-66: SQL Injection

Typical severity

Medium

Type index (hex)

0x00400480

Type index (decimal)

4195456

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
