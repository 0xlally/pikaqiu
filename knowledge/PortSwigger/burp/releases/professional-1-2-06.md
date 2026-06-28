# Professional 1.2.06

Source: https://portswigger.net/burp/releases/professional-1-2-06
Fetched: 2026-06-28T09:16:22.416554+00:00

1. Scanner adds support for REST-style parameters in the URL. Some applications use the path portion of the URL to transmit data parameters, for example:

/cars/red/diesel/2004/ShowDetails

If you configure Scanner to attack REST-style parameters, then each of "cars", "red", etc. will be tested for input-based vulnerabilities. This option is off by default, to avoid creating excessive numbers of scan requests if this is not necessary. You should enable this option any time you believe the application may be transmitting data using the REST paradigm.

The rules for defining non-injectable parameters are now extended so you can exclude specific REST parameters by their index number. So, if you know that "cars" is used to define the application path, and is not a data parameter, you can define a rule to skip server-side injection tests for REST parameter 1 (use the index number as the parameter name in the rule).

2. Scanner adds support for fully customisable attack insertion points, so you can specify arbitrary locations within a base request where attack strings should be placed. To use this function, send the relevant base request to Intruder, use the payload positions UI to define the start/end of each insertion point in the usual way, and select the new Intruder menu option "actively scan defined insertion points".

3. Automatic placement of payload positions within Intruder now recognises XML-formatted data within the currently-selected range of the request template. Some applications send XML-encapsulated data within a multipart request body, for example:

POST /function HTTP/1.0

Content-Type: multipart/form-data; boundary=weidhwiderfhwiuehwiuehfwerrf

Content-Length: 202

--weidhwiderfhwiuehwiuehfwerrf

Content-Disposition: form-data; name="data"

<data>

<param1>foo</param1>

<param2>bar</param2>

<param3>123</param3>

</data>

--weidhwiderfhwiuehwiuehfwerrf--

If you perform auto-placement of payload positions on the entire message, then Intruder will mark the whole of the XML block as a single insertion point, which is probably not what you want:

However, if instead you manually select the precise XML block, then the auto-placement function will recognise that the selection contains XML, and will mark the individual XML parameter values as insertion points:

Used in conjunction with scanning of configurable insertion points (see #2), this enables you to quickly scan complex message bodies properly.

4. In any message display you can now copy to file, and (when editable) paste from file, using the right-click context menu. Copying operates on the selected text or, if nothing is selected, the whole message. Pasting replaces the selected text or, if nothing is selected, inserts at the cursor position.

5. When a message is showing in the Proxy intercept tab, you can forward or drop the message using the shortcut keys Alt-F and Alt-D.
