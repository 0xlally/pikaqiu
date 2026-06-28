# Hacking without credentials

Source: https://portswigger.net/blog/hacking-without-credentials
Fetched: 2026-06-28T09:15:16.160086+00:00

Hacking without credentials

Dafydd Stuttard |

Monday, 23 July 2007 at 08:18 UTC

Authentication

Pen Testing

It is common to be faced with a web application where you have no credentials to log in. Very often, the application contains a wealth of functionality that can be accessed without authentication and which you can start working on to find a way in. Typically, the most promising initial targets are the more peripheral functions supporting the authentication logic, like user registration, password change and account recovery.

But occasionally you will face a narrower challenge. Suppose the web root of the server returns a simple login form, with no other functions and no links anywhere else. You can try to guess a username and password, but is that all?

Here are just a few of the things to think about in this restricted situation:

Looking for names, email addresses and other information in the HTML source.

Fingerprinting the web server software, application platform and any other identifiable technologies in use, and researching these for vulnerabilities.

Enumerating the content that is currently hidden, by brute forcing file and directory names, running Nikto, etc., and checking whether the content discovered is properly access controlled.

Checking search engines and Internet archives for references to the target.

Tampering with any hidden parameters and cookies in the login request that may affect server-side logic.

Checking for any disabled form elements that may still be processed if you re-enable them.

Adding common debug parameters (like test=true) to your request.

Inspecting the ASP.NET ViewState (if present).

Testing for username enumeration via informative failed login messages or other differences.

Testing susceptibility to brute force attacks.

If the application issues session tokens prior to login, testing these for predictability.

Testing all request parameters and headers for common code-level flaws like SQL injection, XSS, script inclusion, etc.

Probing for logic flaws within the login function, by omitting parameters, interfering with the request sequence if multi-stage, etc.

If the application is hosted in a shared environment, looking for co-hosted applications that you may be able to leverage to attack your target.

Any one of these attacks might give you a sufficient foot in the door to get past the login and into the protected functionality behind it. If they do not, then the login mechanism is a lot more robust than most are, and it is probably time to try to get hold of credentials, or move on to another target.

Authentication

Pen Testing

Dafydd Stuttard

@DafyddStuttard

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
