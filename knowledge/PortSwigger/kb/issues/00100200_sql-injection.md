# SQL injection

Source: https://portswigger.net/kb/issues/00100200_sql-injection
Fetched: 2026-06-28T09:17:04.966303+00:00

Support Center

Issue Definitions

SQL injection

SQL injection

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

What is SQL injection?

SQL injection (or SQLi) is a serious vulnerability responsible for many high-profile data breaches.

SQL injection typically allows an attacker to extract the entire database from the vulnerable website, including user information, encrypted passwords, and business data. This can subsequently lead to mass compromise of user accounts, data being encrypted and held to ransom, or stolen data being sold to third parties. Many SQL injection vulnerabilities can be easily found and abused using off-the-shelf tools, making them highly likely to be exploited than vulnerabilities that require a skilled attacker.

SQL injection vulnerabilities normally arise when an application incorporates user data into a database query in an unsafe manner. An attacker can manipulate the data to cause their own database query to execute, allowing them to read or modify the contents of the database.

Organizations that fall victim to SQL injection attacks are often unaware that the vulnerability has been exploited. In some cases, victims become aware of vulnerabilities many months or years after they have been exploited by attackers to steal the organization's data.

Description: SQL injection

SQL injection vulnerabilities arise when user-controllable data is incorporated into database SQL queries in an unsafe manner. An attacker can supply crafted input to break out of the data context in which their input appears and interfere with the structure of the surrounding query.

A wide range of damaging attacks can often be delivered via SQL injection, including reading or modifying critical application data, interfering with application logic, escalating privileges within the database and taking control of the database server.

Remediation: SQL injection

The most effective way to prevent SQL injection attacks is to use parameterized queries (also known as prepared statements) for all database access. This method uses two steps to incorporate potentially tainted data into SQL queries: first, the application specifies the structure of the query, leaving placeholders for each item of user input; second, the application specifies the contents of each placeholder. Because the structure of the query has already been defined in the first step, it is not possible for malformed data in the second step to interfere with the query structure. You should review the documentation for your database and application platform to determine the appropriate APIs which you can use to perform parameterized queries. It is strongly recommended that you parameterize every variable data item that is incorporated into database queries, even if it is not obviously tainted, to prevent oversights occurring and avoid vulnerabilities being introduced by changes elsewhere within the code base of the application.

You should be aware that some commonly employed and recommended mitigations for SQL injection vulnerabilities are not always effective:

One common defense is to double up any single quotation marks appearing within user input before incorporating that input into a SQL query. This defense is designed to prevent malformed data from terminating the string into which it is inserted. However, if the data being incorporated into queries is numeric, then the defense may fail, because numeric data may not be encapsulated within quotes, in which case only a space is required to break out of the data context and interfere with the query. Further, in second-order SQL injection attacks, data that has been safely escaped when initially inserted into the database is subsequently read from the database and then passed back to it again. Quotation marks that have been doubled up initially will return to their original form when the data is reused, allowing the defense to be bypassed.

Another often cited defense is to use stored procedures for database access. While stored procedures can provide security benefits, they are not guaranteed to prevent SQL injection attacks. The same kinds of vulnerabilities that arise within standard dynamic SQL queries can arise if any SQL is dynamically constructed within stored procedures. Further, even if the procedure is sound, SQL injection can arise if the procedure is invoked in an unsafe manner using user-controllable data.

References

Web Security Academy: SQL injection

Using Burp to Test for Injection Flaws

Web Security Academy: SQL Injection Cheat Sheet

Vulnerability classifications

CWE-89: Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection')

CWE-94: Improper Control of Generation of Code ('Code Injection')

CWE-116: Improper Encoding or Escaping of Output

CAPEC-66: SQL Injection

Typical severity

High

Type index (hex)

0x00100200

Type index (decimal)

1049088

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
