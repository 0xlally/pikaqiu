# Repeater Strike: manual testing, amplified

Source: https://portswigger.net/research/repeater-strike-manual-testing-amplified
Fetched: 2026-06-28T09:17:28.365224+00:00

Repeater Strike: manual testing, amplified

Gareth Heyes

Researcher

@garethheyes

Published: Tuesday, 15 July 2025 at 13:46 UTC

Updated: Tuesday, 15 July 2025 at 13:46 UTC

Manual testing doesn't have to be repetitive. In this post, we're introducing Repeater Strike - a new AI-powered Burp Suite extension designed to automate the hunt for IDOR and similar vulnerabilities. By analyzing your Repeater traffic, Repeater Strike generates smart regular expressions based on the requests and responses you're testing. It then applies these regexes across your proxy history to uncover related issues, letting you turn a single vulnerability into a broader set of actionable findings with minimal effort.

At PortSwigger research we're experimenting with AI to produce semi-automated tools that help enhance your security testing. One of the ideas I had was to use AI to find variations and so I built

Shadow Repeater

. This turned out to be quite cool and it fit nicely into what AI is good at. I wondered if I could do more than just generate variations. I had a thought of taking what you do in Repeater and scanning your proxy history to discover more of it.

I experimented with three different methods of finding the vulnerability: Java compilation, regular expression and differential based analysis. I spent some time generating scan checks using a dynamically generated Java class but soon realised that you use multiple regular expressions to accomplish the same thing. I turned my focus to regexes instead.

The first step was to use the AI to identify the vulnerability and produce a JSON object to help the next agent:

"param": {

"values": ["wiener"],

"name": "id",

"type": "URL",

"vulnerabilityClass": "IDOR"

}

The AI correctly identified what you may be testing for and noticed that based on the requests you sent to it you are testing the URL with a parameter called id. The initial probe was to probe for wiener 😂. The AI then takes this probe and tries to find something uniquely identifiable in the response:

"responseRegexes": [[

"Your username is: wiener",

"Your API Key is: [A-Za-z0-9]{32}",

"<a href=\"/my-account\\?id=wiener\">My account<\/a>"

]]

Pretty cool the AI has identified the username reflection and the API key and I told it to match the structure of the data so it can find more rather than the specific key. Now it tries to reproduce the finding by making the request with the probe before it generates the new Strike Rule. If the replication was successful, Repeater Strike then prompts you for a Strike Rule name.

The next step is to mutate the probes and response regexes. This wouldn't have been possible a year ago but now the AI models are super smart. They can take the data and mutate it very cleverly. It's worth noting that I haven't told it specific instructions about the vulnerability it can work it out from the JSON structure I gave to it:

{

"mutatedProbesToUse": [

"admin",

"testuser",

"anonymous",

"user123",

...

],

"mutatedResponsesRegexes": [

[

"Your username is: admin",

"Your API Key is: [A-Za-z0-9]{32}",

"<a href=\"/my-account\\?id=admin\">My account<\/a>"

],

[

"Your username is: testuser",

"Your API Key is: [A-Za-z0-9]{32}",

"<a href=\"/my-account\\?id=testuser\">My account<\/a>"

],

[

"Your username is: anonymous",

"Your API Key is: [A-Za-z0-9]{32}",

"<a href=\"/my-account\\?id=anonymous\">My account<\/a>"

],

[

"Your username is: user123",

"Your API Key is: [A-Za-z0-9]{32}",

"<a href=\"/my-account\\?id=user123\">My account<\/a>"

],

...

}

Once the AI has mutated the probes and regexes, it can then scan your proxy history looking for this behaviour. You can even set up Repeater Strike to dynamically create Strike Rules on every Repeater request sent. You might expect this to burn through a load of AI tokens but actually to create this particular Strike Rule it only cost me 61 tokens and once the rule has been generated it uses no further tokens!

If the AI generated regular expressions failed, no problem I created a Strike Rule editor that lets you edit the generated Strike Rule, hit save and then scan your proxy history all without further tokens.

Challenges

During development, I ran into several challenges. One of the major issues was handling large responses - while the AI could interpret smaller ones effectively, it struggled with longer responses from sites like Facebook. I initially truncated the data, but this led to important context being lost.

Another hurdle was inconsistent output from the AI. For example, when generating regular expressions, it sometimes failed to properly escape metacharacters, leading to runtime errors. A workaround was to programmatically escape these characters when exceptions occurred.

The broader concept also proved difficult to generalise too. While the system could detect issues like IDOR on specific sites, it was hard to create regular expression patterns flexible enough to work across different sites without being too site-specific.

I experimented with response diffing as a way to extract meaningful information by filtering out noise - such as insignificant headers - and focusing only on the parts that change.

In the end I ran out of time to fully solve it - but maybe you can.

Can you find an elegant solution to reliably isolate meaningful UI changes and feed them to the AI? Let's push this further.

I hope I've inspired you to

create your own Burp AI extensions.

It really is super easy to get started. If you need help on how to use Repeater Strike please

consult the readme

.

Please note to use this extension you need to be on the Early Adopter channel. It is currently considered experimental and is far from a finished product.

AI

Burp Suite

burp extender

Hacking Tools

research tools

Back to all articles

Related Research

Document My Pentest: you hack, the AI writes it up!

23 April 2025

Document My Pentest: you hack, the AI writes it up!

Shadow Repeater

AI-enhanced manual testing

20 February 2025

Shadow Repeater

AI-enhanced manual testing

Introducing SignSaboteur: forge signed web tokens with ease

22 May 2024

Introducing SignSaboteur: forge signed web tokens with ease

Using form hijacking to bypass CSP

05 March 2024

Using form hijacking to bypass CSP
