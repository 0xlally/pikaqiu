# Response extraction rules

Source: https://portswigger.net/burp/documentation/desktop/settings/response-extraction
Fetched: 2026-06-28T09:15:55.929078+00:00

Support Center

Documentation

Desktop editions

Settings

Response extraction rules

ProfessionalCommunity Edition

Response extraction rules

Last updated:

June 18, 2026

Read time:

2 Minutes

Response extraction rules are used in various locations within Burp, to define the location within a response of a varying item that needs to be extracted. They are used to identify a custom session token in Sequencer, define an extract grep item in Intruder, and specify the location of a custom parameter value in a macro.

Because response extraction rules are designed to extract the same item from multiple responses that may differ in various ways, Burp provides very flexible ways of specifying the item's location.

The dialog to define an extraction rules shows the current configuration in the top panels, and a sample response in the lower panel. If the response has not yet been fetched from the target application, you can click the Fetch response to do this.

The easiest way to specify the item's location is simply to select it within the sample response. Provided the box Update config based on selection below is checked, Burp will then automatically create a suitable configuration in the top panels.

In some situations, you may need to modify the configuration manually, to ensure that it works when different responses are received. The available options are described below.

Define start and end

This option lets you define the start and end points of the item to be extracted:

Start after expression - You can specify a literal expression that precedes the item you want to extract. You can use escape sequences to represent non-printing characters: \r represents CR, \n represents LF, \xNN represents the character with ASCII hex code NN, and \\ represents a literal backslash.

Start at offset - You can specify a fixed offset into the response where the item begins.

End at delimiter - You can specify a literal expression that follows the item you want to extract. You can use the same escape sequences as described for Start after expression.

End at fixed length - You can specify a fixed length that should be extracted from the start of the item.

Define from regex group

You can specify a regular expression containing a group, and the contents of the group will be extracted, if matched. For example, you could extract the contents of the HTML title tag using:

<title>(.*?)</title>

Or you could extract the first 6-digit number that appears in the response using:

(\d\d\d\d\d\d)

Testing your configuration

When you manually modify the configuration in the upper panels, Burp automatically highlights within the response the item that will be extracted (if any).

When you have completed the configuration, you can click the Refetch response button a few times to test the configuration. Burp will then refetch the response and automatically highlight the item that will be extracted, so that you can confirm that the configuration is working as intended.
