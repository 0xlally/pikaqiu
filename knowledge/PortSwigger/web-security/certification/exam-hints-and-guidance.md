# Hints and guidance for your exam

Source: https://portswigger.net/web-security/certification/exam-hints-and-guidance
Fetched: 2026-06-28T09:17:41.765645+00:00

Get Burp Suite Certified for

Hints and guidance for your exam

Get certified

Get prepared

Ready to take the exam?

Here's what you need to know.

Hints

You will have four hours to complete the Burp Suite Certified Practitioner exam. There are two applications, and each application contains deliberate vulnerabilities. This means that each application

can be completed in three stages:

Stage 1: Access any user account.

Stage 2: Use your user account to access the admin interface at /admin, perhaps by elevating your privileges or compromising the administrator account.

Stage 3: Use the admin interface to read the contents of /home/carlos/secret from the server's filesystem, and submit it using "submit solution".

We expect the three stages to be completed in order. This means that if you are in an application, attempting to break into the admin interface is a waste of time if you haven't yet got access to

a user account. Likewise, we do not recommend attempting to read files if you don't have access to an admin account.

We restrict outbound traffic from the vulnerable servers to the internet. You won't be able to connect back to any internet server, except for the public Burp Collaborator server and the integrated exploit server.

You can use the integrated exploit server to deliver any kind of payload to the vulnerable application or simulated user.

Although some of the vulnerabilities are tricky to find, we do not intentionally hide files or pages that contain them. You never need to guess folders, filenames or parameter names.

Exam progression

To progress through stages, you need not only to identify vulnerabilities, but also exploit them. For example, if you identified an XSS vulnerability, triggering "alert" execution won't be enough to

get access to the next stage: you need to actually exploit it against one of the simulated users and steal their session. Likewise, for SQL Injection vulnerabilities, you need to extract credentials

from the database and use them to access the target account. You don't need to worry about tedious dumping of all database content though: all tables, columns, and local files are easily guessable and

require just a couple of minutes to manually extract the required password or token.

Techniques

Scanning selected pages and insertion points with Burp Suite Professional will often help you quickly progress through the exam. Attempting a full application scan will not be feasible in the exam time

frame. Some vulnerabilities are are very challenging to detect using only manual testing. If you get stuck, we highly recommend using Burp Scanner to help you tackle the problem.

Guides

We've created a guide to using Burp Scanner during manual testing, to make sure you've got

to grips with the full scope of scanning you'll need to perform during the exam. The exam also requires you to be able to adapt

your attack methods to bypass broken defenses - specifically - obfuscating attacks using encodings.

The victim user is running Chromium. When using the XSS Cheat Sheet, focus on vectors that work on Chrome. If your XSS

attack works in Burp's browser or Chrome, chances are it'll work on the victim.

Software

Burp Suite Professional provides the essential functionality to solve the exam. Some vulnerabilities are easier to solve with the following third party tools: ysoserial

and HTTP Request Smuggler. These tools are used by certain labs at the "Practitioner" level. We recommend caution when using other tools - they may

turn out not to be suitable for your objective.

Problem solving

If you come up with a solution that doesn't work as expected, we can offer some general advice on what to do:

If you're attacking the victim user, test the attack out on your own browser first. Pay close attention to the HTTP traffic sequence in Burp.

If your solution is adapted from an Academy lab, try to analyze how the application differs from the lab.

Try to identify any assumptions you're making, and put them to the test.

Refer back to the skill set the certification aims to prove.

Taken the exam and didn't pass?

To help you get better prepared for your next exam attempt, we've put together some helpful hints and advice.

Read the tips for retaking your exam

How the exam works

Read more

Take the practice exam

Read more

What the exam involves

Read more

Buy your BSCP exam

Buy now
