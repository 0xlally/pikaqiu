# React Server Components remote code execution (React2Shell)

Source: https://portswigger.net/kb/issues/00101200_react-server-components-remote-code-execution-react2shell
Fetched: 2026-06-28T09:17:07.266692+00:00

Support Center

Issue Definitions

React Server Components remote code execution (React2Shell)

React Server Components remote code execution (React2Shell)

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: React Server Components remote code execution (React2Shell)

The application is vulnerable to CVE-2025-55182 (React) and CVE-2025-66478 (Next.js), critical Remote Code Execution vulnerabilities in React Server Components with CVSS score of 10.0.

Vulnerability Overview:

Unauthenticated Remote Code Execution via insecure deserialization

The RSC Flight protocol fails to validate property existence in colon-delimited references

Malformed multipart form-data triggers unhandled exceptions leading to RCE

No prerequisites or special configuration required for exploitation

Remediation: React Server Components remote code execution (React2Shell)

CRITICAL - Immediate Action Required

This vulnerability allows unauthenticated attackers to execute arbitrary code on the server. Patch immediately.

Upgrade to Patched Versions:

React: 19.0.1, 19.1.2, or 19.2.1

Next.js: 15.0.5, 15.1.9, 15.2.6, 15.3.6, 15.4.8, 15.5.7, or 16.0.7

Remediation Steps:

Update package.json dependencies to patched versions

Run: npm install or npm update

Rebuild and redeploy application

Verify fix by re-scanning

References

Next.js Security Advisory

CVE-2025-55182 Details

Detection of CVE-2025-55182

Vulnerability classifications

CWE-502: Deserialization of Untrusted Data

Typical severity

High

Type index (hex)

0x00101200

Type index (decimal)

1053184

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Burp Scanner

This issue - and many more like it - can be found using our

web vulnerability scanner

Read more

Get Burp

Scan your web application from just $499.00

Find out more
