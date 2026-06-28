# Burp Intruder payload positions

Source: https://portswigger.net/burp/documentation/desktop/tools/intruder/configure-attack/positions
Fetched: 2026-06-28T09:16:04.014493+00:00

Support Center

Documentation

Desktop editions

Tools

Intruder

Configure attack

Positions

ProfessionalCommunity Edition

Burp Intruder payload positions

Last updated:

June 18, 2026

Read time:

2 Minutes

When you send a request to Burp Intruder, a new tab is created containing the request and target details. You can set payload positions anywhere in these fields. These positions determine where Burp Intruder will insert payloads during the attack.

Note

By default, Update Host header to match target is selected. This means that if the target is modified during the attack, the Host header in the base request is automatically updated to match the new target. You can deselect this to amend the target only. This enables you to send an arbitrary Host header to a fixed target, for example to craft an HTTP host header attack.

Each payload position is enclosed by a pair of payload markers §, and highlighted for ease of identification.

Note

The use of the § character as a payload marker is purely visual. This means that any § characters in your request won't define a payload position.

To automatically set a single payload position when you send a request to Burp Intruder, highlight the position value in a message editor anywhere in Burp, then right-click the message and select

Send to Intruder.

In Intruder, you can set and modify payload positions in the following ways:

Add a payload position - Click Add § to place a pair of payload markers in the request. Alternatively, select some text then click Add § to place markers on either side of the text. Payload positions can't overlap.

Remove all payload markers - click Clear §.

If you have selected some text, markers are removed from within the selected area only.

Apply automatic payload markers - click Auto §. Burp inserts automatic payload positions. You can configure whether these replace or append to the base parameter value in the

Settings dialog.

If you have selected some text, automatic markers are placed within the selected area only. For example, if a multipart parameter value contains data in XML or JSON format, you can highlight the formatted data and click Auto § to position payloads within it.

Note

You can also configure a hotkey to add or clear payload positions. For more information, see Hotkey

settings.

During the attack, both the payload markers and any enclosed text are replaced with the payload. If the payload position does not have an assigned payload, the enclosed text is unchanged but the markers are removed.

Note

You can also use Intruder's payload positions as insertion points for Burp Scanner. Configure your payload positions, then click on the top-level Intruder menu and select Scan defined insertion points.

For more information on Burp Scanner insertion points, see Auditing.
