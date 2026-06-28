# Analyzing session token generation with Burp Suite

Source: https://portswigger.net/burp/documentation/desktop/testing-workflow/vulnerabilities/session-management/analyzing-session-token-generation
Fetched: 2026-06-28T09:16:00.798203+00:00

Support Center

Documentation

Desktop editions

Testing workflow

Testing for vulnerabilities

Testing session management mechanisms

Analyzing session token generation

ProfessionalCommunity Edition

Analyzing session token generation with Burp Suite

Last updated:

June 18, 2026

Read time:

1 Minute

Session tokens must be generated in a way that makes them unpredictable. Predictable session tokens can expose websites to session hijacking attacks, where an attacker accesses another user's active session. If this is an authenticated session, the attacker could access the user's data and potentially perform malicious operations on behalf of the user.

You can use Burp Sequencer to collect a large number of session tokens, and analyze them for predictability.

Before you start

Log in to the target site to generate an authenticated session cookie.

Steps

You can follow along with the process below using ginandjuice.shop, our deliberately vulnerable demonstration site. Use the credentials carlos:hunter2 to log in, then use the post-login response that issued your authenticated session cookie.

Go to Proxy > HTTP history and look for the response that issued your authenticated session cookie.

Select the session cookie, right-click it and select Send to Sequencer.

In the Sequencer tab, click Start live capture to harvest session tokens from the web application. The live capture dialog opens.

When the live capture is complete, click Analyze now to analyze the tokens.

Review the results of the analysis.

The Summary tab gives you an overall assessment of the randomness of the tokens. You can use the other tabs to perform a deeper analysis. For more information, see Burp Sequencer.

Related pages

Burp Sequencer analysis results
