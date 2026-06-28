# Lab: SQL injection UNION attack, retrieving multiple values in a single column

Source: https://portswigger.net/web-security/sql-injection/union-attacks/lab-retrieve-multiple-values-in-single-column
Fetched: 2026-06-28T09:18:04.010899+00:00

Web Security Academy

SQL injection

UNION attacks

Lab

Lab: SQL injection UNION attack, retrieving multiple values in a single column

This lab contains a SQL injection vulnerability in the product category filter. The results from the query are returned in the application's response so you can use a UNION attack to retrieve data from other tables.

The database contains a different table called users, with columns called username and password.

To solve the lab, perform a SQL injection UNION attack that retrieves all usernames and passwords, and use the information to log in as the administrator user.

Hint

You can find some useful payloads on our SQL injection cheat sheet.

Solution

Use Burp Suite to intercept and modify the request that sets the product category filter.

Determine the number of columns that are being returned by the query and which columns contain text data. Verify that the query is returning two columns, only one of which contain text, using a payload like the following in the category parameter:

'+UNION+SELECT+NULL,'abc'--

Use the following payload to retrieve the contents of the users table:

'+UNION+SELECT+NULL,username||'~'||password+FROM+users--

Verify that the application's response contains usernames and passwords.

Community solutions

Rana Khalil

z3nsh3ll

Michael Sommer

Find SQL injection vulnerabilities using Burp Suite

Try for free
