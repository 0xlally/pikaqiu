# Determining the session timeout

Source: https://portswigger.net/burp/documentation/desktop/testing-workflow/vulnerabilities/session-management/session-timeout
Fetched: 2026-06-28T09:16:01.053167+00:00

Support Center

Documentation

Desktop editions

Testing workflow

Testing for vulnerabilities

Testing session management mechanisms

Determining the session timeout

ProfessionalCommunity Edition

Determining the session timeout

Last updated:

June 18, 2026

Read time:

2 Minutes

When a user doesn't use an application for a certain amount of time, most applications will automatically log out the user and destroy their session.

To determine how long it takes for a session to timeout, you can use Burp Intruder to issue the same request multiple times with increasing delays. This enables you to test compliance with security standards that require applications to timeout within a specified period. A longer timeout gives an attacker more time to use or guess a session token.

Steps

You can follow along with the process below using ginandjuice.shop, our deliberately vulnerable demonstration site.

To determine the session timeout:

In Burp's browser, log in to your target website. If you're using ginandjuice.shop, the correct credentials are carlos:hunter2.

Go to Proxy > HTTP history. Identify a logged-in request and send it to Intruder.

Go to Intruder.

In the Payloads side panel, under Payload type, select Null payloads.

Under Payload configuration, select Continue indefinitely.

Click on the Resource pool tab to open the Resource pool side panel.

Select Create new resource pool.

In the resource pool settings, select Delay between requests, then Increase

delay in

increments of ___ milliseconds. Add a delay time.

Click Start attack. The attack starts running in a new dialog. Intruder repeatedly sends the requests, with an

increasing delay between requests.

With the attack results dialog open, click Columns on the top-level menu and select Time of day. A Time of day column is added to the results table. Sort the results by this column.

Review the responses as the attack progresses. Identify the first request that indicates the session is invalid. For example, look for a redirection to a login page.

To determine the session timeout, identify the time difference between the logged-out request and the previous request.

Note

This attack may take some time. To continue the attack in the background, close the results dialog and click

Continue attack in background. The attack is added to the Tasks panel on the

Dashboard.

Related pages

Burp Intruder
