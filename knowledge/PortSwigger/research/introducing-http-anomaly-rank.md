# Introducing HTTP Anomaly Rank

Source: https://portswigger.net/research/introducing-http-anomaly-rank
Fetched: 2026-06-28T09:17:26.917105+00:00

Introducing HTTP Anomaly Rank

James Kettle

Director of Research

@albinowax

Published: Tuesday, 11 November 2025 at 14:41 UTC

Updated: Tuesday, 11 November 2025 at 14:41 UTC

HTTP Anomaly Rank

If you've ever used Burp Intruder or Turbo Intruder, you'll be familiar with the ritual of manually digging through thousands of responses by repeatedly sorting the table via length, status code, etc. I've developed an algorithm called HTTP Anomaly Rank which can efficiently pick out the most interesting responses for you.

HTTP Anomaly Rank is now integrated into Turbo Intruder and automatically places the most anomalous findings at the top of the results table without you needing to lift a finger.

We've also integrated this algorithm into Burp Suite's API in release 2025.10, so you can easily use it in your own tools. Since it can efficiently sift through massive result sets, it's particularly useful for anyone who wants to build AI based features.

In this post I'll explain how the algorithm works in depth but first, here's a quick demo:

HTTP Anomaly Rank

HTTP Anomaly Rank evolved from the diffing logic I developed during my Backslash Powered Scanner: Automating Human Intuition research back in 2016. I built Backslash Powered Scanner to discover unknown injection vulnerability classes by recognising subtle differences in responses to payload pairs such as " vs ". Accurately diffing HTTP responses is a notoriously difficult problem as they're often very noisy, but I eventually found a reliable approach based on calculating a large number of response attributes (think status code, line count, exact byte sequence...), identifying which ones are stable, and using these for response comparison. This let me answer the question "Are the responses to these two payloads consistently different", and automate discovery of some really nice vulnerabilities. Check out the whitepaper and presentation for the full details.

HTTP Anomaly Rank scores every response based on how different it is from the others. First, it calculates a weight for every attribute based on how stable it is.

Payload

Status

Content-Type

Word-count

CRC32

administrator

403

text/html

812

d753916d

admin

403

text/html

812

5129f3bd

sales

503

text/html

97

710639db

accounting

200

text/html

812

3978f20f

ADMIN

403

text/html

811

9fa1cbc1

root

503

text/html

97

27df2486

test

403

text/html

812

e45449e7

For example, consider the response set above.

Status only has two unique values so it gets a high weighting.

Content-Type never changes so it's useless

CRC32 is unique on every response so it's useless (perhaps the username is reflected)

Word-count has three unique values so it's useful but weighted lower than status

The algorithm then looks at every response, and assigns it a score based on how unique the attribute values seen on that response are, combined with how unique it is. In this example, ADMIN ends up with the highest score because it has a unique word-count.

This approach means it can detect and flag responses with tiny discrepancies, even when the overall response content is very noisy - check the video above for an example.

The score increases in accuracy as we collect more responses. The calculation is quite computationally heavy but the algorithmic complexity is O(N) so it scales well. In Turbo Intruder, I made the score only get calculated when the attack is completed to minimise wasted CPU cycles.

Turbo Intruder Integration

Part of my vision for Turbo Intruder is to require as few user clicks as possible. To help achieve this, it will now automatically sort the results table by the anomaly rank column when the attack completes. Hopefully this strategy works for you but if not, you can override it and automatically sort by any column of your choice using table.setSortOrder()

I'm looking forward to announcing some more quality of life updates for Turbo Intruder soon!

If you see the "Anomaly Rank" column but it's always set to 0, that means you need to update Burp Suite. This feature is available in 2025.10 and later.

Let me know how you find it, and if you'd like this feature in Burp Intruder too.

Enjoy!

turbo intruder

Back to all articles

Related Research

Cracking reCAPTCHA, Turbo Intruder style

20 November 2019

Cracking reCAPTCHA, Turbo Intruder style

Turbo Intruder: Embracing the billion-request attack

25 January 2019

Turbo Intruder: Embracing the billion-request attack
