# Free: Dastardly from Burp Suite

Source: https://portswigger.net/blog/free-dastardly-from-burp-suite
Fetched: 2026-06-28T09:15:15.303325+00:00

Free: Dastardly from Burp Suite

Matt Atkinson |

Thursday, 27 October 2022 at 13:03 UTC

burp

Secure Development

Introducing Dastardly - a free, lightweight web application security scanner for your CI/CD pipeline, from the makers of Burp Suite.

Secure web development ain't easy

Ensuring your code is written securely can be a bit of a headache. Most of us know about the risks of SQL injection by now, but what about vulnerabilities like Cross-site scripting (XSS) or CORS misconfigurations?

There are hundreds of static (SAST) code analysis tools around, but many are prone to noise - distracting you with a seemingly endless stream of false positives. In short, these tools often get ignored at best.

Dastardly is different

Dastardly's scanner produces very little noise, thanks to its dynamic (DAST) methodology. It looks at your application from the outside in - just like a real attacker. So if it sees a vulnerability, you can be pretty sure it's real. And to do this, it uses a stripped-down version of the scanner used by Burp Suite - the world's leading toolkit for web security testing.

In the past, dynamic analysis has been difficult to fit into CI/CD - being slower than static analysis. But Dastardly scans complete in ten minutes or less - giving you fast feedback on seven security issues you should be aware of. This gives you the ability to fix actual security issues there and then, without any painful context-switching or false positives.

Get scanning!

That's really all there is to it - Dastardly is fast, accurate, and completely free of charge.

And we've made it easy to get it running in your CI/CD pipeline. Check out the Dastardly documentation for more details.

Like what you see? Follow us on Twitter for all the latest Dastardly / Burp Suite news.

burp

Secure Development

Matt Atkinson

@mattatkinson42

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
