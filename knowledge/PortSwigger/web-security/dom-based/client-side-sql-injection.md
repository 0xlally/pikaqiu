# DOM-based client-side SQL injection

Source: https://portswigger.net/web-security/dom-based/client-side-sql-injection
Fetched: 2026-06-28T09:17:47.836620+00:00

Web Security Academy

DOM-based

Client-side SQL injection

DOM-based client-side SQL injection

In this section, we'll discuss what DOM-based client-side SQL injection is, describe how an attacker can exploit this vulnerability, and suggest ways to reduce your exposure to this kind of attack.

What is DOM-based client-side SQL injection?

Client-side SQL-injection vulnerabilities arise when a script incorporates attacker-controllable data into a client-side SQL query in an unsafe way. An attacker may be able to use this vulnerability to construct a URL that, if visited by another user, will execute an arbitrary SQL query within the local SQL database of the user's browser.

What is the impact of DOM-based client-side SQL injection?

The potential impact of the vulnerability depends on the website's usage of the SQL database. If the database is used to store sensitive data, such as messages on a social network, the attacker may be able to retrieve this data.

If the database is used to store pending user actions, such as outgoing messages in an email application, then the attacker may be able to modify this data and perform arbitrary actions on the user's behalf.

Which sinks can lead to DOM-based client-side SQL-injection vulnerabilities?

The JavaScript database function executeSql() can lead to client-side SQL-injection vulnerabilities.

How to prevent DOM-based client-side SQL-injection vulnerabilities

In addition to the general measures described on the DOM-based vulnerabilities page, you should make sure that you use parameterized queries (also known as prepared statements) for all database access. This method uses two steps to safely incorporate potentially tainted data into SQL queries:

The application specifies the structure of the query, leaving placeholders for each item of user input.

The application specifies the contents of each placeholder. As the structure of the query has already been defined in the first step, it is not possible for malformed data in the second step to interfere with the query structure.

In the JavaScript executeSql() API, parameterized items can be designated within the query string using the query character ?. For each parameterized item, an additional parameter is passed to the API containing the item's value. To prevent oversights occurring and avoid vulnerabilities being introduced by changes elsewhere within the code base of the application, it is strongly recommended that you parameterize every variable data item that is incorporated into database queries, even if it is not obviously tainted.

Find DOM-based vulnerabilities using Burp Suite

Try for free
