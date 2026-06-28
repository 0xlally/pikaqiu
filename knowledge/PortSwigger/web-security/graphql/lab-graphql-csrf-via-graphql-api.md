# Lab: Performing CSRF exploits over GraphQL

Source: https://portswigger.net/web-security/graphql/lab-graphql-csrf-via-graphql-api
Fetched: 2026-06-28T09:17:51.132658+00:00

Web Security Academy

GraphQL API vulnerabilities

Lab

Lab: Performing CSRF exploits over GraphQL

The user management functions for this lab are powered by a GraphQL endpoint. The endpoint accepts requests with a content-type of x-www-form-urlencoded and is therefore vulnerable to cross-site request forgery (CSRF) attacks.

To solve the lab, craft some HTML that uses a CSRF attack to change the viewer's email address, then upload it to your exploit server.

You can log in to your own account using the following credentials: wiener:peter.

Learn more about Working with GraphQL in Burp Suite.

Solution

Open Burp's browser, access the lab and log in to your account.

Enter a new email address, then click Update email.

In Burp, go to Proxy > HTTP history and check the resulting request. Note that the email change is sent as a GraphQL mutation.

Right-click the email change request and select Send to Repeater.

In Repeater, amend the GraphQL query to change the email to a second different address.

Click Send.

In the response, notice that the email has changed again. This indicates that you can reuse a session cookie to send multiple requests.

Convert the request into a POST request with a Content-Type of x-www-form-urlencoded. To do this, right-click the request and select Change request method twice.

Notice that the mutation request body has been deleted. Add the request body back in with URL encoding.

The body should look like the below:

query=%0A++++mutation+changeEmail%28%24input%3A+ChangeEmailInput%21%29+%7B%0A++++++++changeEmail%28input%3A+%24input%29+%7B%0A++++++++++++email%0A++++++++%7D%0A++++%7D%0A&operationName=changeEmail&variables=%7B%22input%22%3A%7B%22email%22%3A%22hacker%40hacker.com%22%7D%7D

Right-click the request and select Engagement tools > Generate CSRF PoC. Burp displays the CSRF PoC generator dialog.

Amend the HTML in the CSRF PoC generator dialog so that it changes the email a third time. This step is necessary because otherwise the exploit won't make any changes to the current email address at the time it is run. Likewise, if you test the exploit before delivering, make sure that you change the email from whatever it is currently set to before delivering to the victim.

Copy the HTML.

In the lab, click Go to exploit server.

Paste the HTML into the exploit server and click Deliver exploit to victim to solve the lab.

Community solutions

Popo Hack

Intigriti

Test GraphQL APIs using Burp Suite

Try for free
