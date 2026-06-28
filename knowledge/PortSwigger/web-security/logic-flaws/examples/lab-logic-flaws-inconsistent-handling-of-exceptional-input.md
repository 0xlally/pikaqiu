# Lab: Inconsistent handling of exceptional input

Source: https://portswigger.net/web-security/logic-flaws/examples/lab-logic-flaws-inconsistent-handling-of-exceptional-input
Fetched: 2026-06-28T09:17:55.636288+00:00

Web Security Academy

Business logic vulnerabilities

Examples

Lab

Lab: Inconsistent handling of exceptional input

This lab doesn't adequately validate user input. You can exploit a logic flaw in its account registration process to gain access to administrative functionality. To solve the lab, access the admin panel and delete the user carlos.

Hint

You can use the link in the lab banner to access an email client connected to your own private mail server. The client will display all messages sent to @YOUR-EMAIL-ID.web-security-academy.net and any arbitrary subdomains. Your unique email ID is displayed in the email client.

Solution

While proxying traffic through Burp, open the lab and go to the "Target" > "Site map" tab. Right-click on the lab domain and select "Engagement tools" > "Discover content" to open the content discovery tool.

Click "Session is not running" to start the content discovery. After a short while, look at the "Site map" tab in the dialog. Notice that it discovered the path /admin.

Try to browse to /admin. Although you don't have access, an error message indicates that DontWannaCry users do.

Go to the account registration page. Notice the message telling DontWannaCry employees to use their company email address.

From the button in the lab banner, open the email client. Make a note of the unique ID in the domain name for your email server (@YOUR-EMAIL-ID.web-security-academy.net).

Go back to the lab and register with an exceptionally long email address in the format:

very-long-string@YOUR-EMAIL-ID.web-security-academy.net

The very-long-string should be at least 200 characters long.

Go to the email client and notice that you have received a confirmation email. Click the link to complete the registration process.

Log in and go to the "My account" page. Notice that your email address has been truncated to 255 characters.

Log out and go back to the account registration page.

Register a new account with another long email address, but this time include dontwannacry.com as a subdomain in your email address as follows:

very-long-string@dontwannacry.com.YOUR-EMAIL-ID.web-security-academy.net

Make sure that the very-long-string is the right number of characters so that the "m" at the end of @dontwannacry.com is character 255 exactly.

Go to the email client and click the link in the confirmation email that you have received. Log in to your new account and notice that you now have access to the admin panel. The confirmation email was successfully sent to your email client, but the application server truncated the address associated with your account to 255 characters. As a result, you have been able to register with what appears to be a valid @dontwannacry.com address. You can confirm this from the "My account" page.

Go to the admin panel and delete carlos to solve the lab.

Community solutions

Rana Khalil

Michael Sommer

Find business logic vulnerabilities using Burp Suite

Try for free
