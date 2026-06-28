# Professional 1.6.20

Source: https://portswigger.net/burp/releases/professional-1-6-20
Fetched: 2026-06-28T09:16:27.545353+00:00

This release updates the Scanner to find super-blind OS command injection vulnerabilities.

Previously, Burp has been able to report OS command injection using both blind and non-blind techniques:

Injecting commands to trigger a time delay in the response.

Injecting commands to echo a value in the response.

In many situations, OS command injection vulnerabilities cannot be found using either of these techniques, because no time delay can be triggered and command output is not echoed in responses. The new release makes use of Burp Collaborator to find more of these vulnerabilities. The Scanner now injects commands like:

nslookup xkll4ipqd9936ht84ku7hw47k.burpcollaborator.net

and verifies that a DNS lookup has been performed on the Burp Collaborator server.

At present, Burp still does not detect cases of injection that are long deferred after submission of the payload (e.g. occurring in an overnight batch job). Later in the Burp Collaborator development roadmap, Burp will also report vulnerabilities of this kind.

This release also fixes some bugs:

A bug in the Collaborator Server that could cause threads to become deadlocked when processing incoming HTTP requests that time out. It is recommended that users with private Collaborator Server deployments update to the new version.

Some issues affecting the new site map UI that was introduced in 1.6.19.

A bug in the interactive prompting for platform authentication.
