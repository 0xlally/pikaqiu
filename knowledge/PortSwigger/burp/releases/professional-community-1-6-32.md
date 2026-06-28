# Professional / Community 1.6.32

Source: https://portswigger.net/burp/releases/professional-community-1-6-32
Fetched: 2026-06-28T09:16:30.715582+00:00

This release introduces a brand new tool: Burp Clickbandit.

Burp Clickbandit is a tool for generating clickjacking attacks. When you have found a web page that may be vulnerable to clickjacking, you can use Burp Clickbandit to create an attack, to confirm that the vulnerability can be successfully exploited.

Burp Clickbandit is built in pure JavaScript, and is easy to use. In Burp, go to the Burp menu and choose "Burp Clickbandit". Copy the script to your clipboard, and paste it into the web developer console in your browser. It works on all modern browsers except for Microsoft IE and Edge.

For more details about how Burp Clickbandit works and how to use it, see the blog post.

This release also adds the following enhancements:

There is a new option in the Proxy to set the "Connection: close" header on incoming requests. Setting this header in requests can speed up the processing of the resulting responses from some target servers. The new option is on by default.

When generating the CA certificate used by the Proxy, Burp now uses a 2048-bit key if that is supported by the platform, and fails over to a 1024-bit key if not. Some modern clients are rejecting certificates that use a key length shorter than 2048 bits. If you encounter this problem, you can tell Burp to generate a new CA certificate at Proxy / Options / Proxy Listeners / Regenerate CA certificate, and you will need to install the regenerated certificate in your browser in the normal way.
