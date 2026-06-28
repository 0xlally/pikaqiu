# Attacking parameter names

Source: https://portswigger.net/blog/attacking-parameter-names
Fetched: 2026-06-28T09:15:07.190560+00:00

Attacking parameter names

Dafydd Stuttard |

Friday, 22 August 2008 at 07:26 UTC

XSS

ASP

NET

SQL Injection

Pen Testing

The most obvious and common technique for finding input-based bugs in web applications is to attack the values of the request parameters used by the application. With this technique, the value of each request parameter is replaced (or appended) with a range of attack strings designed to trigger common vulnerabilities, and the application's responses are reviewed to identify evidence of those vulnerabilities. This core technique is employed in manual testing, application fuzzing, and automated vulnerability scanners. And it is capable of finding a majority of the input-based bugs that exist in a typical web application.

A less commonly used technique is to attack parameter names. With this technique, the attack strings are inserted into the name of a request parameter, typically into a newly-added parameter name. In various situations, this technique can identify bugs that cannot be found only by manipulating parameter values. Applications often perform some defensive input validation on the values of request parameters, but perform less rigorous or no validation on parameter names. If arbitrary parameter names are subsequently processed in an unsafe manner, then the application is vulnerable, and can be exploited by submitting crafted input within parameter names. I'll describe a couple of examples of this.

SQL injection in parameter names

Some applications accept arbitrary request parameters and incorporate these into dynamic SQL queries. Consider a preferences page containing a large number of input fields. Submitting the page causes a request with a large number of parameters, for example:

http://myapp/Prefs.aspx?lang=en&

which causes the application to make a number of SQL queries of the form:

UPDATE profile SET lang='en' WHERE UID=2104

UPDATE profile SET region='uk' WHERE UID=2104

UPDATE profile SET currency='gbp' WHERE UID=2104

...

For whatever reason, this functionality is implemented by enumerating all of the parameters from the query string, and deriving a SQL query from each one. The code looks something like this (forgive the simplification):

IEnumerator i =

Request.QueryString.GetEnumerator();

while (i.MoveNext())

{

string name = (string)i.Current;

string query = "UPDATE profile SET " + name + "='"

+ Request.QueryString[name].Replace("'", "''") +

"' WHERE uid=" + uid;

...

}

Note the sanitisation that is performed on parameter values, in an attempt to block SQL injection attacks: single quotation marks are being doubled up. Note also that no validation is applied to parameter names, probably on the assumption that these are under the application's control, because the application creates the form containing the field names. However, an attacker can of course supply any parameters they wish, and in this instance can deliver a SQL injection attack via parameter names, not values.

XSS in parameter names

Many applications echo parameter names and values into their responses, and yet perform anti-XSS validation only on parameter values. This often arises when applications rely upon generic application-wide input filters or web application firewalls to defend against XSS attacks, but where these defences validate only parameter values, not names. The ValidateRequest feature in ASP.NET behaves in this way, and tolerates malicious input residing within a parameter name.

Application functions which echo arbitrary parameter names are suprisingly common, due to the range of functions which echo the entire URL or query string into the response (into links, form fields, redirects, etc). Consider a simple example which, in itself, is wide open to XSS:

Response.Write(Request.Url);

In the default configuration of ASP.NET, where ValidateRequest is enabled, we cannot trivially exploit this using a crafted parameter value, because ValidateRequest blocks values containing HTML mark-up. For example, requesting the URL:

http://myapp/Default.aspx?a=<script>

causes the following error:

However, if we instead place our attack payload into a parameter name, then ValidateRequest allows our input through and we hit the vulnerable code:

http://myapp/Default.aspx?<script>

The moral of the story? If you are a hacker, don't forget to try all of your input-based attacks within an added parameter name, not only within the values of existing parameters. If you are responsible for securing an application, treat submitted parameter names as tainted, and always try to fix your bugs in the code, rather than hiding behind generic application-wide defences.

XSS

ASP

NET

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
