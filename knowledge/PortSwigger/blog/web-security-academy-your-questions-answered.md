# Web Security Academy - your questions answered

Source: https://portswigger.net/blog/web-security-academy-your-questions-answered
Fetched: 2026-06-28T09:15:28.215160+00:00

Web Security Academy - your questions answered

Emma Stocks |

Thursday, 3 December 2020 at 15:31 UTC

We're nearly at 200 labs on our ever-popular Web Security Academy, so before we hit that magic number we wanted to give you the chance to get your questions answered. This blog post answers your most-asked questions, based on your responses to our tweet.

Which lab or topic should I start with as a beginner?

This question comes up time and time again, and since we love hearing about all of your Web Security Academy success stories it felt like a great place to start. We want to get as many of you as possible off to a flying start!

First of all, if you're right at the start of your learning journey, we recommend checking out our video tutorial series - they'll guide you through some really handy Burp Suite Professional basics.

Our recommended starting topic is SQL injection - an old-but-gold vulnerability responsible for many high-profile data breaches. Although relatively simple to learn, it can potentially be used for some high-severity exploits. This makes it an ideal first topic for beginners and essential knowledge even for more experienced users.

Once you've worked through the SQL injection topic - there are currently 16 labs to complete - we suggest that your next port of call should be some of our other server-side topics such as authentication, directory traversal, or command injection.

If you're still struggling, we've created a page with handy tips, plenty of resources, and lots of advice for everyone who is just getting started on the topics. If you know what you're doing but just aren't sure where to start, then have a read of our learning path - we've listed out our suggested order for you to work through the topics.

Which topic should I do after completing SQL injection and XSS?

It's entirely your own choice which topic you do after completing SQLi and XSS, as it'll very much depend on your skill level and existing knowledge of various vulnerabilities. However, we would recommend that a great follow-on topic would be our authentication labs, as understanding how to bypass authentication is a key skill.

Understanding how to bypass authentication can help you to access additional attack surfaces, which may reveal additional vulnerabilities you wouldn't have discovered otherwise. Additionally, these labs and materials are a really great way to test your skills with Burp Intruder. The authentication labs will help you learn how to use Burp Intruder for brute-force attacks, and for enumerating different inputs.

I'm stuck on the "SSRF with whitelist-based input filter" lab - what should I do?

The SSRF with whitelist-based input lab materials should help you work through this lab. To successfully complete this particular lab, you may want to try combining some of the techniques discussed to come up with the solution.

If this vulnerability is something you'd like to know more about, we highly recommend reading "A new era for SSRF" by Orange Tsai - we named it as our top web hacking technique of 2017. If you're still stuck, we also provide solutions for all of our labs.

If you ever find yourself stuck on anything within our labs and topics, spending more time researching is nearly always going to be the best thing to do. Our labs are all designed to be tackled as part of the process of understanding the topic as a whole. This means that you'll usually need to read through all of the learning materials before attempting to solve the labs.

I need a path of modules to work through - what order should I do the topics in?

For beginners, we recommend starting with server-side topics because these are generally simpler to get your head around. With this type of vulnerability, you only need to understand what's happening on the back-end - this makes it much simpler for you to work through and find the solution.

Server-side topics are also a great place to start to build up a solid foundational knowledge. Working through topics such as SQLi, authentication, and business logic vulnerabilities for example, will equip you with some of the knowledge you need to progress more effectively onto the more challenging topics.

When you start on a new topic, read the section of the learning materials thoroughly before you attempt the lab that accompanies it. If you don't read all of the relevant information prior to attempting to solve the labs, you may miss a vital component that will help you work out the solution. The labs are designed to consolidate your learning, so if you find yourself stuck you may need to go back to the learning materials and labs prior to the one you're on to practice your skills before you attempt it again.

We've also created a suggested learning pathway, as we know a lot of our users will find this really helpful, so make sure to check that out for some guidance if you're stuck!

What resources would you recommend for me to improve my JavaScript knowledge?

We asked the team at PortSwigger Research, and they suggested the following resources for improving and expanding JavaScript knowledge.

The "You Don't Know JS" book series. These are accessible but quite detail-oriented, which is probably a good approach for hacking since understanding of the foundations of the language is really helpful. The first editions are also free.

Effective JavaScript: 68 Specific Ways to Harness the Power of JavaScript.

Finally, although some of the content may be a little outdated, "JavaScript: The good parts" provides a great foundation for building on.

Are there any resources you recommend to keep practicing business logic vulnerabilities?

While we have no immediate plans to create any additional labs on this topic, we always recommend reading the Web Application Hacker's Handbook. If you haven't come across this book before, it was written by PortSwigger's founder Dafydd Stuttard. The Web Security Academy was developed and produced in place of a third edition of this book, but the second edition has a great section on business logic vulnerabilities.

Additionally, bug bounty sites are a great way to build up your practical experience, particularly as they often have opportunities for beginners. If this is an avenue you're interested in, check out James Kettle's "So you want to be a web security researcher" for his advice before you get started.

When bruteforcing in the 2FA bypass lab, or using Burp Intruder, it seems that Burp Suite Community doesn't support more than one thread. Do you suggest using Burp Suite Professional, or doing your own scripting to accomplish the task?

We would always recommend using Burp Suite products on the Web Security Academy. Mainly because we built them, so we feel that they're the best tool for the job.

There are a lot of features that come with Burp Suite Professional that can enhance your ability to complete labs, but if you're proficient in Python you can always use James Kettle's Turbo Intruder extension to help you in this particular instance.

If you're unfamiliar with Burp Suite, the Web Security Academy is a great way to get to grips with Burp Suite Community Edition. Just like our learning platform, it's completely free.

I really want more labs - on SOAP, REST, and GraphQL. Are there any coming out soon?

In a nutshell, yes. We have plans to cover more topics, including API-based vulnerabilities, but there's no exact timeframe we can give. For the latest news, follow us on Twitter.

Have you thought of making an offline version of the labs?

We have no current plans to take the learning experience offline, as we created the Web Security Academy as a follow-on from the Web Application Hacker’s Handbook. Keeping the labs online allows us to provide our users with the latest vulnerability information, and ensures we are providing a fun and interactive learning experience.

To this end, we see no benefit to making them offline but we'd love to know more about this - please contact us so we can find out further information.

I really enjoy all of the labs where I can use Burp Collaborator. Which ones would you recommend for me to keep practicing my techniques?

If you're particularly looking to test your skills with Burp Collaborator, any of the labs that mention 'out-of-band' interactions are a safe bet. Some of our labs on blind vulnerabilities can also be solved using Burp Collaborator. You'll find examples in any of the labs that mention "blind" or "out-of-band" - such as the SSRF, SQLi, or XXE topics.

Additionally, our labs covering stealing cookies, performing internal network pivot attacks, dangling markup attacks, and blind out-of-band data exfiltration, are all great ways to test your skills with Burp Collaborator.

I would like to see a lab on chaining multiple vulnerabilities into rce? Anything like that currently?

Although we don't have any topics that cover this specifically, some of the expert level labs involve chaining a couple of vulnerabilities. If it's a challenge that you're after, we would highly recommend the topic on insecure deserialization - there are some real head-scratchers built in there.

In terms of upcoming topics, we're not about to spill our secrets. While we can't give you any exact details, you'll just have to trust that we have some exciting new challenges in the pipeline, so follow us on Twitter to be sure you'll hear the latest.

Got any more questions?

We love hearing from the people who use our Web Security Academy, as your feedback is what helps us to share our future plans. If you have any other queries, or your question wasn't answered here, give us a shout on Twitter - we'd love to know what you think.

Don't forget, we now have a dashboard so you can track your progress through each and every one of the topics on our Web Security Academy. All you have to do is sign up, and get started on your first topic!

Emma Stocks

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
