# Professional 1.7.25

Source: https://portswigger.net/burp/releases/professional-1-7-25
Fetched: 2026-06-28T09:16:28.481864+00:00

This release adds a number of new scan checks based on our talk today at Black Hat, Cracking the lens: targeting HTTP's hidden attack surface.

The new scan checks use various techniques aimed at inducing vulnerable applications and infrastructure to route requests to a different destination. This can lead to serious attacks, for example SSRF against the application server itself or other infrastructure components. The research behind the new capabilities quickly netted us over $30,000 in bug bounty payouts, and demonstrates the huge power of OAST (out-of-band application security testing).

The novelty of the new checks lies not so much in the payloads themselves as where they are placed. The new scan checks send Collaborator-based payloads in the following locations:

The HTTP Request-Line (where the requested URL normally appears).

The server name specified in the SSL SNI extension.

The server specified in a CONNECT request.

The Host header.

Various other common and not-so-common request headers.

An example of a reported vulnerability is shown below. For full details of these and various other techniques, see today's blog post.
