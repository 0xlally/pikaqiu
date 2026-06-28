# OS command injection

Source: https://portswigger.net/kb/issues/00100100_os-command-injection
Fetched: 2026-06-28T09:17:05.158661+00:00

Support Center

Issue Definitions

OS command injection

OS command injection

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

What is OS command injection?

OS command Injection is a critical vulnerability that allows attackers to gain complete control over an affected web site and the underlying web server.

OS command injection vulnerabilities arise when an application incorporates user data into an operating system command that it executes. An attacker can manipulate the data to cause their own commands to run. This allows the attacker to carry out any action that the application itself can carry out, including reading or modifying all of its data and performing privileged actions.

In addition to total compromise of the web server itself, an attacker can leverage a command injection vulnerability to pivot the attack in the organization's internal infrastructure, potentially accessing any system which the web server can access. They may also be able to create a persistent foothold within the organization, continuing to access compromised systems even after the original vulnerability has been fixed.

Description: OS command injection

Operating system command injection vulnerabilities arise when an application incorporates user-controllable data into a command that is processed by a shell command interpreter. If the user data is not strictly validated, an attacker can use shell metacharacters to modify the command that is executed, and inject arbitrary further commands that will be executed by the server.

OS command injection vulnerabilities are usually very serious and may lead to compromise of the server hosting the application, or of the application's own data and functionality. It may also be possible to use the server as a platform for attacks against other systems. The exact potential for exploitation depends upon the security context in which the command is executed, and the privileges that this context has regarding sensitive resources on the server.

Remediation: OS command injection

If possible, applications should avoid incorporating user-controllable data into operating system commands. In almost every situation, there are safer alternative methods of performing server-level tasks, which cannot be manipulated to perform additional commands than the one intended.

If it is considered unavoidable to incorporate user-supplied data into operating system commands, the following two layers of defense should be used to prevent attacks:

The user data should be strictly validated. Ideally, a whitelist of specific accepted values should be used. Otherwise, only short alphanumeric strings should be accepted. Input containing any other data, including any conceivable shell metacharacter or whitespace, should be rejected.

The application should use command APIs that launch a specific process via its name and command-line parameters, rather than passing a command string to a shell interpreter that supports command chaining and redirection. For example, the Java API Runtime.exec and the ASP.NET API Process.Start do not support shell metacharacters. This defense can mitigate the impact of an attack even in the event that an attacker circumvents the input validation defenses.

References

Web Security Academy: OS command injection

Vulnerability classifications

CWE-77: Improper Neutralization of Special Elements used in a Command ('Command Injection')

CWE-78: Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection')

CWE-116: Improper Encoding or Escaping of Output

CAPEC-248: Command Injection

Typical severity

High

Type index (hex)

0x00100100

Type index (decimal)

1048832

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
