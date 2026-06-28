# Professional 1.5.04

Source: https://portswigger.net/burp/releases/professional-1-5-04
Fetched: 2026-06-28T09:16:27.583943+00:00

This release adds an in-tool repository for the new extensibility APIs. The Extender / APIs tab lists all of the interfaces available in the current build of Burp, and lets you browse these and save the interface and Javadoc files locally.

Various updates have been made to the draft extensibility API, based on user feedback:

IBurpExtenderCallbacks has two new methods, saveExtensionSetting() and loadExtensionSetting(), which extensions can use to persist configuration settings across reloads of the extension and of Burp.

You can now register an IScopeChangeListener to be notified when changes occur to the suite-wide target scope.

There is a new ICookie interface, for holding details of HTTP cookies.

IResponseInfo has a new method, getCookies(), which you can use to obtain details of any cookies that were issued in a response.

IRequestInfo has a new method, getBodyEncoding(), which you can use to determine the encoding used for the message body (URL, multipart, XML etc). Extensions that provide custom scanner checks can use this method to determine the appropriate encoding to apply to attack payloads that are being placed into insertion points in the request body.

IBurpExtenderCallbacks has two new methods, getCookieJarContents() and updateCookieJar(), which extensions can use to query and update Burp's session handling cookie jar, for use when dealing with unusual session handling mechanisms.

The IBurpExtenderCallbacks method customizeUiComponent() now cascades the action automatically to child components, to reduce the number of calls that you need to make to this method.

The IIntruderPayloadGeneratorFactory method createNewInstance() now receives an instance of a new interface, IIntruderAttack, which the extension can use to obtain details about the Intruder attack in which the payload generator will be used.

The last point is the only case where a method signature within the draft API has actually changed (as opposed to new methods and interfaces being added), so hopefully there are mininal effects on any extensions that people have created using the draft API.

The new API is now "final", in the sense that we only anticipate making small incremental changes to the API for the foreseeable future, and those changes should be backwards compatible.

The final API and links to all the sample extensions are available here.
