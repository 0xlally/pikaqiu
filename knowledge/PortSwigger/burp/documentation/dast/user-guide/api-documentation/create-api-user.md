# Creating API users

Source: https://portswigger.net/burp/documentation/dast/user-guide/api-documentation/create-api-user
Fetched: 2026-06-28T09:15:34.140000+00:00

DAST

Creating API users

Last updated:

June 18, 2026

Read time:

1 Minute

If you want to integrate Burp Suite DAST with other software, such as Jira or a CI system, you need to create a dedicated API user that the other software will use to authenticate communication with Burp Suite DAST via either the REST API or GraphQL API.

Note

API users cannot log in to the web UI.

Log in as an administrator and go to Team > Add a new user.

Enter a name and username that will help you easily identify the user later, for example, "Jenkins Build".

Enter an email address, for example, the email address of the admin user.

Select the login type API Key.

When you are happy with your changes, click the save icon in the upper-right corner.

When prompted, copy the API key and URL, and save them somewhere secure. You will need these later.

Note that you cannot retrieve the API key for an existing user. If you lose it, you will have to generate a new key and manually update any files where it's used.
