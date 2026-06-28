# Lab: Bypassing rate limits via race conditions

Source: https://portswigger.net/web-security/race-conditions/lab-race-conditions-bypassing-rate-limits
Fetched: 2026-06-28T09:17:59.301261+00:00

Web Security Academy

Race conditions

Lab

Lab: Bypassing rate limits via race conditions

This lab's login mechanism uses rate limiting to defend against brute-force attacks. However, this can be bypassed due to a race condition.

To solve the lab:

Work out how to exploit the race condition to bypass the rate limit.

Successfully brute-force the password for the user carlos.

Log in and access the admin panel.

Delete the user carlos.

You can log in to your account with the following credentials: wiener:peter.

You should use the following list of potential passwords:

Passwords

123123

abc123

football

monkey

letmein

shadow

master

666666

qwertyuiop

123321

mustang

123456

password

12345678

qwerty

123456789

12345

1234

111111

1234567

dragon

1234567890

michael

x654321

superman

1qaz2wsx

baseball

7777777

121212

000000

Note

Solving this lab requires Burp Suite 2023.9 or higher. You should also use the latest version of the Turbo Intruder, which is available from the BApp Store.

You have a time limit of 15 mins. If you don't solve the lab within the time limit, you can reset the lab. However, Carlos's password changes each time.

Solution

Predict a potential collision

Experiment with the login function by intentionally submitting incorrect passwords for your own account.

Observe that if you enter the incorrect password more than three times, you're temporarily blocked from making any more login attempts for the same account.

Try logging in using another arbitrary username and observe that you see the normal Invalid username or password message. This indicates that the rate limit is enforced per-username rather than per-session.

Deduce that the number of failed attempts per username must be stored server-side.

Consider that there may be a race window between:

When you submit the login attempt.

When the website increments the counter for the number of failed login attempts associated with a particular username.

Benchmark the behavior

From the proxy history, find a POST /login request containing an unsuccessful login attempt for your own account.

Send this request to Burp Repeater.

In Repeater, add the new tab to a group. For details on how to do this, see Creating a new tab group.

Right-click the grouped tab, then select Duplicate tab. Create 19 duplicate tabs. The new tabs are automatically added to the group.

Send the group of requests in sequence, using separate connections to reduce the chance of interference. For details on how to do this, see Sending requests in sequence.

Observe that after two more failed login attempts, you're temporarily locked out as expected.

Probe for clues

Send the group of requests again, but this time in parallel. For details on how to do this, see Sending requests in parallel

Study the responses. Notice that although you have triggered the account lock, more than three requests received the normal Invalid username and password response.

Infer that if you're quick enough, you're able to submit more than three login attempts before the account lock is triggered.

Prove the concept

Still in Repeater, highlight the value of the password parameter in the POST /login request.

Right-click and select Extensions > Turbo Intruder > Send to turbo intruder.

In Turbo Intruder, in the request editor, notice that the value of the password parameter is automatically marked as a payload position with the %s placeholder.

Change the username parameter to carlos.

From the drop-down menu, select the examples/race-single-packet-attack.py template.

In the Python editor, edit the template so that your attack queues the request once using each of the candidate passwords. For simplicity, you can copy the following example:

def queueRequests(target, wordlists):

# as the target supports HTTP/2, use engine=Engine.BURP2 and concurrentConnections=1 for a single-packet attack

engine = RequestEngine(endpoint=target.endpoint,

concurrentConnections=1,

engine=Engine.BURP2

)

# assign the list of candidate passwords from your clipboard

passwords = wordlists.clipboard

# queue a login request using each password from the wordlist

# the 'gate' argument withholds the final part of each request until engine.openGate() is invoked

for password in passwords:

engine.queue(target.req, password, gate='1')

# once every request has been queued

# invoke engine.openGate() to send all requests in the given gate simultaneously

engine.openGate('1')

def handleResponse(req, interesting):

table.add(req)

Note that we're assigning the password list from the clipboard by referencing wordlists.clipboard. Copy the list of candidate passwords to your clipboard.

Launch the attack.

Study the responses.

If you have no successful logins, wait for the account lock to reset and then repeat the attack. You might want to remove any passwords from the list that you know are incorrect.

If you get a 302 response, notice that this login appears to be successful. Make a note of the corresponding password from the Payload column.

Wait for the account lock to reset, then log in as carlos using the identified password.

Access the admin panel and delete the user carlos to solve the lab.

Community solutions

Intigriti

Popo Hack

Find race condition vulnerabilities using Burp Suite

Try for free
