# Lab: Bypassing access controls using email address parsing discrepancies

Source: https://portswigger.net/web-security/logic-flaws/examples/lab-logic-flaws-bypassing-access-controls-using-email-address-parsing-discrepancies
Fetched: 2026-06-28T09:17:55.001889+00:00

Web Security Academy

Business logic vulnerabilities

Examples

Lab

Lab: Bypassing access controls using email address parsing discrepancies

This lab validates email addresses to prevent attackers from registering addresses from unauthorized domains. There is a parser discrepancy in the validation logic and library used to parse email addresses.

To solve the lab, exploit this flaw to register an account and delete carlos.

Required knowledge

To solve this lab, you'll need to understand the techniques described in the Splitting the Email Atom: Exploiting Parsers to Bypass Access Controls whitepaper by Gareth Heyes of the PortSwigger Research team.

Solution

Identify the registration restriction

Open the lab and click Register.

Attempt to register an account with the email foo@exploit-server.net.

Notice that the application blocks the request and displays an error message stating that the email domain must be ginandjuice.shop. This indicates the server enforces a domain check during registration.

Investigate encoding discrepancies

Try to register an account with the following email:

=?iso-8859-1?q?=61=62=63?=foo@ginandjuice.shop.

This is the email abcfoo@ginandjuice.shop, with the abc portion encoded using Q encoding, which is part of the "encoded-word" standard.

Notice that the registration is blocked with the error: "Registration blocked for security reasons."

Try to register an account with the following UTF-8 encoded email:

=?utf-8?q?=61=62=63?=foo@ginandjuice.shop.

Notice that the registration is blocked with the same error message. This suggests that the server is detecting and rejecting attempts to manipulate the registration email with encoded word encoding. It is possible that less common encoding formats may not be picked up by the server's validation.

Try to register an account with the following UTF-7 encoded email:

=?utf-7?q?&AGEAYgBj-?=foo@ginandjuice.shop.

Notice that this attempt doesn't trigger an error. This suggests that the server doesn't recognize UTF-7 encoding as a security threat. Because UTF-7 encoding appears to bypass the server's validation, you may be able to use it to craft an attack that tricks the server into sending a confirmation email to your exploit server email address while appearing to still satisfy the ginandjuice.shop domain requirement.

Exploit the vulnerability using UTF-7

Register an account with the following UTF-7 encoded email:

=?utf-7?q?attacker&AEA-[YOUR-EXPLOIT-SERVER_ID]&ACA-?=@ginandjuice.shop.

This is the string attacker@[YOUR-EXPLOIT-SERVER-ID] ?=@ginandjuice.shop, with the @ symbol and space encoded in UTF-7.

Click Email client. Notice that you have been sent a registration validation email. This is because the encoded email address has passed validation due to the @ginandjuice.shop portion at the end, but the email server has interpreted the registration email as attacker@[YOUR-EXPLOIT-SERVER-ID].

Click the confirmation link to activate the account.

Gain admin access

Click My account and log in using the details you registered.

Click Admin panel to access the list of users.

Delete the carlos user to solve the lab.

Find business logic vulnerabilities using Burp Suite

Try for free
