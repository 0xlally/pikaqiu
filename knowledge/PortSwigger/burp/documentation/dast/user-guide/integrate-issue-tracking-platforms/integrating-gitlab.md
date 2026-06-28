# Integrating Burp Suite DAST with GitLab

Source: https://portswigger.net/burp/documentation/dast/user-guide/integrate-issue-tracking-platforms/integrating-gitlab
Fetched: 2026-06-28T09:15:36.504882+00:00

DAST

Integrating Burp Suite DAST with GitLab

Last updated:

June 18, 2026

Read time:

3 Minutes

If you or your teams use GitLab, you can integrate it with Burp Suite DAST. Once configured, this enables you to raise GitLab issues from directly within Burp Suite DAST for any security issues found by your scans.

Prerequisites

You have access to Burp Suite DAST as an administrator.

You have access to your GitLab instance as an administrator.

You have the Maintainer or Owner role for any GitLab projects you want to create issues on.

(Recommended) Create a new GitLab user for the integration

To integrate with GitLab, Burp Suite DAST must be linked to a specific GitLab user.

We recommend creating a new GitLab user specifically for the integration. This allows you to control which projects are available for use in Burp Suite DAST - simply by adding your user as a Reporter to those projects.

Generate a GitLab impersonation token

A GitLab impersonation token allows Burp Suite DAST to raise GitLab issues as a specific user.

Note

The latest version of GitLab adds a prefix to the personal access token, which means the token now exceeds our 20-character limit. You can use the following workaround to fix this:

Go to the following link: https://gitlab.example.com/admin/application_settings/general#application_setting_personal_access_token_prefix

Delete all the contents from the Personal Access Token prefix field.

Click Save changes.

Create a new impersonation token.

To generate a GitLab impersonation token:

Sign into GitLab with administrator privileges.

In the Admin area, select the user you want Burp Suite DAST to use to raise GitLab issues.

Click Impersonation Tokens.

Give the impersonation token a name (e.g. "Burp Suite DAST"), and check the box to give the impersonation token api scope.

Click the Create impersonation token button.

Copy the impersonation token to your clipboard.

Connect Burp Suite DAST to GitLab

If you're logged in as an administrator, you can connect Burp Suite DAST to GitLab:

Go to Settings > Integrations.

On the GitLab tile, click Configure. This takes you to the GitLab integration screen.

In the provided field, enter your GitLab API URL, for example, https://gitlab.example.com.

Enter the GitLab personal access token you created earlier. For more information, see Generating a GitLab impersonation token.

Click Connect.

If Burp Suite DAST successfully connects to GitLab, you'll be presented with options to configure how issues are raised both manually and automatically.

Note

You must enable at least one of these in order to complete the GitLab configuration.

Enable GitLab issues to be raised manually

To enable users to raise GitLab issues manually from within Burp Suite DAST, you need to configure the list of GitLab projects and issue types that they can choose from:

Select a project from the Project drop-down list.

Select an issue type from the Issue type drop-down list.

Click the + symbol.

If necessary, repeat these steps to add more projects and issue types.

Note

You need to add separate entries for each issue type, even when adding multiple issue types from the same project.

Click Save.

Enable GitLab issues to be raised automatically

You can configure Burp Suite DAST to raise GitLab issues automatically. Issues are created if they meet the minimum severity and confidence levels that you specify.

Note

To avoid inadvertently flooding your GitLab backlog with an overwhelming number of issues, we recommend setting high severity and confidence levels initially. You can then lower these once you have a better understanding of how many issues are raised as a result of your scans.

Click Enable.

Select a project from the Project drop-down list.

Select an issue type from the Issue type drop-down list.

Use the sliders to set the minimum issue severity and confidence levels that trigger GitLab issue

creation.

Click Save.

Raising GitLab issues from within Burp Suite DAST

For information on how users can manually raise GitLab issues, refer to Raise GitLab issues from within Burp Suite DAST.
