# Lab: Accidental exposure of private GraphQL fields

Source: https://portswigger.net/web-security/graphql/lab-graphql-accidental-field-exposure
Fetched: 2026-06-28T09:17:51.053526+00:00

Web Security Academy

GraphQL API vulnerabilities

Lab

Lab: Accidental exposure of private GraphQL fields

The user management functions for this lab are powered by a GraphQL endpoint. The lab contains an access control vulnerability whereby you can induce the API to reveal user credential fields.

To solve the lab, sign in as the administrator and delete the username carlos.

Learn more about Working with GraphQL in Burp Suite.

Solution

Identify the vulnerability

In Burp's browser, access the lab and select My account.

Attempt to log in to the site.

In Burp, go to Proxy > HTTP history and notice that the login attempt is sent as a GraphQL mutation containing a username and password.

Right-click the login request and select Send to Repeater.

In Repeater, right-click anywhere within the Request panel of the message editor and select GraphQL > Set introspection query to insert an introspection query into the request body.

Send the request.

Right-click the message and select GraphQL > Save GraphQL queries to site map.

Go to Target > Site map and review the GraphQL queries. Notice the following:

There is a getUser query that returns a user's username and password.

This query fetches the relevant user information via a direct reference to an id number.

Modify the query to retrieve the administrator credentials

Right-click the the getUser query and select Send to Repeater.

In Repeater, click Send. Notice that the default id value of 0 doesn't return a user.

Select the GraphQL tab and test alternative values for the id variable until the API returns the administrator's credentials. In this case, the administrator's ID is 1.

Log in to the site as the administrator, go to the Admin panel, and delete carlos to solve the lab.

Community solutions

Popo Hack

Test GraphQL APIs using Burp Suite

Try for free
