# SQL Injection in Different Statement Types

Source: https://portswigger.net/support/sql-injection-in-different-statement-types
Fetched: 2026-06-28T09:17:34.995006+00:00

This page may be out of date

We haven't updated it for a while because we're busy working on new, improved content to help you get the

most out of Burp Suite. In the meantime, please note that the information on this page may no longer be

accurate.

Visit our Support Center

SQL Injection in Different Statement Types

The SQL language contains a number of verbs that may appear at the beginning of statements. Because it is the most commonly used verb, the majority of SQL injection vulnerabilities arise within SELECT statements. However, SQL injection flaws can exist within any type of statement. When you are interacting with a remote application, it usually is not possible to know in advance what type of statement a given item of user input will be processed by. However, you can usually make an educated guess based on the type of application function you are dealing with.

Once you have detected a potential SQL vulnerability, one of the next steps is to identify the type of statement type you are dealing with.

The example uses a version of "Mutillidae" taken from OWASP's Broken Web Application Project. Find out how to download, install and use this project.

SELECT Statements

Select statements are used to retrieve information from the database. They are frequently employed in functions where the application returns information in response to user actions, such as viewing a profile or performing a search.

They are also often used in login functions where user-supplied information is checked against data retrieved from a database.

The Bypassing Authentication article demonstrates how to bypass the authentication of a vulnerable login page by injecting in to a SELECT statement.

INSERT Statements

INSERT statements are used to create a new row of data within a table. They are commonly used when an application adds a new entry to an audit log, creates a new user account, or generates a new order.

In this example a new user provides details such as username, password & signature in order to create an account. The submitted data is inserted into the applications database via an INSERT statement:

INSERT INTO accounts (username, password, mysignature) VALUES ('xxx', 'yyy', 'zzz');

If the application is vulnerable, an attacker can inject arbitrary values in to the database using crafted input.

We can demonstrate the vulnerability by adding a user account using the Username parameter:

name','pass','sign')-- -

Having determined that the application is processing SQL queries, if we can locate where the injected data is reflected back by the application, we can alter our input to extract data.

Once we log in to the application we can see the 'signature' parameter is reflected in the status message.

By injecting subqueries into the 'signature' parameter we should be able to extract data in the status message.

By inserting the subquery (select version()) we hope to get the MySQL version number.

When we log back in to the application we can see the version number of the database reflected in the status message. This confirms that the injection is successful.

We can then use this technique to obtain other information from the database.

For example, we could try to obtain the password of another user.

In this example we have managed to obtain the password hash for the user "root".

UPDATE Statements

UPDATE statements are used to modify one or more existing rows of data within a table. They are often used in functions where a user changes the value of data that already exists - for example, updating contact information, changing her password, or changing the quantity on a line of an order.

A typical UPDATE statement works much like an INSERT statement, except that it usually contains a WHERE clause to tell the database which rows of the table to update. For example:

UPDATE contacts SET Email="User@test.com" WHERE Name = 'User'

This Contacts table allows us to add new contacts, update single contacts and search for existing contacts within the database.

However, if the application is vulnerable to SQL injection, an attacker can bypass the application's logic and gain unauthorized access to data.

By adding '-- to our input, we are able to remove the WHERE clause in the UPDATE statement of this application.

Removing the WHERE clause means that every contact in the database is updated with the same information.

Note: This is a clear example of how probing for SQL injection vulnerabilities in a remote application is always potentially dangerous, because you have no way of knowing in advance quite what action the application will perform using your crafted input.
