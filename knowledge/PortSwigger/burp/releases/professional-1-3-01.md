# Professional 1.3.01

Source: https://portswigger.net/burp/releases/professional-1-3-01
Fetched: 2026-06-28T09:16:23.093461+00:00

This beta release introduces a large number of new features and other enhancements to Burp Intruder. A brief summary is below - see the online help for full documentation.

Tabbed attack configuration

You can now configure multiple attacks simultaneously in separate numbered tabs, as with Burp Repeater. Each time you send a request to Intruder, this opens a new attack tab. You can also add and delete tabs using the Intruder menu.

You can configure how Burp populates the configuration of each new tab, with three options accessible via the Intruder menu:

use default attack configuration

copy configuration from first tab

copy configuration from last tab

So, for example, you can set up a standard attack configuration in your first attack tab (e.g. for fuzzing parameters and grepping for error messages) and have this configuration copied into a new tab for each request that you send to intruder.

You can also copy attack configurations between tabs, and save and load attack configurations, using the Intruder menu. This enables you to construct various attack configurations optimised for various purposes, and easily load these into Burp for use on different occasions.

Payload positions editor

This panel now uses the same feature-rich request editor as other Burp tools, with quick search, in-place encoding/decoding, undo/redo, and a context menu with useful functions. Binary and non-printing content is now fully supported, with no normalisation of newlines or other characters.

Auto-placement of payload markers can be configured to either replace or append to existing parameter values, via an option in the Intruder menu.

New payload sources

There are three new payload sources:

Character frobber. This operates on the existing base value of each payload position, or on a specified string. It cycles through the base string one character at a time, incrementing the ASCII code of that character by one. This payload source is useful when you are testing which parts of parameter's values have an effect on the application's response (such as portions of complex session tokens).

Bit flipper. This operates on the existing base value of each payload position, or on a specified string. It cycles through the base string one character at a time, flipping each bit in turn. You can configure which bits are to be flipped. You can configure the bit flipper either to operate on the literal base value, or to treat the base value as an ASCII hex string. This payload source can be useful in similar situations to the character frobber but where you need finer-grained control. For example, if session tokens or other parameter values contain meaningful data encrypted with a block cipher in CBC mode, it may be possible to change parts of the decrypted data systematically by modifying bits within the preceding cipher block. In this situation, you can use the bit flipper payload source to determine the effects of modifying individual bits within the encrypted value, and understand whether the application may be vulnerable.

Username generator. This payload source takes human names as input, and generates potential usernames using various common schemes.

New payload processor

The previous simple options for post-processing payloads are replaced with a new rules-based processor which is much more powerful. You can define arbitrarily many rules, which are executed in sequence on each payload. The types of rules available are:

add prefix

add suffix

match/replace

substring (from a specified offset up to a specified length)

reverse substring (as substring, but indexed from the end of the payload)

modify case (same options as for the case substitution payload source)

encode (as URL, HTML, Base64, ASCII hex and constructed strings for various platforms)

decode (as URL, HTML, Base64 and ASCII hex)

hash

addition of raw payload (this can be useful if you need to include the same payload in both raw and hashed form)

New attack options

The following new options are added:

Number of retries on network error.

Wait between retries.

Make unmodified baseline request (for results comparison with actual attack requests).

Store full payloads. This option imposes some memory overhead and is off by default. It may be necessary to turn this on in some situations - for example, if you are using long payloads (truncated in the results UI) and want to access the full values at runtime, for example in order to modify the payload grep configuration, rebuild and issue requests based on a modified request template, or to save the full results table values.

Live attack configuration

The full configuration for each attack is now replicated within the attack results window. All feasible options can be modified in real time, and will take immediate effect within the running attack. This functionality is useful in various situations, for example: you can adjust the thread count to optimise attack speed; you can change grep settings to analyse existing results based on response content you only notice during the running attack; you can edit the base request template to modify your attack. You should use this feature with caution, and consider pausing the attack if making numerous or significant changes.

Attack results

The attack results table adds numerous features that were previously added to other Burp tools, including:

Preview pane

Filter panel

Item annotation with comments and highlights

Fully-featured context menu

Deletion of results

Various other new functionality has also been added with attack results, which is specifically relevant to Burp Intruder:

You can flag individual or multiple results to be reissued. This is useful if intermittent network or application problems have caused some requests to fail. When a request is reissued, Burp will, if possible, rebuild a new request based on the current attack configuration, including the current request template if this has been modified. So if your application session has been terminated during an attack, you can modify the request template to set a new session token, and reissue any affected requests - these will be rebuilt using the new session token and so will be processed within the new application session.

You can select items within the results and add these to the Suite site map. This function is useful if you are manually enumerating application content, and want to populate the site map with the URLs of confirmed content.

If an attack has been configured to follow redirects, the request and response viewer will show all intermediate responses and requests, in addition to the initial request and final response.

Holding down CTRL and clicking a column header label copies the entire contents of that column to the clipboard.
