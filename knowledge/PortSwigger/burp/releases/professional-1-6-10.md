# Professional 1.6.10

Source: https://portswigger.net/burp/releases/professional-1-6-10
Fetched: 2026-06-28T09:16:27.091811+00:00

This release contains various enhancements and fixes.

Site map performance has been considerably improved, particularly in relation to loading state files and adjusting the view filter.

Some new Scanner checks have been added:

Server-side include (SSI) injection

Server-side Python code injection

Leaked RSA private keys

Duplicate cookies set

Improvements have been made to several existing Scanner checks, including cross-site scripting and server-side code injection.

A new option provides a workaround for a Java SSL problem. As of Java 7, the SSL Server Name Indication (SNI) extension is implemented and enabled by default. Some misconfigured web servers with SNI enabled send an "Unrecognized name" warning in the SSL handshake. Whilst browsers ignore this warning, the Java implementation does not, and fails to connect. Many users have been setting a command line option to disable the SNI extension, but there is now a UI option to do this, at Options / SSL / SSL Negotiation. Changes to this option take effect when you restart Burp.

The following new Burp Extender APIs have been added to help authors who are writing extensions that may appear in the BApp Store:

String getExtensionFilename();

boolean isExtensionBapp();

A number of bugs have been fixed, including:

A bug affecting the execution of some macros that update multiple request parameters.

A bug causing the sessions tracer to sometimes show the incorrect request when a redirect has been followed.

A bug which caused Burp's check for updates not to honor the configured upstream proxy settings.
