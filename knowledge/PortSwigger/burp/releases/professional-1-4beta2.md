# Professional 1.4beta2

Source: https://portswigger.net/burp/releases/professional-1-4beta2
Fetched: 2026-06-28T09:16:24.669437+00:00

This release fixes a few bugs that were identified in the first beta release, and also adds some new features:

NTLMv2 authentication is now supported, for both web and proxy servers, allowing you to work with Windows servers that do not accept the older version of NTLM.

All relevant Burp features now work with IPv6.

Charsets are now automatically recognised and correctly rendered, per response. This avoids the need to set a specific charset on the command line when starting Burp, and allows you to work with content that uses multiple different charsets within the same instance of Burp. You can override this default behaviour and set a specific charset at options / display / charset handling. Note that some charsets are not supported for all fonts. If you are using a charset that employs non-Latin glyphs, you should first try using a system font such as Courier New or Dialog.

The directory path where Burp saves its temporary files is now configurable, at options / misc / temporary files location. This allows you to specify a directory on a different volume, or which is not world-readable, if required. Changes to this setting take effect the next time Burp starts up.

A new method has been added to IBurpExtenderCallbacks allowing you to programmatically send items to Burp Scanner with custom attack insertion points (in the same way as could already be done from the Intruder UI). The definition of this method is as follows:

public IScanQueueItem doActiveScan(

String host,

int port,

boolean useHttps,

byte[] request,

List<int[]> insertionPointOffsets) throws Exception;

The insertionPointOffsets parameter is a list of index pairs representing the positions of the insertion points that should be scanned. Each item in the list must be an int[2] array containing the start and end offsets for the insertion point.

There is a new EULA, written by a proper lawyer.
