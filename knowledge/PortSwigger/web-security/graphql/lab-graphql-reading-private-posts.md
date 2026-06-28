# Lab: Accessing private GraphQL posts

Source: https://portswigger.net/web-security/graphql/lab-graphql-reading-private-posts
Fetched: 2026-06-28T09:17:51.020339+00:00

Web Security Academy

GraphQL API vulnerabilities

Lab

Lab: Accessing private GraphQL posts

The blog page for this lab contains a hidden blog post that has a secret password. To solve the lab, find the hidden blog post and enter the password.

Learn more about Working with GraphQL in Burp Suite.

Solution

Identify the vulnerability

In Burp's browser, access the blog page.

In Burp, go to Proxy > HTTP history and notice the following:

Blog posts are retrieved using a GraphQL query.

In the response to the GraphQL query, each blog post has its own sequential id.

Blog post id 3 is missing from the list. This indicates that there is a hidden blog post.

Find the POST /graphql/v1 request. Right-click it and select Send to Repeater.

In Repeater, right-click anywhere in the Request panel of the message editor and select GraphQL > Set introspection query to insert an introspection query into the request body.

Send the request. Notice in the response that the BlogPost type has a postPassword field available.

Exploit the vulnerability to find the password

In the HTTP history, find the POST /graphql/v1 request. Right-click it and select Send to Repeater.

In Repeater, click on the GraphQL tab. In the Variables panel, modify the id variable to 3 (the ID of the hidden blog post).

In the Query panel, add the postPassword field to the query.

Send the request.

Copy the contents of the response's postPassword field and paste them into the Submit solution dialog to solve the lab. You may need to refresh the page.

Community solutions

Intigriti

Popo Hack

Test GraphQL APIs using Burp Suite

Try for free
