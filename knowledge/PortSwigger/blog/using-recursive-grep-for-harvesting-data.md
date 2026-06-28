# Using recursive grep for harvesting data

Source: https://portswigger.net/blog/using-recursive-grep-for-harvesting-data
Fetched: 2026-06-28T09:15:26.913386+00:00

Using recursive grep for harvesting data

Dafydd Stuttard |

Thursday, 5 April 2007 at 09:02 UTC

SQL Injection

burp

Talking to someone the other day I realised that even many experienced users of burp don’t know what the "recursive grep" payload source is used for.

This payload source is different from all the others, because it generates each attack payload dynamically based upon the application’s response to the previous request. In some situations, this can be extremely useful when extracting data from a vulnerable application.

A typical situation is where you have an SQL injection bug that enables you to retrieve a single item of data at a time. To extract the entire contents of a table, you can use recursion to extract each value in turn on the basis of the previous value. For example, suppose you are attacking an MS-SQL database and have enumerated the structure of the table containing user credentials. Supplying the following input returns an informative error message containing the username which appears alphabetically first in this table:

' or 1 in (select min(username) from users where username > 'a')--

Microsoft OLE DB Provider for ODBC Drivers error '80040e07'

[Microsoft][ODBC SQL Server Driver][SQL Server]Syntax error converting the nvarchar value 'abigail' to a column of data type int.

This gives you the username 'abigail', which you can place into your next input to retrieve the username which appears alphabetically second:

' or 1 in (select min(username) from users where username > 'abigail')--

Microsoft OLE DB Provider for ODBC Drivers error '80040e07'

[Microsoft][ODBC SQL Server Driver][SQL Server]Syntax error converting the nvarchar value 'adam' to a column of data type int.

To extract all usernames, you can continue this process, inserting each discovered username into the next request until no more values are returned. However, performing this attack manually may be very laborious. You could write a script to do it in a few minutes. Or in a few seconds, you can configure the "recursive grep" function to perform the attack for you.

The first step is to capture the vulnerable request in burp proxy, and choose the "send to intruder" action. Then type your attack string into the vulnerable field, and position the payload markers around the part which you need to modify:

Next, in order to use "recursive grep" as a payload source, you need to configure "extract grep" to capture the username which is disclosed in each response. To do this, you tell intruder to capture the text following the error message

Syntax error converting the nvarchar value '

and to stop capturing when it reaches a single quotation mark:

Finally, you need to select the "recursive grep" payload source, select the single "extract grep" item you have configured, and specify the first payload as 'a':

That's it! Launching the attack will cause intruder to send 'a' in the first request, and in each subsequent request send the username which was extracted from the previous error message. Within seconds, you can dump out all of the usernames in the table:

You can select save/results table to export the username list. Equipped with this list, you can then use it as a conventional payload source to retrieve all of the passwords and other data, for example using requests of the form:

' or 1 in (select password from users where username = 'abigail')--

There are other cases where recursive grep can be useful, but this kind of attack was the one I mainly had in mind when I wrote it.

SQL Injection

burp

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
