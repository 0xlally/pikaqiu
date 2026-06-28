# XSRF and threat ratings

Source: https://portswigger.net/blog/xsrf-and-threat-ratings
Fetched: 2026-06-28T09:15:28.649712+00:00

XSRF and threat ratings

Dafydd Stuttard |

Thursday, 20 March 2008 at 19:16 UTC

xsrf

SQL Injection

Pen Testing

Readers who are relatively long in the tooth will remember the sweet, carefree days before the web was blighted by cross-site request forgery (XSRF). Like or loathe these vulnerabilities, they are here to stay, and as penetration testers we need to look for and report them.

One often overlooked aspect of the arrival of XSRF is that it obliges us to reassess the threat ratings associated with some other types of vulnerability. Here is one example.

Consider an application which contains a function for administrators to view a user's details:

https://myapp/admin/ViewUser.asp?UID=123

The UID parameter is inserted into a dynamic SQL query, which is passed to MS-SQL Server, and so the application is vulnerable to SQL injection. However, the ViewUser function is protected by robust access controls which prevent lower privileged users from accessing it. Only administrators, who are fully trusted in any case, can exploit the bug. In days gone by, we would have called this a low risk issue, probably worth fixing from a defence-in-depth perspective, but nothing to get excited about.

Enter XSRF. Consider a different application which implements a function for administrators to issue SQL queries directly to the database. This is done using URLs like the following:

https://otherapp/admin/doSQL.php?query=

SELECT+*+FROM+ORDERS

This function is wide open to XSRF. An attacker can create a malicious web page which, if viewed by a logged-in administrator, will perform arbitrary queries on the database. For example:

<img src="https://otherapp/admin/doSQL.php?query=

INSERT+INTO+USERS+(username,password,isAdmin)+

VALUES+('jlo','secrets',true)">

We might classify this XSRF vulnerability as a medium or (if we are feeling excited) high risk issue.

Now, each of the functions described enables a crafted request to perform arbitrary actions on the database - the only difference is that this is the intended purpose of the second function, and is the consequence of bad coding in the previous example. But from an attacker's perspective, it doesn't matter whether the application's behaviour was intended or not - a vulnerability is simply a condition that can be exploited for some illicit purpose. And the first vulnerability can be exploited via XSRF just as easily as the second:

<img src="https://myapp/admin/ViewUser.asp?UID=

123;+INSERT+INTO+USERS+(username,password,isAdmin)+

VALUES+('wade','congrats',true)">

Hence, regardless of the access controls protecting direct exploitation of the SQL injection vulnerability, the threat rating we assign to this issue should be at least as serious as that which we assign to the second vulnerability. The arrival of XSRF as a recognised attack vector obliges us to identify ways of exploiting some other bugs that we may previously have overlooked.

xsrf

SQL Injection

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
