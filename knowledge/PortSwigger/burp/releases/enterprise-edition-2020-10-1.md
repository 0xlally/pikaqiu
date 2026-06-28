# Enterprise Edition 2020.10.1

Source: https://portswigger.net/burp/releases/enterprise-edition-2020-10-1
Fetched: 2026-06-28T09:16:16.184594+00:00

Bug fix

This release fixes a bug in the installer that affected some customers using an Oracle database. Previously, the installer would fail if the database schema name was anything other than burp_enterprise.

Cloud deployment links

We no longer provide AWS CloudFormation or Azure Resource Manager templates. We're releasing an improved, much simpler deployment method soon and recommend waiting for this instead.
