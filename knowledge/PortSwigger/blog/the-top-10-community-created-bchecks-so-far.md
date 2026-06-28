# The top 10 community-created BChecks, so far ...

Source: https://portswigger.net/blog/the-top-10-community-created-bchecks-so-far
Fetched: 2026-06-28T09:15:26.137729+00:00

The top 10 community-created BChecks, so far ...

Emma Stocks |

Monday, 24 July 2023 at 14:09 UTC

We recently launched BChecks, scripted scan checks that allow you to create customized scans without the hassle of learning advanced programming. We've shortlisted the top ten BChecks (so far) that have been submitted, and now we'd like you to vote for your favourite.

Each of the BChecks will be shared as an individual tweet - simply hit the "Like" button for the BCheck you like, or think you'd use, the most. If you'd prefer to vote on GitHub, just hit the link below for your chosen BCheck and give it a thumbs up directly in the repo.

We'll be counting any and all votes up to midnight on 31 July.

The shortlist

Each of the BChecks in the shortlist below have been selected based on community popularity, ease of use, frequency of activity on the repo, and creative ingenuity.

CVE-2023-25690 Apache mod_proxy CRLF Smuggling

View on the BChecks GitHub repo.

Author: p80n-sec

Description: Tests for CRLF based HTTP Request Smuggling/Splitting according to CVE-2023-25690.

Summary: This BCheck attempts to smuggle a payload to verify vulnerability to the Apache mod_proxy vulnerability CVE-2023-25690 which affects some mod_proxy configurations on Apache HTTP Server versions 2.4.0 through 2.4.55.

CVE-2020-10770 Keycloak request_uri SSRF

View on the BChecks GitHub repo.

Author: mrrootsec

Description: Keycloak allows an unauthenticated attacker to send arbitrary values in 'request_uri' parameter and interact with internal network resources which is otherwise not accessible externally. An attacker may use this feature to perform Blind SSRF (Server-side request forgery) attacks on the server.

Summary: This BCheck sends a payload that triggers CVE-2021-10774 which is a Server Side Request Forgery vulnerability and uses Collaborator to ascertain if it is vulnerable or not.

CVE-2021-27748 SSRF Websphere Portal.bcheck

View on the BChecks GitHub repo.

Author: Anof-cyber

Description: CVE-2021-27748.

Summary: This BCheck sends a payload that triggers CVE-2021-27748 which is a Server Side Request Forgery vulnerability and uses Collaborator to ascertain if it is vulnerable or not.

ntlm-authentication-discovery.bcheck

View on the BChecks GitHub repo.

Author: puzzlepeaches

Description: Detects NTLM authentication on non-standard directories.

Summary: This BCheck appends an HTTP header for each request in order to attempt to elicit a response which indicates NTLM authentication is present. If present it potentially provides an attack surface which via password spraying and similar a threat actor may gain further access.

CVE-2023-24488 - Citrix Gateway Open Redirect and XSS.bcheck

View on the BChecks GitHub repo.

Author: TheButcherRepository

Description: This rule checks if the remote host is vulnerable to CVE-2023-24488 - Citrix CRLF Injection / Reflected XSS.

Summary: This BCheck sends a payload which tests for presence of CVE-2021-27748 which is a CRLF injection vulnerability leading to reflected Cross Site Scripting through HTTP Response Splitting.

Nacos-default-password.bcheck

View on the BChecks GitHub repo.

Author: JaveleyQAQ

Description: Nacos Default Password.

Summary: This BCheck sends a payload attempting to authenticate with the default username and password. It then checks the response to see if authentication was successful or not.

exposed-prometheus-metrics.bcheck

View on the BChecks GitHub repo.

Author: nightshiba

Description: Prometheus Metrics Found.

Summary: This BCheck sends a payload which checks for the presence of a particular path which indicates Prometheus metrics.

are accessible. These metrics may leak sense information and thus should not be publicly available.

Javascript/jsMapFile.bcheck

View on the BChecks GitHub repo.

Author: TheButcherRepository

Description: This rule checks for the presence of indicators suggesting the availability of a JavaScript map file.

Summary: This BCheck checks for the presence of JavaScript map files. These map files if present help with recovering the original source code JavaScript which has been minified or similar.

CVE-2018-1000129 - Jolokia 137 - Cross-Site Scripting.bcheck

View on the BChecks GitHub repo.

Author: dbrwsky

Description: Jolokia 1.3.7 is vulnerable to cross-site scripting in the HTTP servlet and allows an attacker to execute malicious JavaScript in the victim's browser.

Summary: This BCheck sends a request which is a Cross Site Scripting payload within a set of SVG HTML tags to test for the presence of CVE-2018-1000129 which is reflected XSS.

exposed-swagger-ui.bcheck

View on the BChecks GitHub repo.

Author: genuinemoses

Description: Tests for an exposed SwaggerUI endpoint.

Summary: This BCheck checks for the presence and accessibility of SwaggerUI and OpenAPI endpoints. If publicly available they may leak sensitive information.

What happens next?

Voting will be open until midnight on 31 July. After that time, we'll count up all of the votes and select a winner - that contributor will win an exclusive interview with a member of the Burp Suite development team.

The creators of each of the BChecks in the shortlist above will be winning some exclusive swag - we'll be in touch with you all to get that organized. Massive thanks to everyone who has contributed a BCheck so far - it's been incredibly exciting to see the unique, creative, and genuinely useful applications of the functionality.

Inspired to create your own BCheck?

If the shortlist above has inspired you to create your own BCheck, simply follow the steps below to get started:

Read through the documentation to get the basics of the language, and learn how to create your own BCheck.

Define and create your BCheck.

Submit your pull request to the BChecks GitHub repo.

Emma Stocks

Latest Posts

Burp Extensibility 2026: Awards, Talks, and Highlights

19 June 2026

Burp Extensibility 2026: Awards, Talks, and Highlights

The beast needs a cage: What's next for AppSec post-Mythos

12 May 2026

The beast needs a cage: What's next for AppSec post-Mythos

3 ways custom scan checks turn practitioner knowledge into scalable automation

01 May 2026

3 ways custom scan checks turn practitioner knowledge into scalable automation

Senior pentesters have a deeply refined intuition about what is vulnerable in an environment. The problem? That expertise is often siloed with an individual and trapped in their notes or Python scripts.
