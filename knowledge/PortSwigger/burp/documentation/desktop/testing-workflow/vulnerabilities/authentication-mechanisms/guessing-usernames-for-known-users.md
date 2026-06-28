# Guessing usernames for known users

Source: https://portswigger.net/burp/documentation/desktop/testing-workflow/vulnerabilities/authentication-mechanisms/guessing-usernames-for-known-users
Fetched: 2026-06-28T09:15:59.369068+00:00

Support Center

Documentation

Desktop editions

Testing workflow

Testing for vulnerabilities

Testing authentication mechanisms

Guessing usernames for known users

ProfessionalCommunity Edition

Guessing usernames for known users

Last updated:

June 18, 2026

Read time:

2 Minutes

Burp Intruder has a built-in username generator that takes an input and produces a list of potential usernames using common patterns. For example, if you were to provide the input Carlos Montoya the generator would return carlos.montoya, mcarlos, and similar combinations.

This is useful in circumstances where you know details of a specific user (for example, their name or email address) but don't know their exact username. It provides a more targeted way of enumerating usernames than a generic name list.

Note

You can test this process out in the Username enumeration via different responses Web Security Academy lab.

Steps

In Burp's HTTP history, identify a failure message for a username-based authentication mechanism.

In the message, highlight the username value, right-click, and select Send to Intruder.

Go to Intruder. Notice that Burp has automatically added the username as a payload position.

Make sure that Sniper attack is selected.

In the Payloads side panel, change the Payload type to Username generator.

Under Payload configuration, enter an input that you want to base the generated usernames on. You can add multiple inputs if required.

In the Maximum payloads per item field, enter the number of usernames you want Burp to generate. Burp generates this number of usernames for every input added.

Click Start attack. Intruder generates its list of potential usernames and runs an attack testing each username in turn.

Analyze the attack results to check for interesting patterns, such as usernames that results in anomalous error messages, response times, or a different HTTP response code.

Related pages

Burp Intruder

Enumerating usernames with Burp Suite
