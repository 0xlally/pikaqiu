# Burp Extensibility 2026: Awards, Talks, and Highlights

Source: https://portswigger.net/blog/burp-extensibility-2026-awards-talks-and-highlights
Fetched: 2026-06-28T09:15:08.560925+00:00

Burp Extensibility 2026: Awards, Talks, and Highlights

Fran Hutchings |

Friday, 19 June 2026 at 12:18 UTC

The 2026 Burp Suite Extension Awards

Best Recon & Discovery

Best Auth & Access Control

Best Workflow & Manipulation

Best API & Specialist Testing

Hidden Gem

Most Nominated

The talks

Intro to Extensibility in Burp

Submitting extensions to the BApp Store

Writing your first Burp extension

Restoring Testability: Handling Complex Scenarios in Burp Suite with a Custom Extension

Swapper: A quick rundown

ByteBanter - LLM-driven Payload Generator for Burp Intruder

Extension in the loop: Developing Burp extensions with AI

Adventures in Bambda Automation with Claude Code

Build to learn: How PortSwigger uses Burp extensions to prototype ideas

Try it yourself

Get involved

Throughout May 2026 we ran Extensibility Month on the PortSwigger Discord server - a full month of talks, workshops, community sessions, and the Burp Extension Awards, decided by community vote.

The goal was to showcase the different ways people extend Burp, and highlight the work being shared across the community.

Extensibility in Burp means three things: extensions (BApps), Bambdas, and custom scan checks (BChecks). All three give you ways to tailor Burp to your workflow, whether that's automating something repetitive, adding a check the scanner doesn't have out of the box, or building something entirely new.

The 2026 Burp Suite Extension Awards

The talks highlight what's possible with Burp's extensibility features, but they only tell part of the story. Running alongside the sessions, the community nominated and voted for the extensions they find most useful in day-to-day testing.

More than 200 nominations were submitted for 46 extensions. Rather than ranking tools just by raw popularity, nominations were also scored on the quality of the reasoning behind them: specificity, real-world use cases, and technical insight.

Best Recon & Discovery

Shortlist: Param Miner, Sensitive Discoverer, Active Scan++, Backslash Powered Scanner, JS Miner, JS Link Finder, Firewall Ferret, GAP (Get All Parameters, Links, and Words), 403 Bypasser

Backslash Powered Scanner impressed with its philosophy: "Instead of looking for known issues, it looks for anomalous behaviour - that often hides known and unknown types of server-side injection vulnerabilities."

JS Miner drew some of the most vivid nominations in the competition: "I've pulled some really solid findings out of it - hidden endpoints buried in JS files that turned out to expose PII, secrets that were actually exploitable and ended up being critical severity, and in some cases straight up hardcoded credentials and tokens sitting there giving access to internal systems."

Best Auth & Access Control

Shortlist: Autorize, PwnFox For Chromium, JWT Editor, Auth Analyzer, SAML Raider, Burp Variables, Authentication Token Obtain and Replace, AuthMatrix

JWT Editor earned nominations for keeping everything in-tool: "Easy way to decode JWTs without relying on third-party websites or browser extensions. Automatic JWT discovery with a tab that shows the decoded JWT per request."

Auth Analyzer: "Saves time and nerves, allows doing comprehensive access control tests with multiple users at the same time."

Best Workflow & Manipulation

Shortlist: Highlighter And Extractor, CSTC, Modular HTTP Manipulator, Turbo Intruder, Hackvertor, Burpcord, Discord Rich Presence for Burp, Saver Logger, Logger++, Proxy Enriched Sequence Diagrams Exporter, Reshaper, Sheet Intruder, Burp Bounty, Scan Check Builder, Swapper, Piper, HTTP Request Smuggler, Taborator, WebSocket Turbo Intruder

Highlighter And Extractor was the single most-nominated extension in the entire competition with 18 votes. "Highlighter And Extractor acts like a smart filter, immediately drawing my eyes to the requests that matter most. It feels like having an extra pair of eyes watching the traffic for me. The rule-based automation - the ability to write custom regex rules and have Burp automatically highlight and extract data - is a game-changer."

Hackvertor got technically specific nominations: "The auto-update tags. Being able to recalculate an HMAC signature, timestamp or hash automatically on every request makes attacking signed APIs and anti-replay mechanisms trivial. Combined with custom tags - JS, Python, Java, Groovy - it's endlessly extensible."

Best API & Specialist Testing

Shortlist: Postman Burp Importer, Burp AI Agent, Intigriti Quick Scope, InQL - GraphQL Scanner, ByteBanter, AI Intruder Payload Generator, MCP Server, SSL Scanner, Wsdler, Java Deserialization Scanner, Brida, Burp to Frida Bridge, J2EEScan, Upload Scanner, Freddy, Deserialization Bug Finder.

Hidden Gem

This category focused on extensions with three or fewer nominations. Winners were ranked on average quality score rather than total nominations, highlighting tools that may be less widely known but are highly valued by the people who use them.

Most Nominated

Runners-up: Postman Burp Importer and Burp AI Agent (17 votes each), CSTC, Modular HTTP Manipulator (16 votes), Intigriti Quick Scope (13 votes).

The talks

Intro to Extensibility in Burp

We kicked things off with an overview of the full extensibility landscape - what's available across extensions, Bambdas, and BChecks, and when you'd reach for each one. The goal was to give everyone a shared foundation before the more specialized sessions that followed.

Submitting extensions to the BApp Store

This session walked through what it takes to get an extension listed on the BApp Store: the submission criteria, what PortSwigger looks for during review, and the benefits of having your extension publicly available to the community.

Writing your first Burp extension

A hands-on workshop covering the basics of building a Burp extension with the Montoya API - from setting up a project to writing and loading your first extension. A practical starting point for anyone who's been meaning to give it a go.

Restoring Testability: Handling Complex Scenarios in Burp Suite with a Custom Extension

Federico Dotta (Burp Ambassador, Research Lead at HN Security) walked through a real-world scenario - an application with end-to-end encryption on top of TLS - and showed how to build a Burp extension that restores full testability: decrypting traffic for manual testing, and making Intruder and Scanner work as if the encryption wasn't there. He covered two different architectural approaches with different trade-offs, and demonstrated how the same extension logic can be used to pass traffic through external tools like SQLmap. The extension code and demo application are available on GitHub.

Swapper: A quick rundown

Dave Blandford demonstrated Swapper, his extension that automates match-and-replace of tokens, CSRF values, and authentication headers across Burp tools. Swapper takes a format-agnostic, regex-only approach, which makes it work cleanly across XML, JSON, and anything else. Dave walked through setting up response and request regexes, the auto-refresh feature for short-lived tokens, and a live demo against a local Juice Shop instance.

ByteBanter - LLM-driven Payload Generator for Burp Intruder

Andrea Braschi from Anvil Secure presented ByteBanter, AI Intruder Payload Generator, an extension that integrates multiple LLM engines - including Burp AI, Ollama, OpenAI-compatible APIs, and Anthropic - directly into Intruder, enabling context-aware, stateful payload generation for testing LLM applications and guardrails. Andrea demonstrated the second-generation architecture, the new automated success verification feature, and a live demo using ByteBanter to extract a password from Lakera Gandalf.

Extension in the loop: Developing Burp extensions with AI

Zak Fedotkin (PortSwigger Security Researcher) showed how AI code agents like Claude Code can become part of the Burp extension development workflow. The session covered the core problem: Claude can generate extension code, but without access to a real Burp instance, it can't run or verify it. Zak's solution, "extension in the loop", is a test harness that compiles the generated extension, loads it into Burp, runs it against real inputs, reads back the stack traces, and feeds them to the agent to fix. The result is a tight feedback loop that iterates automatically until the extension works. The framework is on GitHub.

Adventures in Bambda Automation with Claude Code

Tib3rius (Burp Ambassador) documented his experiments building autoBambda - a Claude Code project that automates the entire Bambda development loop: writing the Java body, compiling it against a stub Montoya API, running test harnesses with fake requests and responses, validating false positive behaviour, and packaging the result as a YAML file ready to import into Burp. The autoBambda repo is on GitHub and contributions are welcome.

Build to learn: How PortSwigger uses Burp extensions to prototype ideas

Tom SL (PortSwigger Product Engineer) gave a behind-the-scenes look at how the team uses extensions to test ideas before deciding whether to build them into the product. He walked through three real internal extension experiments with three different outcomes: ReportLM, an AI report-writing extension that stayed as a BApp because it worked but didn't need to be native; Co Organizer, an internal prototype that was never released but directly informed the Collections feature in Organizer; and an in-progress MCP Server Scanner being built by a colleague to explore a specialist area the Scanner doesn't yet cover. The takeaway: don't wait for a perfect plan. Build the smallest useful version, get it in front of people, and let the feedback guide you.

Try it yourself

If any of the talks caught your attention, the recordings are available in the #event-enthusiast channel on the Discord server. The extensions featured - ByteBanter, AI Intruder Payload Generator, Swapper, and all the Award winners - are on the BApp Store.

If you've been thinking about experimenting with Bambdas, BChecks, or extensions, there are now more resources available than ever. The Montoya API documentation, community repositories, session recordings, and Discord channels provide plenty of examples to build from, whether you're automating a workflow or exploring a new idea.

The community Bambda repository on GitHub is a good place to see what others have built and to submit your own.

Get involved

One of the recurring themes throughout the month was that many of the most useful ideas start small: a custom scan check to solve a specific problem, a Bambda to automate a repetitive task, or an extension built to explore a new testing technique. The talks and award nominations showed how much practical knowledge is being shared through the Burp community, and how often those ideas end up helping other testers solve similar problems.

If you have an extension, a Bambda workflow, or a technique you'd like to share, the Discord server is the place to do it. Community talks, demos, and workshops remain one of the best ways to exchange ideas and help others get more out of Burp.

If you'd like to run a session, whether that's a talk, workshop, or demo, share your idea in the #extensions, #bchecks, or #bambdas channel, or raise a #modmail.

Join the PortSwigger Discord server to find the recordings, the community extension channels, and the next round of events.

Fran Hutchings

Latest Posts

The beast needs a cage: What's next for AppSec post-Mythos

12 May 2026

The beast needs a cage: What's next for AppSec post-Mythos

3 ways custom scan checks turn practitioner knowledge into scalable automation

01 May 2026

3 ways custom scan checks turn practitioner knowledge into scalable automation

Senior pentesters have a deeply refined intuition about what is vulnerable in an environment. The problem? That expertise is often siloed with an individual and trapped in their notes or Python scripts.

28 April 2026
