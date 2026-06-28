# Professional 1.5.02

Source: https://portswigger.net/burp/releases/professional-1-5-02
Fetched: 2026-06-28T09:16:24.702375+00:00

This release adds native support for Burp extensions written in Ruby. To use this feature, you'll need to download JRuby, and either configure the location of the JRuby JAR file within the Extender options, or load the JRuby JAR file on startup via the Java classpath.

The code for the following sample extensions has been updated to include versions written in Ruby, which you can use as a template for your own extensions if you wish:

Hello World

Event listeners

Traffic redirector

Custom logger

[As with the Python examples, I'm new to Ruby, so apologies if the code isn't to your taste.]

This is still a beta release, pending feedback about the new extensibility framework.
