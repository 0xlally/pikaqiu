# Resetting your admin password

Source: https://portswigger.net/burp/documentation/dast/user-guide/users-and-permissions/resetting-your-admin-password
Fetched: 2026-06-28T09:15:42.445611+00:00

DAST

Resetting your admin password

Last updated:

June 18, 2026

Read time:

3 Minutes

Cloud

Self-hosted

The first time you launch Burp Suite DAST, you're prompted to set a password for an initial administrator user so that you can log in and complete the setup process. If you lose or forget these credentials, you need to reset your password.

If you've already created additional admin users, you can simply ask one of them to reset your password from the Teams page, just like any other user. If you are the only admin user, the process you need to follow to reset your password depends on how you deployed Burp Suite DAST.

On this page

Resetting your admin password on a Cloud instance

Resetting your admin password on a self-hosted standard instance

Resetting your admin password on a self-hosted Kubernetes instance

Resetting your admin password on a Cloud instance

Cloud

To reset your admin password on a Cloud instance, you need to request a password reset from the Sign in page:

Go to the Sign in page and click Forgot password. The Reset your password page is displayed.

Enter the email address for your admin account and click Request password reset. Burp Suite DAST sends a reset email to the named account.

Open the email and click the URL. Burp Suite DAST generates a new password and opens the Here's your new password page.

Copy the new password and store it somewhere secure, such as a password manager.

If required, click Go to login to display the Sign in page and then log in with your email and newly-created password.

Resetting your admin password on a self-hosted standard instance

Self-hosted

To reset your admin password on a standard, self-hosted instance of Burp Suite DAST, we've provided a resetAdministratorPassword script. This script enables you to reset the default admin user password without logging in to the web interface. It can be found in your Burp Suite DAST installation directory.

To run the script:

Windows

Open a command prompt.

Enter the following command, with your installation directory and the new password that you want to set:

"<your-installation-directory>\resetAdministratorPassword" <new-password>

Log in to Burp Suite DAST as normal with the username administrator and the password you just set.

Linux

Open the Linux Terminal.

Navigate to the installation directory:

cd <your-installation-directory>

Run the following command:

sudo ./resetAdministratorPassword <new-password>

Note

If no user with the name administrator exists, one will be created and assigned the new password.

Resetting your admin password on a self-hosted Kubernetes instance

Self-hosted

To reset your admin password on a Kubernetes instance, you need to use the kubectl command. For more information on how to connect and run commands via kubectl, consult the kubectl documentation or your cloud provider's documentation.

Connect to your Burp Suite DAST Kubernetes cluster.

Run the following command to output the details of your Burp Suite DAST pods:

kubectl -n bsee get pods

In the output, find the name of the DAST server pod. This should begin with bsee-enterprise-server-deployment- followed by a unique identifier.

Run the following command to execute the script and reset the password for the administrator user:

kubectl -n bsee exec <your-Enterprise-server-pod-name> -- ./bin/resetAdministratorPassword <your-new-password>

Log in to Burp Suite DAST as normal with the username administrator and the password you just set.

Note

If no user with the name administrator exists, one will be created and assigned the new password.

Related pages

Role-based access control

Managing users and permissions
