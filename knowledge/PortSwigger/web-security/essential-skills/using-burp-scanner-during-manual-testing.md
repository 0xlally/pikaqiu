# Using Burp Scanner during manual testing

Source: https://portswigger.net/web-security/essential-skills/using-burp-scanner-during-manual-testing
Fetched: 2026-06-28T09:17:49.399853+00:00

Web Security Academy

Essential skills

Using Burp Scanner during manual testing

Using Burp Scanner during manual testing

In this section, we'll show you a number of ways you can optimize your manual testing workflow by using Burp Scanner to supplement your own knowledge and intuition. Not only will this help you cover more ground, you'll be able to spend your time where it matters rather than on tedious preliminary work.

Scanning a specific request

When you come across an interesting function or behavior, your first instinct may be to send the relevant requests to Repeater or Intruder and investigate further. But it's often beneficial to hand the request to Burp Scanner as well. It can get to work on the more repetitive aspects of testing while you put your skills to better use elsewhere.

If you right-click on a request and select Do active scan, Burp Scanner will use its default configuration to audit only this request.

This may not catch every last vulnerability, but it could potentially flag things up in seconds that could otherwise have taken hours to find. It may also help you to rule out certain attacks almost immediately. You can still perform more targeted testing using Burp's manual tools, but you'll be able to focus your efforts on specific inputs and a narrower range of potential vulnerabilities.

Even if you already use Burp Scanner to run a general crawl and audit of new targets, switching to this more targeted approach to auditing can massively reduce your overall scan time.

Scanning custom insertion points

It's easy to see the benefits of limiting your scans to a single request, but you can take this a step further by only testing specific inputs within that request. You can do this from the message editor.

Highlight the insertion point you're interested in, then right-click and select Scan selected insertion point.

This lets you focus on the input that you're interested in, instead of scanning additional content that you know is unlikely to be useful.

Although you can just define a single insertion point using Intruder, it's often quicker to use the Scan manual insertion point extension. You can highlight any sequence of characters within the request, typically a parameter value, and select Extensions > Scan manual insertion point from the context menu.

This approach can yield results incredibly quickly, giving you something to work with in just a couple of seconds. It also means you can choose to scan inputs that Burp Scanner normally doesn't use, such as custom header values.

Scanning non-standard data structures

As you're free to define insertion points in arbitrary positions, you can also target a specific substring within a value. Among other things, this can be useful for scanning non-standard data structures.

When dealing with common formats, such as JSON, Burp Scanner is able to parse the data and place payloads in the correct positions without breaking the structure. However, consider a parameter that looks something like this:

user=048857-carlos

Using our intuition, we can take a guess that this will be treated as two distinct values by the back-end: an ID of some kind and what appears to be a username, separated by a hyphen. However, Burp Scanner will treat this all as a single value. As a result, it will just place payloads at the end of the parameter, or replace the value entirely.

To help scan non-standard data structures, you can scan a single part of a parameter. In this example you may want to target carlos. You can highlight carlos in the message editor, then right-click and select Scan selected insertion point.

You can also use Intruder to define multiple insertion points. In the example above, you can define insertion points for 048857 and carlos, then right-click and select Scan defined insertion points.

Burp Suite essential skills

Try for free
