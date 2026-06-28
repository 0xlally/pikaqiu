# Professional 1.5.09

Source: https://portswigger.net/burp/releases/professional-1-5-09
Fetched: 2026-06-28T09:16:25.661109+00:00

This release adds support for PKCS#11 client SSL certificates contained in smart cards and other physical tokens. These can be configured at Options / SSL / Client SSL Certificates.

Key features include:

Ability to configure multiple PKCS#11 and PKCS#12 certificates for use with different hosts (or host wildcard masks) .

Auto-detection of installed PKCS#11 libraries (currently Windows only).

Auto-detection of card slot settings.

Support for OS X, Linux and 32-bit Windows (note that Oracle Java does not currently support PKCS#11 on 64-bit Windows).

Persistence of configuration across reloads of Burp.

Although we have tested the PKCS#11 support using numerous cards on various platforms, please do let us know if you have problems with particular devices.

This release also adds an option to encrypt passwords contained in Burp's configuration options when these are saved in persisted preferences or Burp state files. This option is available via the Burp menu / Remember settings / Passwords, and also within the save state wizard. If the option is selected, Burp will prompt you for a master password with which to encrypt individual passwords. The master password is not saved anywhere. When the settings are later restored, Burp will prompt you for the master password to decrypt the individual passwords. For those who are interested, this feature uses AES encryption with a 128-bit key generated from your password using PKCS#5v2.0.
