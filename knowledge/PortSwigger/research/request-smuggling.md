# HTTP Request Smuggling Research

Source: https://portswigger.net/research/request-smuggling
Fetched: 2026-06-28T09:17:28.438832+00:00

HTTP Request Smuggling Research

HTTP Request Smuggling is an advanced technique for attacking websites that have one or more front-end servers. An attack is launched by sending ambiguous HTTP requests that get interpreted as different lengths by the servers. This causes them to desynchronize, and merge requests and responses from attackers and legitimate users.

This can ultimately lead to a wide range of serious effects. These include letting attackers steal plaintext passwords, and poison caches to persistently compromise critical functionality like login pages. It was first documented in 2004, but largely forgotten until we revisited it in 2019. We built on the existing request smuggling research with modern techniques and tooling, earning six figures in bug bounties along the way.

HTTP Request Smuggling Research

We presented HTTP Desync Attacks: Request Smuggling Reborn at both Black Hat USA and DEF CON. This repopularized the technique, and has since led to a wave of discoveries and patches.

In subsequent years we presented HTTP/2: The Sequel is Always Worse followed by Browser-Powered Desync Attacks. The next major installment will be HTTP/1.1 Must Die! The Desync Endgame.

We also released a collection of interactive labs as part of our Web Security Academy, so you can practise applying the techniques to real systems.

HTTP Request Smuggling Research Articles
