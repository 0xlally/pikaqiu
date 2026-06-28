# Allowlisting an application for CORS

Source: https://portswigger.net/burp/documentation/dast/user-guide/post-installation-config/whitelist-application-cors
Fetched: 2026-06-28T09:15:38.938184+00:00

DAST

Allowlisting an application for CORS

Last updated:

June 18, 2026

Read time:

2 Minutes

Cloud

Self-hosted

You can use our GraphQL API to integrate Burp Suite DAST with third-party applications. For web applications that send requests to the API using client-side JavaScript, you need to allowlist the origin of these requests for cross-origin resource sharing (CORS).

This enables you to develop more powerful integrated applications that can fetch the relevant data, create and edit sites, and launch new scans directly from the browser using AJAX.

Note

Even if you're integrating Burp Suite DAST with your CI/CD system using our native plugins, you still need to allowlist your Jenkins or TeamCity URL in order to use the Burp site-driven scan option.

You can allowlist as many origins as you want, each separated by a new line:

Log in to Burp Suite DAST as an administrator.

From the settings menu , select Connectivity.

In the Allowed Origins for GraphQL API section, enter the origin on which the other application is running. make sure that you include the URL scheme, domain name, and port. For example:

https://third-party-app.com:8082

https://custom-app.your-company.net:8083

When you're sure your entries are correct, click Save.

Test your external application to make sure it works as expected.

If you still run into CORS-related issues, examine the Origin header of the associated request and compare this to the URLs that you have in the allowlist. There should be no discrepancies.

Note

The origin of incoming requests refers only to the URL scheme, domain name, and port. In other words, you can allowlist all cross-origin requests from https://example.com:8080 but you cannot restrict this to specific subdirectories such as https://example.com:8080/my-app. For more granular control, you need to deploy your application to a dedicated subdomain:

https://your-app.example.com:8080

Read more

For more information about CORS, the same-origin policy, and the related security implications, please refer to the corresponding topic on our Web Security Academy.

Cross-origin resource sharing
