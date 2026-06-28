# [MoBP] Flexible redirection

Source: https://portswigger.net/blog/mobp-flexible-redirection
Fetched: 2026-06-28T09:15:20.450315+00:00

[MoBP] Flexible redirection

Dafydd Stuttard |

Thursday, 27 November 2008 at 07:22 UTC

MoBP

burp

Burp currently lets you configure Intruder and Repeater to automatically follow redirects to targets on the same host and port. This restriction to on-site URLs was implemented to prevent you from inadvertently attacking third-party web sites, by following off-site redirectors which relayed your attack payloads in the redirection URL.

However, you often need more flexibility than this restriction allows. For example, if you are performing a brute force attack against a login request which uses HTTPS, you may be redirected to an HTTP URL to receive the login result. Alternatively, if the application uses single sign-on, you may submit credentials to a central authentication host, and need to follow a redirection back to the actual application to determine the result of each login attempt. In larger applications, you may be redirected between different hosts for all kinds of reasons.

In other situations, you may only be following redirects on the same host, but need more fine-grained control over which you follow. For example, if you are fuzzing a interesting function, you may be redirected sometimes to a dynamic error page, and sometimes to the logout function. You will want Intruder to follow redirects to the error page, to harvest error messages, but avoid redirects to the logout function, which would kill your session.

In the new release, Burp gives you full control over how redirects are followed, enabling you to work effectively in these situations. You can tell Burp to follow only on-site redirects, or only in-scope redirects, or to follow every redirect, or none of them:

The "in-scope" option is normally the easiest way to ensure that you follow relevant redirects while avoiding inappropriate ones. If you have configured the suite-wide target scope correctly, then simply selecting this option within Repeater or Intruder will be right for you, and Burp will only follow redirects to the hosts and URLs that you are willing to attack.

MoBP

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
