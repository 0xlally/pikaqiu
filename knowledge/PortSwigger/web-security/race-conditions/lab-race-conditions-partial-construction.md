# Lab: Partial construction race conditions

Source: https://portswigger.net/web-security/race-conditions/lab-race-conditions-partial-construction
Fetched: 2026-06-28T09:17:59.711836+00:00

Web Security Academy

Race conditions

Lab

Lab: Partial construction race conditions

This lab contains a user registration mechanism. A race condition enables you to bypass email verification and register with an arbitrary email address that you do not own.

To solve the lab, exploit this race condition to create an account, then log in and delete the user carlos.

Note

Solving this lab requires Burp Suite 2023.9 or higher. You should also use the latest version of the Turbo Intruder, which is available from the BApp Store.

Hint

You may need to experiment with different ways of lining up the race window to successfully exploit this vulnerability.

Solution

Predict a potential collision

Study the user registration mechanism. Observe that:

You can only register using @ginandjuice.shop email addresses.

To complete the registration, you need to visit the confirmation link, which is sent via email.

As you don't have access to an @ginandjuice.shop email account, you don't appear to have a way to access a valid confirmation link.

In Burp, from the proxy history, notice that there is a request to fetch /resources/static/users.js.

Study the JavaScript and notice that this dynamically generates a form for the confirmation page, which is presumably linked from the confirmation email. This leaks the fact that the final confirmation is submitted via a POST request to /confirm, with the token provided in the query string.

In Burp Repeater, create an equivalent request to what your browser might send when clicking the confirmation link. For example:

POST /confirm?token=1 HTTP/2

Host: YOUR-LAB-ID.web-security-academy.net

Content-Type: x-www-form-urlencoded

Content-Length: 0

Experiment with the token parameter in your newly crafted confirmation request. Observe that:

If you submit an arbitrary token, you receive an Incorrect token: <YOUR-TOKEN> response.

If you remove the parameter altogether, you receive a Missing parameter: token response.

If you submit an empty token parameter, you receive a Forbidden response.

Consider that this Forbidden response may indicate that the developers have patched a vulnerability that could be exploited by sending an empty token parameter.

Consider that there may be a small race window between:

When you submit a request to register a user.

When the newly generated registration token is actually stored in the database.

If so, there may be a temporary sub-state in which null (or equivalent) is a valid token for confirming the user's registration.

Experiment with different ways of submitting a token parameter with a value equivalent to null. For example, some frameworks let you to pass an empty array as follows:

POST /confirm?token[]=

Observe that this time, instead of the Forbidden response, you receive an Invalid token: Array response. This shows that you've successfully passed in an empty array, which could potentially match an uninitialized registration token.

Benchmark the behavior

Send the POST /register request to Burp Repeater.

In Burp Repeater, experiment with the registration request. Observe that if you attempt to register the same username more than once, you get a different response.

In a separate Repeater tab, use what you've learned from the JavaScript import to construct a confirmation request with an arbitrary token. For example:

POST /confirm?token=1 HTTP/2

Host: YOUR-LAB-ID.web-security-academy.net

Cookie: phpsessionid=YOUR-SESSION-ID

Content-Type: application/x-www-form-urlencoded

Content-Length: 0

Add both requests to a new tab group.

Try sending both requests sequentially and in parallel several times, making sure to change the username in the registration request each time to avoid hitting the separate Account already exists with this name code path. For details on how to do this, see

Sending grouped HTTP requests.

Notice that the confirmation response consistently arrives much quicker than the response to the registration request.

Prove the concept

Note that you need the server to begin creating the pending user in the database, then compare the token you send in the confirmation request before the user creation is complete.

Consider that as the confirmation response is always processed much more quickly, you need to delay this so that it falls within the race window.

In the POST /register request, highlight the value of the username parameter, then right-click and select Extensions > Turbo Intruder > Send to turbo intruder.

In Turbo Intruder, in the request editor:

Notice that the value of the username parameter is automatically marked as a payload position with the %s placeholder.

Make sure the email parameter is set to an arbitrary @ginandjuice.shop address that is not likely to already be registered on the site.

Make a note of the static value of the password parameter. You'll need this later.

From the drop-down menu, select the examples/race-single-packet-attack.py template.

In the Python editor, modify the main body of the template as follows:

Define a variable containing the confirmation request you've been testing in Repeater.

Create a loop that queues a single registration request using a new username for each attempt. Set the gate argument to match the current iteration.

Create a nested loop that queues a large number of confirmation requests for each attempt. These should also use the same release gate.

Open the gate for all the requests in each attempt at the same time.

The resulting script should look something like this:

def queueRequests(target, wordlists):

engine = RequestEngine(endpoint=target.endpoint,

concurrentConnections=1,

engine=Engine.BURP2

)

confirmationReq = '''POST /confirm?token[]= HTTP/2

Host: YOUR-LAB-ID.web-security-academy.net

Cookie: phpsessionid=YOUR-SESSION-TOKEN

Content-Length: 0

'''

for attempt in range(20):

currentAttempt = str(attempt)

username = 'User' + currentAttempt

# queue a single registration request

engine.queue(target.req, username, gate=currentAttempt)

# queue 50 confirmation requests - note that this will probably sent in two separate packets

for i in range(50):

engine.queue(confirmationReq, gate=currentAttempt)

# send all the queued requests for this attempt

engine.openGate(currentAttempt)

def handleResponse(req, interesting):

table.add(req)

Launch the attack.

In the results table, sort the results by the Length column.

If the attack was successful, you should see one or more 200 responses to your confirmation request containing the message Account registration for user <USERNAME> successful.

Make a note of the username from one of these responses. If you used the example script above, this will be something like User4.

In the browser, log in using this username and the static password you used in the registration request.

Access the admin panel and delete carlos to solve the lab.

Community solutions

Intigriti

Find race condition vulnerabilities using Burp Suite

Try for free
