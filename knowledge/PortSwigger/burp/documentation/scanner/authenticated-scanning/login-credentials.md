# Login credentials

Source: https://portswigger.net/burp/documentation/scanner/authenticated-scanning/login-credentials
Fetched: 2026-06-28T09:16:10.014507+00:00

Support Center

Documentation

Scanner

Authenticated scanning

Login credentials

DASTProfessional

Login credentials

Last updated:

June 18, 2026

Read time:

2 Minutes

Both Burp Suite Professional and Burp Suite DAST enable you to specify login credentials that Burp Scanner can use when scanning applications that use a single-step login mechanism. Specifying a valid username and password enables Burp Scanner to audit content that only authenticated users can usually see.

Note

We recommend using a recorded login sequence, even for sites that use basic username and password authentication. Recorded logins support the status check, which helps the scanner stay logged in and can make scans faster and deeper. In Burp Suite DAST, recorded logins also enable the pre-scan check to confirm that authentication is working before scanning begins. If your site uses a more complex login mechanism, you must use a recorded login sequence, as Burp Scanner may be unable to log in otherwise.

You can only use one authentication method per scan. If you enter both login credentials and a recorded login sequence, the Burp Scanner ignores the login credentials provided.

How does Burp Scanner use login credentials?

Burp Scanner begins crawls with an unauthenticated phase in which it does not submit any credentials. This enables Burp Scanner to discover any login and self-registration functions within the application.

Note

For more information on how Burp identifies login and self-registration forms, see Identifying login and registration forms.

If the application supports self-registration, Burp Scanner by default attempts to register a user at this point.

If the Use invalid usernames to trigger login failures scan configuration setting is enabled, Burp Scanner also attempts to submit bogus credentials to the site. Although these credentials cannot be used to log in, they might still reach interesting functions such as account recovery mechanisms.

Note

If you select Only perform an authenticated crawl using the provided credentials from the Crawl strategy section of the scan configuration, then Burp Scanner skips the unauthenticated phase of the crawl.

Next, Burp Scanner attempts an authenticated crawl. It visits the login function multiple times and attempts to login using:

The credentials for the self-registered account (if applicable).

The credentials you specify for any pre-existing account.

Burp Scanner logs in using each set of credentials in turn and crawls the content behind the login mechanism. This enables the system to capture the different functions that are available to different types of user.

Login settings

The Testing login functions section of the crawling scan configuration enables you to configure aspects of Burp Scanner's behavior during authenticated crawls. You can configure:

Whether Burp Scanner attempts to self-register a new user on the target website before performing the crawl.

Whether Burp Scanner uses bogus credentials to deliberately trigger login failures.

Related page

Adding usernames and passwords to a site - explains how to manage usernames and passwords for sites in Burp Suite DAST.

Application login options - explains how to manage usernames and passwords for applications in the desktop editions of Burp Suite.

Scan configuration: Crawl settings.
