# Professional / Community 1.7.20

Source: https://portswigger.net/burp/releases/professional-community-1-7-20
Fetched: 2026-06-28T09:16:31.398775+00:00

This release considerably enhances the detection of blind injection vulnerabilities based on response diffing. Various Burp Scanner checks involve sending pairs of payloads (such as or 1=1 and or 1=2) and looking for a systematic difference in the resulting responses. Previously, Burp used a fuzzy diffing algorithm that analyzed the whole content of responses. This approach has various limitations that can lead to false negatives, such as:

Small variations that are insignificant in the context of the whole response content are liable not to trigger the fuzzy diffing threshold, despite being highly significant when their precise syntactic context is taken into account.

Situations where application responses vary due to non-deterministic or unrelated factors can lead to large variations that trigger the fuzzy diffing threshold for all payloads, thereby masking other variations that depend systematically on the supplied payload.

Burp now uses a more granular diffing logic that takes into account all of the response attributes that were previously exposed in the analyzeResponseVariations API and used in our backslash powered scanning research. Variations are separately analyzed for attributes such as tag names, HTTP status code, line count, HTML comments, and many others. This granularity avoids the limitations described above and dramatically improves the accuracy of blind scan checks in many cases.

Additionally, several of the payloads used in diff-based scan checks have been enhanced to ensure that observed differences are indeed the result of injecting into the intended technology, rather than other input-dependent logic. For example, some web application firewalls (lamely) filter input that matches or N=N and cause a different response than is observed for or N=M. Burp's payloads are now intelligent enough to avoid false positives in situations like this.

The scan checks whose logic has improved include: SQL injection, LDAP injection, XPath injection, file path manipulation, User-agent-dependent response, X-forwarded-for-dependent response, and Referer-dependent-response.

We welcome feedback about the real-world performance of the new scanning logic, particularly in relation to false negatives or positives for diff-based injection issues.

Burp Proxy's generated per-host SSL certificates now include the site's commonName in the subjectAlternativeName extension. Apparently fallback to the commonName was deprecated by RFC2818 (in 2000), and browsers have recently decided to implement this.

Burp Collaborator server now has a configurable logging function that can be used for diagnostic purposes. See the Collaborator configuration file documentation for more details.

Various other minor fixes and enhancements have been made.
