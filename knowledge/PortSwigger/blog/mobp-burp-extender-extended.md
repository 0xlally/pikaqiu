# [MoBP] Burp Extender extended

Source: https://portswigger.net/blog/mobp-burp-extender-extended
Fetched: 2026-06-28T09:15:19.990652+00:00

[MoBP] Burp Extender extended

Dafydd Stuttard |

Tuesday, 25 November 2008 at 07:12 UTC

MoBP

burp extender

burp

Burp Extender is an interface which allows third-party code to extend Burp's functionality. As it currently stands, the interface is fairly basic, but several people have used it to do cool stuff. I would like to see this interface get a lot more sophisticated, and the new release sees a step in this direction.

The IBurpExtender interface now has a new method:

public void registerExtenderCallbacks

(burp.IBurpExtenderCallbacks callbacks);

This is invoked on startup, and passes to implementations an instance of the new IBurpExtenderCallbacks interface, which provides methods that may be used by the implementation to perform various actions. The IBurpExtenderCallbacks interface currently looks like this, but it may change slightly before release:

package burp;

public interface IBurpExtenderCallbacks

{

public byte[] makeHttpRequest(

String host,

int port,

boolean useHttps,

byte[] request) throws Exception;

public void sendToRepeater(

String host,

int port,

boolean useHttps,

byte[] request,

String tabCaption) throws Exception;

public void sendToIntruder(

String host,

int port,

boolean useHttps,

byte[] request) throws Exception;

public void sendToSpider(

java.net.URL url) throws Exception;

public void doActiveScan(

String host,

int port,

boolean useHttps,

byte[] request) throws Exception;

public void doPassiveScan(

String host,

int port,

boolean useHttps,

byte[] request,

byte[] response) throws Exception;

public void issueAlert(String message);

}

As you can see, the new methods enable you to pro-actively interface with several of the Burp tools. Note that the new way of making HTTP requests replaces the old, rather clunky method, so anyone who has used the old method will need to tweak their code a little.

The next phase of development for Burp Extender will see several new ways in which Burp can call out to your code, to enable custom implementations of key tasks. Unfortunately, these are unlikely to make an appearance in the forthcoming release, but they are on the list for the future:

Methods like the existing processProxyMessage method, but for other tools. These will enable custom modifications of HTTP requests and responses. So, for example, if you are using Intruder against an application which employs an unusual session handling mechanism, you can write a request preprocessor to log in a new session and add the relevant tokens to the request.

When sending a request to Intruder, a method to specify custom payload positions. This will enable implementations to handle custom data formats and place attack payloads in locations that are applicable to that format.

During Intruder attacks, a method to perform custom manipulation of attack payloads prior to placement in requests. Also a method to process responses and return custom result information which will appear in the attack UI.

When the Spider is parsing response content for links, a method to perform custom parsing and return a list of discovered URLs.

If anyone has further suggestions for extensibility, do let me know.

MoBP

burp extender

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
