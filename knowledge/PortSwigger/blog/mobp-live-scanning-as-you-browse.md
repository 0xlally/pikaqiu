# [MoBP] Live scanning as you browse

Source: https://portswigger.net/blog/mobp-live-scanning-as-you-browse
Fetched: 2026-06-28T09:15:22.295388+00:00

[MoBP] Live scanning as you browse

Dafydd Stuttard |

Thursday, 20 November 2008 at 07:29 UTC

MoBP

burp

Pen Testing

scanners

On Monday, I described one way in which Burp Scanner can integrate with the actions you carry out when testing an application - you can select individual requests and send them for active or passive scanning. There are several other ways too.

You can configure Burp Scanner to automatically scan selected requests while you are browsing an application. When running in this mode, each unique request (based on URL and parameter names) that you make via Burp Proxy is sent for scanning without any action by you. You can configure different settings for active and passive scanning, and you can use the suite-wide target scope, or define a custom scope for each kind of scan. Below, we have configured Burp to actively scan every request we make to www.myapp.com, with the exception of login requests, and to passively scan every request we make to any destination whatsoever:

When you use the live scanning feature, you will see the scanner tab flash each time a vulnerability is identified (with a colour indicating the severity of the issue). All you need to do is browse around the application's content in the normal way, and Burp will check for vulnerabilities whose detection can be reliably automated, leaving you to focus on test activities that require human intelligence to perform.

Configuring Burp to perform live passive scanning of every request you make is particularly interesting. As you browse around random sites on the web, you will see the scanner tab constantly flashing with issues that have been identified without sending a single malicious request:

A further way in which you can initiate scans against interesting targets is via the target site map. After you have browsed around an application, and built up the site map with all of its content, you can select hosts and folders within the tree view to perform active or passive scans of the entire branch. Or you can select multiple items within the table view to do the same:

Used in the ways described, Burp Scanner gives you fine-grained control over everything that it does, and fits right in to your existing testing activities. It lets you prioritise areas of an application that interest you, by browsing them using live scanning, or selecting them for scanning from the site map. And it provides immediate feedback about those areas to inform your manual testing actions.

MoBP

burp

Pen Testing

scanners

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
