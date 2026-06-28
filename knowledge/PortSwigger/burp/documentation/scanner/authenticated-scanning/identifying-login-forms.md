# Identifying login and registration forms

Source: https://portswigger.net/burp/documentation/scanner/authenticated-scanning/identifying-login-forms
Fetched: 2026-06-28T09:16:10.023489+00:00

Support Center

Documentation

Scanner

Authenticated scanning

Identifying login and registration forms

DASTProfessional

Identifying login and registration forms

Last updated:

June 18, 2026

Read time:

2 Minutes

Burp Scanner's ability to identify login and registration forms is a key part of what makes authenticated scanning in Burp so effective.

When crawling, Burp Scanner first identifies any forms that it believes to be login or registration forms. Any forms meeting all of the following criteria are added to the list:

The form is a standard HTML form.

The form contains an input field with the attribute type=password.

The password field has a non-empty name attribute.

Burp Scanner then attempts to distinguish registration forms from login forms. To do this, it applies a series of ordered criteria.

The registration form is:

Whichever form has the most password fields.

Whichever form has the most text fields.

Whichever form has the most multi-value select fields.

Whichever form has the most single-value select fields.

Whichever form Burp Scanner found first.

For example, if two forms have an equal number of password fields, Burp Scanner next compares the number of text fields, and so on.

Why is Burp Scanner not filling in my login forms?

Burp Scanner identifies login and registration forms based on the password field. However, it only enters a username or email address if the related fields:

Have a type=email or type=text attribute.

Have a non-empty name attribute.

If the username field does not meet these conditions, then Burp Scanner can identify the form but is unable to enter the corresponding data.

What usernames does Burp Scanner submit?

Burp Scanner submits the username as provided in the following situations:

The field has a type=text attribute.

The field has a type=email attribute and the username provided ends in an email domain.

If the field has a type=email attribute but the username provided does not end in an email domain, then Burp Scanner submits the provided username with @burpcollaborator.net appended.
