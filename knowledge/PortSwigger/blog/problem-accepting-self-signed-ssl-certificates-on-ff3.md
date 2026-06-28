# Problem accepting self-signed SSL certificates on FF3

Source: https://portswigger.net/blog/problem-accepting-self-signed-ssl-certificates-on-ff3
Fetched: 2026-06-28T09:15:23.958249+00:00

Problem accepting self-signed SSL certificates on FF3

Dafydd Stuttard |

Wednesday, 20 August 2008 at 11:00 UTC

firefox

burp

Firefox 3 changes the default handling of invalid SSL certificates, to make it harder for end users to do things they probably don't want to do. If you have used FF3 to access an HTTPS web site via an intercepting proxy such as Burp, you probably know about this behaviour.

The way the feature is documented, FF3 prevents you from accessing an HTTPS site which uses an invalid SSL certificate (such as a self-signed certificate). In order to access the site, you need to explicitly add an exception, which is more cumbersome than simply clicking a "connect anyway" button. When you use an intercepting proxy, your browser receives the proxy's self-signed SSL certificate, and so you cannot connect without creating an exception.

The problem is that, for many users, the feature is not working as documented. When FF3 receives an invalid SSL certificate, many users are just seeing the following error dialog, with no option to add an exception:

You can try to add an exception manually, by going into Options / Advanced / Encryption / View Certificates / Add Exception ...

However, when you click "Get Certificate", you receive the same error dialog as originally, and the "Confirm Security Exception" button is never enabled.

At this point, there is no clue within the product or documentation about how to fix the problem, and I've spoken to several users who have given up and used another browser.

However, you can fix the problem by tweaking FF3's configuration. Somewhat bizarrely, you need to go to about:config and change the network.dns.disableIPv6 option to true:

Having done this, you will now see a completely different error message when FF3 receives a self-signed SSL certificate:

If you follow the "Or you can add an exception ..." link, then everything works as documented, and you can add an exception for the invalid certificate:

I assume that Firefox will fix this usability issue at some point, but in the meantime, if you have had problems accepting invalid certificates, try disabling IPv6 in the FF3 configuration and see if things start working.

firefox

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
