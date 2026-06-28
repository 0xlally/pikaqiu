# Lab: Blind SQL injection with time delays and information retrieval

Source: https://portswigger.net/web-security/sql-injection/blind/lab-time-delays-info-retrieval
Fetched: 2026-06-28T09:18:03.238148+00:00

Web Security Academy

SQL injection

Blind

Lab

Lab: Blind SQL injection with time delays and information retrieval

This lab contains a blind SQL injection vulnerability. The application uses a tracking cookie for analytics, and performs a SQL query containing the value of the submitted cookie.

The results of the SQL query are not returned, and the application does not respond any differently based on whether the query returns any rows or causes an error. However, since the query is executed synchronously, it is possible to trigger conditional time delays to infer information.

The database contains a different table called users, with columns called username and password. You need to exploit the blind SQL injection vulnerability to find out the password of the administrator user.

To solve the lab, log in as the administrator user.

Hint

You can find some useful payloads on our SQL injection cheat sheet.

Solution

Visit the front page of the shop, and use Burp Suite to intercept and modify the request containing the TrackingId cookie.

Modify the TrackingId cookie, changing it to:

TrackingId=x'%3BSELECT+CASE+WHEN+(1=1)+THEN+pg_sleep(10)+ELSE+pg_sleep(0)+END--

Verify that the application takes 10 seconds to respond.

Now change it to:

TrackingId=x'%3BSELECT+CASE+WHEN+(1=2)+THEN+pg_sleep(10)+ELSE+pg_sleep(0)+END--

Verify that the application responds immediately with no time delay. This demonstrates how you can test a single boolean condition and infer the result.

Now change it to:

TrackingId=x'%3BSELECT+CASE+WHEN+(username='administrator')+THEN+pg_sleep(10)+ELSE+pg_sleep(0)+END+FROM+users--

Verify that the condition is true, confirming that there is a user called administrator.

The next step is to determine how many characters are in the password of the administrator user. To do this, change the value to:

TrackingId=x'%3BSELECT+CASE+WHEN+(username='administrator'+AND+LENGTH(password)>1)+THEN+pg_sleep(10)+ELSE+pg_sleep(0)+END+FROM+users--

This condition should be true, confirming that the password is greater than 1 character in length.

Send a series of follow-up values to test different password lengths. Send:

TrackingId=x'%3BSELECT+CASE+WHEN+(username='administrator'+AND+LENGTH(password)>2)+THEN+pg_sleep(10)+ELSE+pg_sleep(0)+END+FROM+users--

Then send:

TrackingId=x'%3BSELECT+CASE+WHEN+(username='administrator'+AND+LENGTH(password)>3)+THEN+pg_sleep(10)+ELSE+pg_sleep(0)+END+FROM+users--

And so on. You can do this manually using Burp Repeater, since the length is likely to be short. When the condition stops being true (i.e. when the application responds immediately without a time delay), you have determined the length of the password, which is in fact 20 characters long.

After determining the length of the password, the next step is to test the character at each position to determine its value. This involves a much larger number of requests, so you need to use Burp Intruder. Send the request you are working on to Burp Intruder, using the context menu.

In Burp Intruder, change the value of the cookie to:

TrackingId=x'%3BSELECT+CASE+WHEN+(username='administrator'+AND+SUBSTRING(password,1,1)='a')+THEN+pg_sleep(10)+ELSE+pg_sleep(0)+END+FROM+users--

This uses the SUBSTRING() function to extract a single character from the password, and test it against a specific value. Our attack will cycle through each position and possible value, testing each one in turn.

Place payload position markers around the a character in the cookie value. To do this, select just the a, and click the Add § button. You should then see the following as the cookie value (note the payload position markers):

TrackingId=x'%3BSELECT+CASE+WHEN+(username='administrator'+AND+SUBSTRING(password,1,1)='§a§')+THEN+pg_sleep(10)+ELSE+pg_sleep(0)+END+FROM+users--

To test the character at each position, you'll need to send suitable payloads in the payload position that you've defined. You can assume that the password contains only lower case alphanumeric characters. In the

Payloads side panel, check that Simple list is selected, and under

Payload configuration add the payloads in the range a - z and 0 - 9. You can select these easily using the Add from list drop-down.

To be able to tell when the correct character was submitted, you'll need to monitor the time taken for the application to respond to each request. For this process to be as reliable as possible, you need to configure the Intruder attack to issue requests in a single thread. To do this, click the Resource pool tab to open the Resource pool side panel and add the attack to a resource pool with the

Maximum concurrent requests set to 1.

Launch the attack by clicking the Start attack button.

Review the attack results to find the value of the character at the first position. You should see a column in the results called Response received. This will generally contain a small number, representing the number of milliseconds the application took to respond. One of the rows should have a larger number in this column, in the region of 10,000 milliseconds. The payload showing for that row is the value of the character at the first position.

Now, you simply need to re-run the attack for each of the other character positions in the password, to determine their value. To do this, go back to the main Burp window and change the specified offset from 1 to 2. You should then see the following as the cookie value:

TrackingId=x'%3BSELECT+CASE+WHEN+(username='administrator'+AND+SUBSTRING(password,2,1)='§a§')+THEN+pg_sleep(10)+ELSE+pg_sleep(0)+END+FROM+users--

Launch the modified attack, review the results, and note the character at the second offset.

Continue this process testing offset 3, 4, and so on, until you have the whole password.

In the browser, click My account to open the login page. Use the password to log in as the administrator user.

Community solutions

Intigriti

Rana Khalil

Michael Sommer

Find SQL injection vulnerabilities using Burp Suite

Try for free
