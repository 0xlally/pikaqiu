# Draft new extensibility API

Source: https://portswigger.net/blog/draft-new-extensibility-api
Fetched: 2026-06-28T09:15:14.879874+00:00

Draft new extensibility API

Dafydd Stuttard |

Monday, 10 December 2012 at 13:46 UTC

burp extender

burp

The new Burp Suite extensibility framework employs a much improved API. This allows extensions to integrate much more deeply with Burp's internals, and customize Burp in ways that were previously not possible. It is also hopefully much easier for users with limited programming experience.

This post contains a brief summary of the key highlights in the new API. There are links at the end to the full interface files and API documentation.

Note: The new API is currently in draft form and is subject to change.

Event listeners

Extensions can register listeners for key runtime events:

void registerProxyListener(IProxyListener listener);

void registerHttpListener(IHttpListener listener);

void registerScannerListener(IScannerListener listener);

void registerExtensionStateListener(

IExtensionStateListener listener);

This was previously achieved by implementing specific methods directly within the main BurpExtender class, but the new technique is more flexible.

User interface

Extensions can add their own tabs to Burp’s main window:

void addSuiteTab(ITab tab);

Extensions can create instances of Burp’s HTTP message editor, for use in their own UI:

IMessageEditor createMessageEditor(

IMessageEditorController controller, boolean editable);

Extensions can create their own UI components and have Burp customize them according to Burp’s current UI configuration (font size, etc.):

void customizeUiComponent(Component component);

Extensions can add their own items to the context menus that appear throughout Burp:

void registerContextMenuFactory(IContextMenuFactory factory);

With the new menu support, menu items can be generated contextually, based on:

Location of the menu invocation

Any selected HTTP messages or Scanner issues

Any selected text

Editability

In editable contexts, menu items can drive changes to the underlying message.

Extensions can add their own tabs to message editors everywhere, to allow custom in-place rendering and editing of HTTP messages:

void registerMessageEditorTabFactory(

IMessageEditorTabFactory factory);

This lets extensions handle unusual serialization formats without needing to unpack / repack messages by hooking into the HTTP stack.

Per-extension output and error streams are available:

OutputStream getStdout();

OutputStream getStderr();

The Burp user can choose whether to direct these streams to the extension’s UI (in the Extender tab), or to file, or to the Java system console.

Scanner integration

Extensions can register to provide custom scanner insertion points, for use in active scanning:

void registerScannerInsertionPointProvider(

IScannerInsertionPointProvider provider);

For each actively scanned request, Burp will ask the extension to provide insertion points that should be used:

public interface IScannerInsertionPointProvider

{

List<IScannerInsertionPoint> getInsertionPoints(

IHttpRequestResponse baseRequestResponse);

}

The custom scanner insertion point handles the generation of requests during scanning:

public interface IScannerInsertionPoint

{

String getInsertionPointName();

String getBaseValue();

byte[] buildRequest(byte[] payload);

int[] getPayloadOffsets(byte[] payload);

byte getInsertionPointType();

}

This lets extensions parse unusual serialized data formats, and make these available for effective scanning by Burp's native scan engine.

Extensions can add their own scanner checks:

void registerScannerCheck(IScannerCheck check);

Burp will invoke each registered check at the appropriate points during active and passive scanning, and the extension can report its own scan issues:

public interface IScannerCheck

{

List<IScanIssue> doPassiveScan(

IHttpRequestResponse baseRequestResponse);

List<IScanIssue> doActiveScan(

IHttpRequestResponse baseRequestResponse,

IScannerInsertionPoint insertionPoint);

}

In active scanning, the insertion point handles the task of building HTTP requests containing your check’s payloads.

Intruder integration

Extensions can provide custom payload generators, which the user can then select from the Intruder payloads UI:

void registerIntruderPayloadGeneratorFactory(

IIntruderPayloadGeneratorFactory factory);

Extensions can provide custom payload processors, which the user can invoke for any payload type:

void registerIntruderPayloadProcessor(

IIntruderPayloadProcessor processor);

These methods allow extensions to deal with arbitrarily complex custom data formats, using Intruder's attack engine to manipulate data deep within serialized objects or other structures.

Session handling integration

Extensions can register their own session handling actions:

void registerSessionHandlingAction(

ISessionHandlingAction action);

The Burp user can create rules which invoke a custom action, either on the current base request, or following execution of a macro:

public interface ISessionHandlingAction

{

public void performAction(

IHttpRequestResponse currentRequest,

IHttpRequestResponse[] macroItems);

}

Custom session handling actions can issue their own requests if needed, and modify the base request as appropriate. This lets extensions work with arbitrarily complex session handling mechanisms, for example:

Where the parameters used for session tokens have changing names

Chaining tokens from prior responses made by any tool

Addition of timestamps, hashes, etc.

Modifying tokens inside serialized data

Helper methods

Burp provides a set of helper methods for tasks that frequently arise when writing a Burp extension, including:

Analysis of HTTP messages for headers, parameters, etc.

Decoding and encoding in common schemes.

Conversion of data between String and byte[] forms.

Searching for an expression within binary data.

Building HTTP messages based on URL, headers, body content, parameters etc.

Manipulation of parameters within HTTP requests.

These helpers are available via the new IExtensionHelpers interface. They will hopefully make the task of writing an extension much easier for users with limited programming experience.

Backwards compatibility

An objective for the new extensibility framework was to preserve backwards compatibility as far as possible. This has been largely achieved, although some compromises have been necessary, in the interests of easier development of new extensions.

All legacy extensions (compiled against the old interfaces) should be binary compatible with the new framework. In other words, you should be able to dynamically load existing JAR files into Burp via the Extender tool, and they should work exactly the same as previously.

If legacy extension code is compiled against the new interfaces, then some minor changes will be necessary for some extensions. This affects some usages of the IHttpRequestResponse and IScanIssue interfaces. These interfaces previously contained get/set methods for the server host, port and protocol, and also helper methods for obtaining the request URL and the response status code. These methods have now been removed, and the following replacements should be used instead:

There are new get/set methods using the new IHttpService interface to access all server details as a single object.

The request URL and response status code details are easily accessible for any HTTP request or response, via the helper methods in the new IExtensionHelpers interface.

The reason for actually removing the legacy methods from these interfaces (rather than deprecating them) is that in various new APIs, extensions must provide their own implementations of the IHttpRequestResponse and IScanIssue interfaces. Removing the superfluous methods altogether means that extensions won't need to provide dummy implementations of them.

Now, in order to achieve binary compatibility with legacy extensions, Burp does actually implement the removed methods in any instances of those interfaces that it itself generates and passes to extensions. Hence, if you really want to compile against the new interfaces without changing your legacy code, you can add the removed methods back to the new interface files and continue using them. But that isn't recommended.

Additionally, a small number of legacy methods are still present in the new interfaces but have been deprecated because superior alternatives are now available.

Full code and documentation

You can download the source code to the new interfaces, and browse the full Javadoc here.

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
