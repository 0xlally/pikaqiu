# Testing for privilege escalation

Source: https://portswigger.net/burp/documentation/desktop/testing-workflow/vulnerabilities/access-controls/privilege-escalation
Fetched: 2026-06-28T09:15:59.177561+00:00

Support Center

Documentation

Desktop editions

Testing workflow

Testing for vulnerabilities

Testing access controls

Testing for privilege escalation

ProfessionalCommunity Edition

Testing for privilege escalation

Last updated:

June 18, 2026

Read time:

3 Minutes

When a user logs in to an application, they usually only have access to the parts of the application that they need to perform their specific tasks. If access controls are incorrectly set, a user can gain access to functionality that should only be available to higher-privileged users.

If you have credentials for a high-privileged and a low-privileged account, you can test the effectiveness of an application's access controls by accessing the application using different accounts. You can use Burp to send ad-hoc requests to compare access or automate the steps for sending multiple requests as a different user.

You can follow along with the processes below using the lab Method based access control can be

circumvented from our Web Security Academy.

Before you start

Get credentials for an admin / high-privileged account and a low-privileged user.

Testing a specific endpoint

To run a quick test on specific endpoints, you can use Burp Repeater:

Go to the Proxy > Intercept tab and click Open browser.

Visit the target site and log in as a high-privileged user. If you're following along using the lab, you can use the credentials administrator:admin.

Access the admin panel and log out.

In Burp's browser, go back to the account page and log in as a low-privileged user. If you're following along using the lab, you can use the credentials wiener:peter.

Go to Proxy > HTTP history.

Right-click the admin panel request sent by the high-privileged user and select Send to Repeater.

Find the low privileged user's most recent request. Select the request and copy the session cookie.

Go to Repeater. Paste the low-privileged user's cookie into the admin panel request, replacing the original session

cookie.

Click Send. Review the response to identify if privilege escalation was possible. In this case, we get a 401 Unauthorized response.

Testing across the entire site

Testing for privilege escalation on a large number of endpoints can be time-consuming. Burp Suite can help you to automate this process across all the requests in the current site map:

Map the application as a high-privileged user. If you're following along using the lab, you can use the credential administrator:admin. Browse around the application to populate Target > Site map making sure you visit the admin panel.

Log out, then log back in as a low-privileged user to obtain their session cookie. If you're following along using the lab, you can use the credentials wiener:peter.

Go to the Proxy > HTTP history tab. Select the low-privileged user's most recent request and copy the session cookie to use later.

Create a session handling rule that adds the low-privileged user's session cookie to all requests sent from the Target tool:

From the Settings dialog, go to Sessions > Session handling rules and click

Add. The Session handling rule editor opens.

Go to the Scope tab.

Under Tools scope, select Target and deselect all other tools.

Under URL scope, select Use custom scope, click Add, then enter the URL of the target site.

Go to the Details tab to define the rule.

Under Rule actions, click Add, then select Set a specific

cookie or parameter value. The

Session handling action editor opens.

Set the following details to add the low-privileged user's session cookie.

Name: session

Value: The cookie you copied from your low-privileged user's request

Keep clicking OK to close all open dialogs. The rule is added to the list of session handling rules.

Re-request the entire site map as a low-privileged user:

Go to the Target > Site map tab, right-click the target host, then select Compare site maps. The Compare site maps dialog opens.

Select Use current site map, then click Next.

Select Use only selected branches.

Select Request map 1 again in a different session context.

Keep the default settings for each of the remaining steps.

Review the two site maps. Any differences are highlighted. Pay close attention to the admin panel requests. Notice that the high-privileged user was able to access the admin panel, but the low-privileged user received a 401 Unauthorized, confirming that this endpoint is not vulnerable in this case.

Note

You can also use the Autorize extension from the BApp Store to compare requests. This lets you browse as a high-privileged and mirrors the requests as a low-privileged user.

Related pages

Burp Repeater

Mapping the visible attack surface with Burp Suite

Comparing site maps

Session handling rule editor
