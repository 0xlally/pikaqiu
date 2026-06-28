# Testing for SSRF with Burp Suite

Source: https://portswigger.net/burp/documentation/desktop/testing-workflow/vulnerabilities/ssrf/testing-for-ssrf
Fetched: 2026-06-28T09:16:01.766529+00:00

Support Center

Documentation

Desktop editions

Testing workflow

Testing for vulnerabilities

Testing for SSRF vulnerabilities

Testing for SSRF

ProfessionalCommunity Edition

Testing for SSRF with Burp Suite

Last updated:

June 18, 2026

Read time:

2 Minutes

Server-side request forgery (SSRF) is a web security vulnerability that allows an attacker to induce the server-side application to make requests to an unintended location.

SSRF vulnerabilities may enable you to communicate with back-end systems that are not normally publicly available via a compromised server. This is often done via non-routable private IP addresses. You can use Intruder to enumerate these IP addresses and potentially gain access to these back-end systems.

Before you test for SSRF, you need to identify a suitable attack vector. This could be a request with a parameter that contains a full or partial URL, for example. To learn more about identifying SSRF attack surface, see Finding hidden attack surface for SSRF vulnerabilities.

Steps

You can follow along with the process below using the Basic SSRF against a backend system lab from our Web Security Academy.

Identify a request that appears to both:

Cause data to be fetched from another backend system

Use a user-controllable input to determine where this data is fetched from

In the lab, you can use the stock check feature and its stockApi parameter.

Send the relevant request to Intruder.

Add a suitable payload position that will allow you to probe for internal IP addresses or private hostnames. In the case of the lab, you know that the IP address falls within the range 192.168.0.0/24. You can add the payload to the last octet in the IP address as follows: 192.168.0.§0§:8080

Modify the path to point to the root and remove the query and fragment strings if present. In the lab, this would result in stockApi=192.168.0.§0§:8080/

Use Intruder to look for internal IP addresses or private host names that give a different response. In the lab, you can do this as follows:

Make sure that Sniper attack is selected.

In the Payloads side panel, set the Payload type to Numbers.

Set From to 1, To to 255, and Step to 1.

Click Start attack.

Check the results, and look for payloads that return a different status code or length.

Related pages

You can also use Intruder to look for directories, if you find an interesting internal IP address or private host name. For more information, see Burp Intruder.
