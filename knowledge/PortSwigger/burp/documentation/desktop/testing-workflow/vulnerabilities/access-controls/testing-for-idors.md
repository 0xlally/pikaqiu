# Testing for IDORs

Source: https://portswigger.net/burp/documentation/desktop/testing-workflow/vulnerabilities/access-controls/testing-for-idors
Fetched: 2026-06-28T09:15:58.735810+00:00

Support Center

Documentation

Desktop editions

Testing workflow

Testing for vulnerabilities

Testing access controls

Testing for IDORs

ProfessionalCommunity Edition

Testing for IDORs

Last updated:

June 18, 2026

Read time:

2 Minutes

Insecure Direct Object References (IDORs) are a type of access control vulnerability in which an application uses user-supplied input to access objects such as files, directories, or database records directly.

If suitable access controls are not in place, this enables attackers to manipulate these references and gain access to other objects without authorization.

IDORs are sometimes confused with other types of access control vulnerability. Note that the term "IDOR" specifically refers to vulnerabilities in which an application exposes references to its own internal implementation objects.

Steps

These steps use the User ID controlled by request parameter Web Security Academy lab to demonstrate the process. However, the principle of running a Sniper attack in Burp Intruder should apply to any application in which you find exposed object references in a URL.

Identify parameters or other locations in which you suspect an IDOR vulnerability exists.

In the example lab you would select My account and log in using username wiener and password peter. Note that the URL now shows the query parameter id=wiener. This strongly indicates that, on this site, the user ID is used to retrieve the relevant user's data in order to render the account page.

Forward the relevant request to Burp Intruder. In the example lab, this is the GET /my-account?id=wiener request from the HTTP History tab.

Go to Intruder and make sure that Sniper attack is selected.

Highlight the parameter that you want to test and click Add § to set this as a payload position.

In the Payloads side panel, add a list of the test values you want to use in the attack. The example lab requires a list of usernames. If you're using Burp Suite Professional, you can open the Add from list drop-down menu and select the Usernames list.

Click Start attack. Burp Intruder sends a series of new requests, replacing the selected payload positions with each username in the list.

Study the responses to look for indications that some of the requests sent in the attack were successful.

In this case, requests sent to /my-account?id=administrator and /my-account?id=carlos received a 200 OK response. This indicates that you may be able to access the account pages for these usernames without authorization. If the responses to these requests show that the page was retrieved then the IDOR vulnerability is confirmed.

Related pages

Web Security Academy: Insecure direct object references (IDOR)

Burp Intruder documentation
