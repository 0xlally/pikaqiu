# Lab: Single-endpoint race conditions

Source: https://portswigger.net/web-security/race-conditions/lab-race-conditions-single-endpoint
Fetched: 2026-06-28T09:17:59.775377+00:00

Web Security Academy

Race conditions

Lab

Lab: Single-endpoint race conditions

This lab's email change feature contains a race condition that enables you to associate an arbitrary email address with your account.

Someone with the address carlos@ginandjuice.shop has a pending invite to be an administrator for the site, but they have not yet created an account. Therefore, any user who successfully claims this address will automatically inherit admin privileges.

To solve the lab:

Identify a race condition that lets you claim an arbitrary email address.

Change your email address to carlos@ginandjuice.shop.

Access the admin panel.

Delete the user carlos

You can log in to your own account with the following credentials: wiener:peter.

You also have access to an email client, where you can view all emails sent to @exploit-<YOUR-EXPLOIT-SERVER-ID>.exploit-server.net addresses.

Note

Solving this lab requires Burp Suite 2023.9 or higher.

Solution

Predict a potential collision

Log in and attempt to change your email to anything@exploit-<YOUR-EXPLOIT-SERVER-ID>.exploit-server.net. Observe that a confirmation email is sent to your intended new address, and you're prompted to click a link containing a unique token to confirm the change.

Complete the process and confirm that your email address has been updated on your account page.

Try submitting two different @exploit-<YOUR-EXPLOIT-SERVER-ID>.exploit-server.net email addresses in succession, then go to the email client.

Notice that if you try to use the first confirmation link you received, this is no longer valid. From this, you can infer that the website only stores one pending email address at a time. As submitting a new email address edits this entry in the database rather than appending to it, there is potential for a collision.

Benchmark the behavior

Send the POST /my-account/change-email request to Repeater.

In Repeater, add the new tab to a group. For details on how to do this, see Creating a new tab group.

Right-click the grouped tab, then select Duplicate tab. Create 19 duplicate tabs. The new tabs are automatically added to the group.

In each tab, modify the first part of the email address so that it is unique to each request, for example, test1@exploit-<YOUR-EXPLOIT-SERVER-ID>.exploit-server.net, test2@..., test3@... and so on.

Send the group of requests in sequence over separate connections. For details on how to do this, see Sending requests in sequence.

Go back to the email client and observe that you have received a single confirmation email for each of the email change requests.

Probe for clues

In Repeater, send the group of requests again, but this time in parallel, effectively attempting to change the pending email address to multiple different values at the same time. For details on how to do this, see Sending requests in parallel.

Go to the email client and study the new set of confirmation emails you've received. Notice that, this time, the recipient address doesn't always match the pending new email address.

Consider that there may be a race window between when the website:

Kicks off a task that eventually sends an email to the provided address.

Retrieves data from the database and uses this to render the email template.

Deduce that when a parallel request changes the pending email address stored in the database during this window, this results in confirmation emails being sent to the wrong address.

Prove the concept

In Repeater, create a new group containing two copies of the POST /my-account/change-email request.

Change the email parameter of one request to anything@exploit-<YOUR-EXPLOIT-SERVER-ID>.exploit-server.net.

Change the email parameter of the other request to carlos@ginandjuice.shop.

Send the requests in parallel.

Check your inbox:

If you received a confirmation email in which the address in the body matches your own address, resend the requests in parallel and try again.

If you received a confirmation email in which the address in the body is carlos@ginandjuice.shop, click the confirmation link to update your address accordingly.

Go to your account page and notice that you now see a link for accessing the admin panel.

Visit the admin panel and delete the user carlos to solve the lab.

Community solutions

Popo Hack

Find race condition vulnerabilities using Burp Suite

Try for free
