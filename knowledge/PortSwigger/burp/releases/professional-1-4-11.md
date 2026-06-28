# Professional 1.4.11

Source: https://portswigger.net/burp/releases/professional-1-4-11
Fetched: 2026-06-28T09:16:24.194665+00:00

This release fixes a number of bugs and stability issues, mainly arising from the recent new user interface:

Various causes of UI deadlock when modifying the site map tree and active scan queue have been resolved.

A bug has been fixed when manually adding payloads to the Intruder preset list (and elsewhere), where hitting enter to add an item to the list caused the text field to become unstable.

A bug in Intruder, where exporting selected result rows from a reordered table caused the wrong rows to be saved, has been fixed.

A bug in the handling of built-in world lists in the Content Discovery function has been fixed.

A bug has been fixed in the ViewState renderer, where the root tree node, including the ViewState version and MAC status, was hidden.

A bug in Intruder, where modifying a live attack config and then repeating the attack caused the original config to be used, has been fixed.

A bug in tab renaming (Intruder and Repeater) which sometimes caused the cursor and modified text to disappear, has been fixed.

An accidental change made to the use of the Burp Extender API processHttpMessage(), where the tool name became capitalized, has been reversed.

An occasional bug in the active scan queue where restoring state caused some scan threads to become stalled has been fixed.

Column reordering is re-enabled in the Proxy history.

Burp Sequencer's behavior has been modified when handling samples whose character set size is not a round value of 2^N. Previously, these partial bits of entropy were rounded down to the nearest bit, resulting in some original data being lost, and the likely introduction of bias into the remaining data. In this situation, Burp now transforms the input data so that it uses a round 2^N-sized character set without losing any original data (partial bits are merged into the whole bits at the same character position). No solution to this problem is going to be perfect, but in most cases the new algorithm markedly improves Sequencer's accuracy.

A new feature has been added to optionally prevent Burp from saving configured passwords in persisted settings or state files. If this setting is used, then the user is prompted for the required passwords when Burp is launched, or the state file is restored.
