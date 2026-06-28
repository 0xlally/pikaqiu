# Professional 1.6.37

Source: https://portswigger.net/burp/releases/professional-1-6-37
Fetched: 2026-06-28T09:16:27.787957+00:00

This release gives the Scanner the capability to report all instances where user input is returned in application responses, both reflected and stored:

The information gathered is primarily of use to manual security testers. Some applications contain numerous instances of input retrieval, since it is very common for the entire URL to be reflected within responses. For these reasons, the new Scanner checks are off by default, but can be turned on in the Scanner options:
