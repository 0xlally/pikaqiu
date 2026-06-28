# Null byte attacks are alive and well

Source: https://portswigger.net/blog/null-byte-attacks-are-alive-and-well
Fetched: 2026-06-28T09:15:22.282195+00:00

Null byte attacks are alive and well

Dafydd Stuttard |

Monday, 5 May 2008 at 13:10 UTC

xpath

ldap

null bytes

Null byte attacks against web and other applications are nothing new. Later in this post, I will describe two cases that may nonetheless be unfamiliar to some readers.

Before that, a well-known example to illustrate the issue. Consider a Java-based application which displays an image file specified by the user:

String filename = request.getParameter("filename");

if (filename.endsWith(".jpg"))

{

File f = new File(filename);

...

Forget about path traversal attacks for the moment. The application seeks to ensure that the function can only be used to access JPEG files by checking that the user-supplied filename ends in ".jpg". If so, the filename is passed to the constructor for java.io.File, which opens the specified file.

The file extension check can of course be defeated using input of the form:

secret.txt%00.jpg

where %00 is a URL-encoded null byte. The reason the attack works is because of the different ways in which null bytes are typically handled in native and managed code. In native code, the length of a string is determined by the position of the first null byte from the start of the string - the null byte effectively terminates the string. In managed code, on the other hand, string objects comprise a character array, which may contain null bytes, and a separate record of the string's length.

When the above Java code excutes String.endsWith() on our input, it knows that the filename string is 15 characters long, and it checks whether the last four characters (after the null byte) match ".jpg", which they do. However, when the filename is processed by java.io.File, this operation is ultimately implemented within native operating system APIs in which a string's length is determined by the first null byte after the start of the string. So the filename which is ultimately processed is equivalent to:

secret.txt

and so the application's defence is defeated.

Interestingly, the corresponding code in ASP.NET:

string Filename = Request.Params["filename"];

if (Filename.EndsWith(".jpg"))

{

FileStream fs = File.Open(Filename, FileMode.Open);

...

is not vulnerable to the same attack. Our malicious input results in the following exception:

System.ArgumentException:

Illegal characters in path.

Before our input is passed to the native filesystem APIs, ASP.NET checks whether the managed string contains any invalid characters, including null bytes, and rejects the input if it does. So ASP.NET helps to protect developers against null byte attacks in this instance.

Null byte attacks against LDAP

LDAP is a protocol for querying directory services, and in the context of web applications is most commonly encountered in functionality for searching personnel directories etc. Suppose an application lets us search by name for employees in the Marketing department only. When we supply the input:

John

the application performs an LDAP query with the following filter:

(&(displayName=John)(department=Marketing))

When an LDAP filter combines multiple logical conditions, as here, the boolean operator comes at the start of the list of conditions, and applies to all of the conditions in the list. Hence, there is nothing directly analogous to the "or 1=1" attack in SQL injection. In a conjunctive filter (one employing the boolean AND operator, &) any additional conditions we inject are only able to further restrict the results that will be returned, and cannot undo the restrictions imposed by existing conditions.

On some LDAP platforms, it is possible to supply two filters back-to-back, the second of which is ignored. In this situation, we can use the following crafted input to circumvent the department restriction and view all entries in the directory:

(&(displayName=*))(&(1=1)(department=Marketing))

(See this paper for examples of this kind of attack in action.)

However, some LDAP services, notably Microsoft ADAM (Active Directory Application Mode) do not tolerate queries with two filters. Hence, you may hear it said that LDAP injection into conjunctive filters cannot be usefully exploited against ADAM directories.

This overlooks the possibility of null byte attacks, however. If our query is being passed to ADAM, we can use the following input to circumvent the department restriction and view all entries:

(&(displayName=*))%00)(department=Marketing))

This input does not result in a well-formed LDAP filter, when considered as a managed string. However, because the query is ultimately processed by ADAM in native code, the filter gets truncated to our injected null byte, and so the subsequent conditions in the filter are not processed.

Further, the ASP.NET APIs for querying ADAM, in the System.DirectoryServices namespace, do not block input containing null bytes, in the way that System.IO.File does.

Null byte attacks against XPath

The Web Application Hacker's Handbook includes an example of XPath injection against an application function which retrieves users' credit card numbers based on their username and password (see p316 onwards). If the XML datastore contains entries of the form

<addressBook>

<address>

<name>James Hunter</name>

<password>letmein</password>

<email>james.hunter@pookmail.com</email>

<ccard>8113 5320 8014 3313</creditcard>

</address>

</addressBook>

then a legitimate user's request for their credit card number will result in this XPath query:

/addressBook/address[name='James Hunter' and

In the book, we described how an attacker could retrieve a list of credit card numbers for all users with input like:

/addressBook/address[name='James Hunter' and

password='' or 'a'='a']/ccard

and could perform various blind attacks to extract other information from the datastore one bit at a time, in the manner of Absinthe for blind SQL injection.

However, none of these attacks involved subverting the /ccard attribute in the application's query. Hence, the ccard data field was the only item we could retrieve directly, and we could infer other data, such as names and passwords, only by manipulating the query filter to return either a credit card number or otherwise, based on a controllable condition.

Again, what was overlooked here was the possibility of a null byte attack. In fact, we can supply the following input to effectively replace the ccard attribute with one of our own:

/addressBook/address[name='James Hunter' and

This technique enables us to fully subvert both the filter and attributes of the query, and directly retrieve data such as names and passwords which we could otherwise infer only using cumbersome blind techniques.

As previously, common managed APIs for performing XPath queries, such as those in the .NET System.Xml.XPath namespace, do not block input containing null bytes, and yet are ultimately implemented in native code in which our input gets terminated at the null byte.

xpath

ldap

null bytes

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
