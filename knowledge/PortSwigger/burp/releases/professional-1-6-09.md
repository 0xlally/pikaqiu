# Professional 1.6.09

Source: https://portswigger.net/burp/releases/professional-1-6-09
Fetched: 2026-06-28T09:16:26.567758+00:00

This release fixes a problem affecting some users of 32-bit systems with the new handling of temporary files that was introduced in v1.6.08.

When the temporary file store grows sufficiently large, some users of 32-bit systems have experienced out-of-memory errors with v1.6.08 of Burp. The new release reverts to the old handling of temporary files for users of 32-bit systems.

In the near future, we are planning to release some powerful new features in Burp which will only be properly supported on 64-bit systems. We recommend that any Burp users who are still using 32-bit editions of their operating system or Java should upgrade to 64-bit editions.
