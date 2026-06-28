# Enterprise Edition 2021.12.1

Source: https://portswigger.net/burp/releases/enterprise-edition-2021-12-1
Fetched: 2026-06-28T09:16:16.848455+00:00

We have audited both Burp Suite Enterprise Edition and Burp Suite Professional/Community Edition and determined that neither are vulnerable to the recently disclosed vulnerability in the Java logging library Log4j. Although this library was present in Burp Suite Enterprise Edition due to a transitive dependency, it was not used. This release removes this dependency as a precautionary measure.

Please note that third-party extensions may be vulnerable. You may wish to disable these while they are audited.

Jira bug fix

This release also fixes a bug that prevented you from creating Jira tickets from Burp Suite Enterprise Edition.

Cloud deployment links

We no longer provide AWS CloudFormation or Azure Resource Manager templates. We're releasing an improved, much simpler deployment method soon and recommend waiting for this instead.
