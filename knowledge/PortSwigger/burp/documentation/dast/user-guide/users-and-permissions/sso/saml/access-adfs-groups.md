# Enabling Burp Suite DAST to access your ADFS groups

Source: https://portswigger.net/burp/documentation/dast/user-guide/users-and-permissions/sso/saml/access-adfs-groups
Fetched: 2026-06-28T09:15:42.584035+00:00

DAST

Enabling Burp Suite DAST to access your ADFS groups

Last updated:

June 18, 2026

Read time:

3 Minutes

Cloud

Self-hosted

If you're not using SCIM, you can create groups in Burp Suite DAST that have identical names to your groups in ADFS. This enables Burp Suite DAST to duplicate these groups of users, and enables you to manage them locally.

To make sure that the group membership of your users is in a format that Burp Suite DAST can recognize, you have the following options:

Create a central claim issuance policy that handles all of your groups in the same way.

Configure claim rules for each group that you want to expose to Burp Suite DAST individually.

Note

You can also use a combination of both approaches. In this case, the groups available to Burp Suite DAST would be the union of the groups covered by the claim issuance policy and any additional groups for which you created individual claim rules.

Create a central claim issuance policy

To expose all of your users' groups to Burp Suite DAST, configure a central claim issuance policy. This allows you to manage the claim rules for all of your groups in one place. It also removes the need to configure claim rules each time you add a new group.

The downside to this approach is that your groups must keep their existing group names. For example, if your group is called BSEE_View_Scans in Active Directory, you need to use this exact name for the corresponding user group in Burp Suite DAST. For more information, see Configuring user permissions for SSO.

Open the ADFS Management tool and go to the list of relying party trusts.

Right-click on the entry you created for Burp Suite DAST and select Edit claim issuance policy.

Use the wizard to configure the following rules:

Rule 1

Template: Send LDAP attributes as claims

Name: Send UPN as nameId

Rule: User-Principle-Name => Name ID

Rule 2

Template: Send LDAP attributes as claims

Name: AccountName

Rule: SAM-Account-Name = Windows Account Name

Rule 3

Template: Send claims using a custom rule

Name: nameDN

Rule:

c:[Type == "http://schemas.microsoft.com/ws/2008/06/identity/claims/windowsaccountname", Issuer == "AD AUTHORITY"] => add(store = "Active Directory", types = ("http://schemas.xmlsoap.org/ws/2005/05/identity/claims/nameDN"), query = ";distinguishedName;{0}", param = c.Value);

Rule 4

Template: Send claims using a custom rule

Name: Group

Rule:

c1:[Type == "http://schemas.microsoft.com/ws/2008/06/identity/claims/windowsaccountname", Issuer == "AD AUTHORITY"] && c2:[Type == "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/nameDN"] => add(store = "Active Directory", types = ("http://schemas.xmlsoap.org/claims/Group"), query = "(member:1.2.840.113556.1.4.1941:={1});samaccountname;{0}", param = c1.Value, param = c2.Value);

Rule 5

Template: Pass through or filter an incoming claim

Name: IssuedGroup

Rule: Group - Pass through all claim values

All the groups that the user belongs to are sent with every claim to Burp Suite DAST. If you add new groups, these rules automatically apply to them as well.

Create claim rules for each group individually

You can create claim rules on a group-by-group basis. This gives you more granular control over which groups and related information are exposed to Burp Suite DAST in each claim.

You can output the group with a different name than the one used in Active Directory. For example, if your group is called BSEE_View_Scans, you can output this with a more user-friendly name, such as "Scan viewers". You can then use this name for the corresponding group in Burp Suite DAST. For more information, see Configuring user permissions for SSO.

Open the ADFS Management tool and go to the list of relying party trusts.

Right-click on the entry you created for Burp Suite DAST and select Edit claim issuance policy.

From the Claim rule template drop-down list, select Send Group Membership as Claim and click Next.

Enter a name for the claim rule.

To configure a claim rule, select User's group and select the group.

From the Outgoing claim type drop-down list, select Group.

In the Outgoing claim value field, enter a new name that you want to use for this group when sending a claim.

Repeat this process for each group that you want to expose to Burp Suite DAST.

If you add new groups in the future, you will need to repeat this process for each of them.

Adding your groups to Burp Suite DAST

The next step is to grant permissions, by matching the names of groups that you create in Burp Suite DAST with your ADFS groups. For more information, see Configuring groups for SAML or LDAP.
