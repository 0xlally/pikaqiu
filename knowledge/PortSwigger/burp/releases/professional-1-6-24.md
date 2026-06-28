# Professional 1.6.24

Source: https://portswigger.net/burp/releases/professional-1-6-24
Fetched: 2026-06-28T09:16:27.365953+00:00

This release adds a new Scanner check for server-side template injection.

Template engines are widely used by web applications to present dynamic data via web pages and emails. Unsafely embedding user input in templates leads to a vulnerability that is:

frequently critical, allowing full arbitrary code execution on the server; and

easily mistaken for cross-site scripting, which is usually a much less serious issue.

The vulnerability is generic in nature, potentially affecting any web application that uses a template engine in an unsafe way. This can arise both through developer error, and through the intentional exposure of templates in an attempt to offer rich functionality, as is commonly done by wikis, blogs, marketing applications, and content management systems. Many template engines offer a "sandboxed" mode for this purpose, but it is frequently possible to escape from this.

In the course of researching this vulnerability and developing the new Scanner check, we have identified numerous zero-day instances of the vulnerability in real-world, widely-used applications. The exact frequency of the vulnerability is unknown, but we have repeatedly stumbled upon it on penetration testing engagements and have easily located several targets for demonstration. Today, James Kettle from the Burp Suite team has presented the results of this research at the Black Hat security conference.

For full technical details of how this vulnerability can be found and exploited, see our server-side template injection blog post.

The release also adds two other new features:

A new Scanner check for server-side Expression Language injection. From the client-side perspective, server-side Expression Language injection can look similar to server-side template injection. Burp should correctly distinguish between these different vulnerabilities.

A new Intruder payload list for common server-side variables. This list was compiled through analysis of a large quantity of real-world application source code posted on GitHub. As described in the blog post, full exploitation of server-side template injection may involve using brute force to guess the names of variables in use within the template code. The new payload list is useful for this purpose, as well as various others.
