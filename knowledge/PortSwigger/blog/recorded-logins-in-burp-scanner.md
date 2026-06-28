# Recorded logins in Burp Scanner

Source: https://portswigger.net/blog/recorded-logins-in-burp-scanner
Fetched: 2026-06-28T09:15:23.923942+00:00

Recorded logins in Burp Scanner

Jonathan Jamison |

Thursday, 22 April 2021 at 13:32 UTC

If you’re using Burp Suite to test your website, it’s probably got some way for users to log in - and chances are it’s more complicated than filling in a username and password and hitting submit. Burp Scanner has always been able to find and use simple login forms, but you can now record a more involved login process, and it’ll play the recording back to authenticate itself, letting it through to test all of your site.

Older versions of Burp Scanner would just look at a site’s raw HTML to identify login forms, but wouldn’t be able to see logins on modern websites that use JavaScript to render their content. Newer versions of Burp Scanner use Chromium to render the site, executing the JavaScript to view the webpage as a user would. Recording a login sequence lets Burp Scanner mimic a user’s actions, interacting with the login process though Chromium exactly as they would.

Most sites will hide a lot of interesting functionality from unauthenticated users, and many will have several classifications of users (think user, admin, super admin, etc.). Logging in to appear as a bona-fide user is crucial to the Scanner’s ability to thoroughly test a website.

Login mechanisms vary a lot between websites, which is difficult for an automated scanner to deal with

Let’s take a minute to look back and discuss how we can log in to a website without a recorded login sequence available. This is how Burp Scanner used to handle all logins, and it’s how it will still behave if you don’t supply a recorded sequence.

When attempting to log in, the first step is to find a login form in the application. This isn’t too tricky, because we can just look for something like <input type=“password”> in the HTML, as there’s no reason for a site not to use a password type on a password field. Of course, we’ll find registrations that ask for a password as well, so once it’s found some candidate forms, Burp Suite’s got a simple heuristic to identify which one is the login:

Pick the form with the fewest password fields, as a login will likely only have one password field, compared to a registration which will probably have two.

If there are multiple forms with the same number of password fields, then the login form will be the one with fewer text fields - registrations might ask for additional information like your name or phone number.

As a tiebreaker, consider the number of <select> fields on the form - again the login will likely have fewer options than the registration.

If all these are identical, then the forms are probably the same anyway, just on different parts of the site, so we can use either one.

Once we’ve found a form, how do we get in? We could go straight to brute force, but that seems like a waste of time and resources. Before recorded logins, Burp Suite would let you specify username/password credentials to use, and plug those into the form once it found it. But what to do if the form requires some extra information? Given some heuristic clues, it would take a guess - it’s not too hard to come up with something that looks like a legitimate email, for example. But the form could still trip the Scanner up by asking it for the number of moons of Saturn, or the year of release of Metallica’s “Seek and Destroy” (the Scanner team’s #1 party anthem, of course).

And what to do if the process is split over multiple pages? A good guess might be to enter the username on the first page, and the password on the second, but this would fail if we were asked to provide a date of birth, perhaps, between these two. Add in the increasing popularity of SSO services (we’re talking about “Log in with Google”, “Log in with Microsoft” et al.) and the chance for complications makes it untenable for the Scanner to rely on the same login strategy for every website.

Record your login to let the Scanner know what to do on your website

The solution is recordable login sequences. We capture the actions performed by a real user, and then the Scanner can replay them when it needs to log in. This means we can handle external SSO providers, multi-stage forms, and include any arbitrary information - it no longer matters if we have to log in with a username, then Google, then Microsoft, then provide some 80s thrash metal trivia. As long as the login process is consistent, then we will be able to perform it every time.

We’re lucky to have some extremely talented developers at PortSwigger, who whipped up a Chrome extension to record a login and export the sequence in JSON to the clipboard. Once captured, the JSON text can be simply pasted into Burp Suite and it’ll play it back as needed - detailed instructions for Burp Suite Professional and Burp Suite Enterprise Edition users are available in the Support Centre.

As a side note, the Burp Suite Navigation Recorder isn’t just limited to logins - it can record any type of user interaction. For example, if you found a XSS vulnerability you could use the recorder to capture and playback the sequence that causes the vulnerability.

Burp Scanner replays the login through its underlying Chromium browser

As highlighted by Alex Borshik’s blog post on browser-powered scanning, Burp Suite uses the DevTools protocol to communicate with the Chromium browser it uses to drive the scan. There were a few approaches to consider when deciding how to replay a login. For example, when clicking an element, we could work similarly to WebDriver, which uses a query selector to locate the element and then dispatches a click event to it. This is mostly how the Scanner works during the “ordinary” sections of a crawl and audit.

For the recorded logins, however, we wanted to mimic the actions taken by a user as closely as possible. DevTools has a native dispatchMouseEvent, equivalent to the user actually moving their mouse and clicking on the screen at some given coordinates. This threw up a number of complications as now we’re relying on knowing the exact position of the element, which could easily have changed between recording and replaying, and could be affected by the screen width; we also need to make sure we don’t click on overlapping elements by mistake. Developing strategies that work consistently across all websites is hard, but we tried a lot of techniques, and we’re pretty happy with the outcome.

We’re working on being able to handle as many logins as possible

As the Scanner just takes actions performed by a user and replays them each time it needs to log in, it works very well for login processes that are the same every time. But if the website asks for different digits of a password each time, or requires a two-factor authentication code, or needs a CAPTCHA to be solved, there’s no way to pre-record the correct behaviour and so recorded logins won’t work. There’s also the possibility that a server detects suspicious activity and locks out the account, or throws up an extra “prove you’re not a robot” that wasn’t present in the recorded login.

Another difficulty is when websites use a popup window as part of the login process. In our existing implementation, we can only use DevTools to talk to a single frame within Chromium, so when a second tab, or second window, is opened we aren’t able to work with it. If you’ve been using recorded logins then you may have come across the error message “Recorded login sequences with popup windows are currently not supported” - but this is a problem we think we can solve, so watch this space.

Recorded logins are a powerful addition to Burp Suite and will become more so

The rollout of recorded logins has been really successful. It’s great to hear from those of you who have been getting more coverage from your scans, and we’ve been working hard on fixing the the issues reported back to us. As well as the aforementioned pop-up windows, some of you have reported logins that work fine for a while and then break during a scan. The next big improvement will be to stabilize the replay, logging in the Scanner as consistently as possible. To keep up with this and all the other cool stuff we’re working on with the Scanner, you can check out our 2021 roadmap.

Special thanks to Dave Paterson of the Scanner team who provided much of the material for this post.

Jonathan Jamison

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
