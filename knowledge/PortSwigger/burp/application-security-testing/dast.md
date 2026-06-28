# Dynamic application security testing (DAST)

Source: https://portswigger.net/burp/application-security-testing/dast
Fetched: 2026-06-28T09:15:29.330119+00:00

Dynamic application security testing (DAST)

What is DAST security testing?

Dynamic application security testing (DAST) tests security from the outside of a web app. A good analogy would be testing the security of a bank vault by attacking it. DAST necessitates that the security tester has no knowledge of an application's internals. This is called a "black box" testing method - because the tester can't see inside the metaphorical "box". Its aim is to simulate a real attack.

Burp Suite was born out of the DAST mindset. Nowadays it can augment and improve its scans with other testing methods, but it's still a black box tool at heart.

Is DAST an automated or manual methodology?

The answer is "both". The automated scanner at the heart of Burp Suite, for instance, is rooted in DAST. But manual penetration testing is also (generally) DAST - and requires the kind of lateral thinking only a human is capable of. Large parts of it simply can't be automated.

So DAST is broad enough to include both automated and manual techniques. It only requires that you don't have insider knowledge of the systems you're testing.

How does dynamic security testing work?

Automated DAST

As we know, the concept behind DAST is that it mimics a real attack. And like a bank robber, the first thing a real cyber attacker will do is case the premises. Burp Suite's scanner simulates this by "crawling" the web application you're looking at.

A crawler is a type of bot that can automatically visit and log each page of a web application. Armed with this knowledge, it can then create a map. Building a crawler is actually a lot more complicated than it sounds, given the dynamic and volatile nature of many modern web apps.

Next, in the case of Burp Suite, the software would audit the app for vulnerabilities. This could involve anything from using brute force code injection techniques like "fuzzing", to searching for instances where user login details are handled in an unsafe manner.

Burp Suite's automated scanner is capable of detecting a long list of security vulnerabilities - many instances of which wouldn't be reported by conventional DAST alone. These augmented capabilities come thanks to input from IAST (interactive application security testing) and OAST (out-of-band application security testing) techniques.

Where an organization manages many web applications, or where developers are using a DevSecOps approach, automated DAST scanning will often be carried out continuously. Burp Suite DAST is designed specifically with enterprise security use-cases in mind - integrating seamlessly with development software and providing extreme scalability.

Manual DAST

No automated vulnerability scanner will pick up every bug. While automated software saves penetration testers and bug bounty hunters a great deal of time, there are certain situations where human creativity and lateral thinking is irreplaceable.

Often, a tester will use an automated DAST solution first, to harvest "low-hanging fruit". This approach frees up extra time for them to then work on more interesting vulnerabilities. This is why, in addition to Burp Scanner, Burp Suite Professional also includes a powerful intercepting proxy tailored to the needs of manual web security testers.

An intercepting proxy is a fairly simple concept. In the case of Burp Suite, it entails a piece of software that intercepts all HTTP traffic between the tester's browser and their target web application. Burp Suite will even do this for HTTPS (encrypted) traffic. The ability to read all communication sent between a web app and your browser is priceless in the DAST context.

Using the intercepting proxy approach, a tester can change the response that is sent to a server by their browser - opening up a wealth of opportunity for exploring vulnerabilities. This is one reason Burp Suite Pro has gained its reputation as the ethical hacker's Swiss Army knife and become industry standard pentesting software.

The advantages of a DAST approach

Accuracy

The DAST concept is advantageous in many ways - and is often more practical than alternate "white box" methods like SAST (static application security testing). SAST investigates an app's source code to look for bugs - and while this is a great idea in theory, in practice it tends to report many false positives. DAST doesn't suffer from this tendency.

It's not that DAST will never report a false positive - because this does happen from time to time. But, compared to SAST, the amount returned is negligible. In terms of false positives then, it's a resounding win for DAST. And false positives waste both time and money.

Adaptability

DAST also compares favorably with SAST where adaptability is concerned. SAST suffers in this regard because it relies on being able to read a given programming language in order to function. But because DAST is language-agnostic by design, it doesn't require multiple implementations for different types of code like SAST does.

Modern web apps are complex and tend to use multiple frameworks and layers of abstraction. An agnostic approach is a huge advantage in this context. This is not to mention that near constant updates mean programming languages often change. With DAST, you know that your scanner is always prepared for this. One size quite simply fits all.

DAST's agnostic approach will also pay dividends if you have a number of web apps to scan. Because of its scalability, Burp Suite DAST is used by organizations with tens of thousands of live apps. These users are then free to develop apps in more or less any language they choose.

Augmentable testing

This is not to say that SAST is useless: far from it. But in real-world scenarios, we believe that DAST is the superior base methodology. And DAST's superiority is only enhanced by the additional testing methods included in Burp Suite Professional and Burp Suite DAST.

See below for a discussion of how methods such as OAST help to negate some of the drawbacks inherent in the DAST concept.

Are there any drawbacks to a DAST methodology?

Blind and asynchronous bugs

No testing method is perfect, and there are areas where DAST's performance is less than ideal. Used in isolation, it would miss many blind and/or asynchronous bugs, for instance. These involve situations where an application is vulnerable to an exploit but gives no perceivably different response when an attack is sent.

But by deploying DAST in conjunction with OAST, this problem is largely solved. OAST was a technique pioneered by PortSwigger with Burp Collaborator - and is fully integrated into the vulnerability scanner package that powers Burp Suite.

Want to learn more about web application security testing?

Non-exposed inputs

A similar situation exists where non-exposed application inputs are concerned. DAST will not identify such vulnerabilities - because it only sees things from outside the web app. Of course, a real attacker would be in the same position here.

And in Burp Suite's case, the shortcoming can be mitigated somewhat by using extensions. Param Miner, for instance, can enhance Burp Suite Professional's brute force capabilities significantly where non-exposed inputs are concerned. But this is also an area where the intuition of an experienced penetration tester is invaluable in inferring how an app works.

Hard-to-execute paths

In certain cases where an input path is hard-to-execute, DAST may miss some bugs. An example would be an advanced exploit relying on a combination of multiple input variables in order to work. While a SAST approach should find this, as might a good manual pentester, a DAST scan alone would not.

The trade-off here is that while SAST may report the bug, it would often be returned as part of a long list of false positives. This then requires a tester to manually review the code in order to find the real vulnerabilities. This is far from ideal. Reviewing code is expensive, and in practice you may find that the regular alerts given by SAST tools are simply ignored.

Is DAST the right methodology for you?

PortSwigger are the makers of Burp Suite, which is a DAST tool. We think it's the best solution out there for many use cases - and it includes the world's most widely used vulnerability scanner. But is it right for you?

Firstly, we should point out that no automated method can completely replace manual penetration testing. There are vulnerabilities that it takes a human to find. Consequently, cybersecurity compliance standards often include a requirement for both penetration testing and vulnerability scanning.

An automated DAST scanner like Burp Suite can help you protect your online property whether you manage many apps, or just a few. It can do this from the development stage, right up into deployment and beyond. And if you're a penetration tester, you'll love how Burp Suite Pro's advanced manual tooling could help you achieve new heights.

Find and fix vulnerabilities early with our DAST scanners

Burp Suite DAST

Automate your scanning at scale with Burp Suite DAST, the enterprise-enabled dynamic web vulnerability scanner.

We use as a DAST scanner outside the CI/CD pipeline. I like the outsider point of view it provides. I also like the scalability that DAST allows.

Source: TechValidate survey of PortSwigger customers

See more customer stories

Application Security Manager

Large Enterprise Pharmaceuticals Company

Learn more

Find out what Burp Suite could do for you, according to your particular use case:

Development teams

Organizations

Penetration testers
