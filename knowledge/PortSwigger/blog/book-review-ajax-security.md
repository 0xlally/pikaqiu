# Book review: Ajax Security

Source: https://portswigger.net/blog/book-review-ajax-security
Fetched: 2026-06-28T09:15:07.437864+00:00

Book review: Ajax Security

Dafydd Stuttard |

Friday, 14 March 2008 at 08:10 UTC

ajax

SQL Injection

books

Ajax Security, by Billy Hoffman and Bryan Sullivan, has several positive points to recommend it, and also some important caveats of which the reader should be aware.

The book is well written throughout, and clearly explains the technical subject matter with which it deals. The authors have a gift for imaginative and entertaining narrative, which is most evident in the accounts of hypothetical attacks against web applications that are described at various points. In the main, the book is well edited and contains a minimum of typos and other editorial glitches that are often the bane of technical computing books.

Several sections within the book stand out as being useful and informative. Chapter 8 discusses client-side storage mechanisms: notably Flash's Local Shared Objects, Mozilla's sessionStorage, and Internet Explorer's userData. Chapter 9 provides a useful overview of the Google Gears framework for offline Ajax applications, and Chapter 11 covers mashup applications. These sections will be of benefit even to many readers who already have a good grounding in web application security.

I have two broad complaints about the book. The first, and less significant, concerns the authors' determination to argue that Ajax represents a "fundamental shift" in web application architecture (p24), and that Ajax applications are "susceptible to far more dangerous security vulnerabilities than conventional" applications (back cover). Any author can be forgiven for stating that their subject is terribly important. But this polemical thrust appears in every chapter of the book, and frequently distracts from the interesting content which it punctuates. The argument is also ultimately unsuccessful in supporting its claims.

The authors' case boils down to two points. Firstly, Ajax applications contain more functionality than their pre-Ajax counterparts, other things being equal; more client-side wizardry requires more server-side code and interfaces to support it; and creating more functionality presents more opportunities to introduce vulnerabilities. Secondly, having more client-side code provides more information and clues about server-side functionality that can be attacked.

The observations about functional complexity are perfectly valid, but the differences identified between Ajax and conventional web applications are ones of degree, not of kind. For the most part, an Ajax application is inherently more vulnerable than a corresponding conventional application in the same way that any large and complex application is inherently more vulnerable than a simple one - it has more attack surface. This reading is borne out by the specific attacks discussed throughout the book. With the notable exception of JSON hijacking (which is unique to Ajax applications), all of the vulnerabilities described involve "old school" bugs like SQL injection and broken access controls, which can affect any kind of web application. What the authors' argument really demonstrates is that Ajax has led to insecurity because it provides developers with more opportunities to make familiar mistakes.

The argument concerning the greater transparency of Ajax applications is less convincing. The authors assert that "much of traditional web application security" relies on users being unable to see server-side code (p174) and that increased transparency is "probably the most significant and most dangerous" feature of Ajax applications (p391). It is no doubt true that if an application's functionality is insecure, then greater knowledge of that functionality can help an attacker. But, as the authors themselves acknowledge, applications cannot rely for their security on the obscurity of how their functionality works (p172). I would argue that developers should actively assume that an attacker fully understands how their application works, and create functionality that is robust against fully-informed attacks. All the authors' argument really shows is that an insecure Ajax application may leave more clues about where the holes are than a corresponding conventional application. Again, the conclusion that Ajax applications face "far more dangerous security vulnerabilities" is not supported.

My second broad complaint about Ajax Security, which is more significant, concerns the surprising number of technical errors in the advice that is offered to developers to avoid security vulnerabilities in their applications. Here are the most serious instances of defective advice within the book:

SQL injection. The main discussion of this topic (p102 onwards) begins with a demonstration that database stored procedures are not a panacea, with an example of a SQL injection vulnerability inside a stored procedure. The proposed alternative is input validation, which is described as a "general purpose strategy that solves all of these issues" (p105). After a few pages explaining how to do whitelist-based validation using regular expressions, the elephant in the corner speaks up: what about apostrophes? Of course, applications must often accept input which contains apostrophes and other syntax that can be used to perform SQL injection. The authors' answer is as follows: "The solution is to continue to refine the whitelist pattern. Consider limiting the number of words (the number of groups of alphanumeric characters delimited by whitespace characters). Consider limiting the number of apostrophes allowed". This is dangerous advice and would leave an application which followed it open to attack. In reality, arbitrarily complex SQL injection attacks can be performed using only a single apostrophe and no whitespace whatsoever. If you don't know how, consult Chapter 9 of WAHH for the full explanation.

It is undeniable that input validation is a key defence which applications should implement at every opportunity, but it has its limitations. My favourite example of this is close to home: a blog about web application security. The blogging application must allow the author and commenters to submit free-form input containing all kinds of potentially malicious syntax, precisely because they are discussing the subject of attacks against web applications. The core functionality of the blogging application is to store this input in a database and display it back to readers of the blog. The obvious attacks that must be defended against here are SQL injection and cross-site scripting. But any solution based on whitelist input validation is liable to break the application, preventing users from doing what they need to. The better solution is to handle user input in ways that are inherently safe: arbitrary input can be safely passed to the database using parameterised queries, and safely rendered back to readers using HTML-encoding. In the vast majority of cases, these defences are completely robust against SQL injection and XSS, even without any input validation being performed. (By the way, I make no claims about the security of this particular blogging application, because I didn't write it.)

Curiously, much later in the book (p261) parameterised queries are mentioned briefly as an effective remedy, in a discussion about client-side SQL injection into the Google Gears database.

Cross-site request forgery. To block XSRF attacks, developers are advised "to create a unique token and store that token in both server-side session state and in a client-side state mechanism like a cookie" (p76). But this recommendation achieves nothing - the primary cause of XSRF bugs is of course that browsers automatically submit tokens stored in cookies regardless of whether a request originates on-site or off-site. Again, an aside to a different discussion later in the book gets it right: "Placing the token in a cookie would be useless and completely defeat the purpose of sending it" (p430).

Cookie scope. It is wrongly asserted that cookies are not by default submitted to subdomains (p208), when in fact Internet Explorer always submits cookies to subdomains of their in-scope domain (regardless of the spec). Chapter 11 recommends that aggregator sites should place third-party widgets into IFrame jails residing in subdomains of the aggregator site's domain. The problem is raised of how to prevent a malicious widget stealing the user's session token for the aggregator site. It is wrongly advised that default cookie handling takes care of the problem: "by default, cookies set by site.com cannot be accessed by foo.site.com" (p323). This is mistaken: the mechanism proposed is indeed open to session hijacking by a malicious widget.

It is also wrongly asserted that the path scope of cookies defaults to the web root (p206), when in fact in all browsers (and indeed the spec) the scope defaults to the directory of the script which issued the cookie. It is also advised that an application can leverage path scope to prevent untrusted applications residing on the same domain from accessing its cookies (p242), without mentioning attacks that exist against this defence.

(If you don't believe me about the way browsers handle cookies with default scope, then download Burp, inject some cookies into responses from various paths and domains, and see for yourself.)

There is a certain amount of filler in the book. Chapter 10 ("Request Origin Issues") does not discuss same origin issues, but rather makes the simple points that web servers can't tell whether a request comes from a human clicking a link or from XmlHttpRequest, and that XHR is faster and less clunky at doing multi-stage attacks than other techniques. This message doesn't really merit an entire chapter, especially given that the book has another chapter specifically about XHR-based worms. Also, Chapter 14 ("Testing Ajax Applications") consists of a high-level description of a few vulnerability scanning tools, with minimal attention to Ajax. Given that the rest of the book can be summarised as "Lots of things can go wrong in Ajax applications", it would have been nice to see some actual testing methodology here - specifically, something to help a penetration tester who is familiar with conventional web applications and who one day says: "Ah, this application uses Ajax; what else do I need to do to test it properly?".

Despite the caveats described, I would recommend this book to a reader who already has a good grounding of web application security knowledge and who wants to learn more about Ajax. (Indeed, the relative size of my pro and con remarks is not in proportion to their relative significance.) The book's main strengths lie in good expositions of many Ajax-related technologies and frameworks, and in clear illustrations of how web applications (Ajax-based and otherwise) can be vulnerable. However, if you need detailed and reliable information about how to attack or defend Ajax applications, this may not be the book for you.

ajax

SQL Injection

books

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
