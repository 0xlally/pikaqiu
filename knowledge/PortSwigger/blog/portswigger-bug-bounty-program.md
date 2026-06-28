# PortSwigger bug bounty program

Source: https://portswigger.net/blog/portswigger-bug-bounty-program
Fetched: 2026-06-28T09:15:22.925995+00:00

PortSwigger bug bounty program

Dafydd Stuttard |

Wednesday, 30 November 2016 at 12:13 UTC

Today we are pleased to announce our bug bounty program. This covers:

Our website at https://portswigger.net

Burp Suite software (latest versions)

The program is managed on HackerOne, and all reports should be submitted through that platform.

Access the PortSwigger bug bounty program on HackerOne.

Visit HackerOne

Full details of the program policy are reproduced below. Please read the policy carefully and in full before carrying out any testing or submitting any reports.

Scope

Website: https://portswigger.net/

Software: Burp Suite Professional and Burp Suite Free Edition (latest versions)

Subdomains of portswigger.net like support.portswigger.net are strictly out of scope. Do not test these.

If you wish to test the Burp Collaborator functionality, please configure your own private Collaborator server and test that.

Vulnerabilities of interest

Here are some examples of vulnerabilities that we could consider to be valid, and rough guidelines as to what kind of payout you can expect:

Critical - $5000

SQL injection on portswigger.net

Remotely retrieving other users' Burp Collaborator interactions

High - $3000

Stored XSS on portswigger.net

File path traversal on portswigger.net

Complete authentication bypass on portswigger.net

A website accessed through Burp Suite can make Burp execute arbitrary code

Medium - $1000

A website accessed through Burp Suite can retrieve local files from the user's system

A website accessed through Burp Suite can extract data from Burp's sitemap

Exploitable reflected XSS on portswigger.net

CSRF on significant actions

Any medium severity issue involving unlikely user interaction - $350

Reflected XSS that is unexploitable due to CSP

A website scanned using Burp Suite can inject JavaScript into reports exported from the scanner as HTML

DLL hijacking on the Burp Suite installer, on fully patched Windows 7/8.1/10

Issues not of interest

The following are strictly forbidden and may result in you being barred from the program, the website, or both:

Denial of service attacks

Physical or social engineering attempts

Targeting subdomains of portswigger.net

Bruteforcing subdomains

Spamming orders

Unthrottled automated scanning - please throttle all tools to one request per second.

We are not interested in low severity, purely theoretical and best-practice issues. Here are some examples:

Denial of service vulnerabilities

Headers like Server/X-Powered-By disclosing version information

XSS issues in non-current browsers

window.opener related issues

Unvalidated reports from automated vulnerability scanners

CSRF with minimal security implications (logout, etc.)

Issues related to email spoofing (eg SPF/DMARC)

DNS issues

Content spoofing

Reports that state that software is out of date or vulnerable without a proof of concept

Missing autocomplete attributes

Missing cookie flags on non-security sensitive cookies

SSL/TLS scan reports (this means output from sites such as SSL Labs)

Caching issues

Concurrent sessions

HPKP / HSTS preloading

Implausible bruteforce attacks

There are a few known issues we consider to be low severity, but may fix eventually:

As customer numbers are emailed out in plaintext, users should be encouraged to regenerate them on first login.

Generating a new customer number should kill all associated sessions.

Invoices, quotations, and receipts can be accessed by anyone who is given the link. This is an intentional design decision to enable sharing (the ability to view someone's invoice without being given the link would be considered a serious vulnerability).

Some other caveats:

The Paypal price can be tampered with but underpayment will result in product non-delivery so this isn't a security issue.

We use Content-Security-Policy (CSP) site-wide. This means you will have a hard time doing alert(1). To maximize your payout, see if you can make a payload that will steal some sensitive information.

As the makers of Burp Suite, we can assure you that we have already scanned our website with it. Don't waste your bandwidth.

Extensions including those in the BApp Store are out of scope.

What constitutes a vulnerability in Burp Suite?

The system that Burp Suite runs on is trusted, and every system that can access the Proxy listener is trusted to access the data within Burp. Extensions, configuration files and project files are also trusted. Websites accessed through Burp are untrusted, so anything a website could do to read files off the user's computer, read data out of Burp Suite, or gain remote code execution would be considered a vulnerability. Also, any way to get someone else's Collaborator interactions would be considered a vulnerability. Burp doesn't enforce upstream SSL trust by design, so we're not currently concerned about issues like weak SSL ciphers that would be considered a vulnerability in a web browser. Detection of Burp usage, denial of service vulnerabilities, and license enforcement/obfuscation issues are all out of scope. Please refer to the payout guidelines for some example vulnerabilities.

Contact

If you have any questions, you can contact us at support@portswigger.net.

Good luck and have fun!

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
