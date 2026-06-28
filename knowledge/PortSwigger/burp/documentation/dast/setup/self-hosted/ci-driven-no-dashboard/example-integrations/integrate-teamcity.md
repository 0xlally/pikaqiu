# Integrating a CI-driven scan with no dashboard with TeamCity

Source: https://portswigger.net/burp/documentation/dast/setup/self-hosted/ci-driven-no-dashboard/example-integrations/integrate-teamcity
Fetched: 2026-06-28T09:15:32.601685+00:00

DAST

Integrating a CI-driven scan with no dashboard with TeamCity

Last updated:

June 18, 2026

Read time:

3 Minutes

This page contains instructions to integrate a no-dashboard scan with TeamCity. This enables you to use Burp Scanner to run scans as a stage in your existing CI/CD pipeline, and fail builds if issue thresholds are met.

You configure the scan by defining a set of simple parameters in a YAML file. To learn how to configure the scan, see Creating a configuration file for a CI-driven scan with no dashboard.

These instructions were tested with TeamCity version 2023.05.

Before you start

Before you start, save the configuration for your no-dashboard scan as a YAML file. See Creating a configuration file for a CI-driven scan with no dashboard.

TeamCity agent requirements

To integrate a no-dashboard scan with TeamCity:

Your TeamCity agent must have Docker configured to run containers.

No plugins beyond the TeamCity defaults are required to run a no-dashboard scan in a TeamCity CI/CD pipeline.

For information on the machine specification required to run a no-dashboard scan, see System requirements for CI-driven scans with no dashboard.

Creating the settings file

Configure access from TeamCity to the repository where your settings.kts file is stored.

Add the following content to your settings.kts file:

import jetbrains.buildServer.configs.kotlin.BuildType

import jetbrains.buildServer.configs.kotlin.DslContext

import jetbrains.buildServer.configs.kotlin.buildSteps.script

import jetbrains.buildServer.configs.kotlin.project

import jetbrains.buildServer.configs.kotlin.version

version = "2022.10"

project {

description = "Contains all other projects"

buildType(ExampleScan)

}

object ExampleScan : BuildType({

name = "Example Scan"

vcs {

root(DslContext.settingsRoot)

cleanCheckout = true

}

failureConditions {

testFailure = false

}

features {

feature {

type = "xml-report-plugin"

param("xmlReportParsing.reportType", "junit")

param("xmlReportParsing.reportDirs", "+:burp_junit_report.xml")

}

}

steps {

script {

name = "Example Scan"

scriptContent =

"docker run --rm --pull=always \

-u $(id -u) -w %system.teamcity.build.checkoutDir% " +

"-v %system.teamcity.build.checkoutDir%:%system.teamcity.build.checkoutDir% " +

"-e BURP_CONFIG_FILE_PATH=%system.teamcity.build.checkoutDir%/burp_config.yml " +

"public.ecr.aws/portswigger/enterprise-scan-container:latest"

}

}

artifactRules = "+:burp_junit_report.xml"

})

Setting the configuration of your scan

To set the configuration for your scan, save your configuration file as burp_config.yml in the root of your application.

To learn how to create and edit the configuration file, see Creating a configuration file for a CI-driven scan with no dashboard.

Configuring the TeamCity pipeline

From the main TeamCity interface, click New project and choose an appropriate place in your project hierarchy.

Make sure that Manually is selected.

Give your project a Name. You can also add a Description.

Click Create.

Click Versioned Settings.

Select Synchronization enabled.

Under Project settings VCS Root, click Create VCS root or use an existing option from the Project Settings VCS root drop-down.

Make sure that the Settings format is set to Kotlin.

Click Apply.

From the Existing Project Settings Detected pop-up, click Import settings from VCS.

Viewing scan results in TeamCity

To view the results of your scan:

Run the no-dashboard scan for your TeamCity project, and wait for the scan to complete. The time the scan takes varies, depending on how the scan is configured.

From the main TeamCity interface, click on your project containing the no-dashboard scan.

Under Example Scan, click on the build containing your scan.

Click Tests. Here you can see any failed tests. See more details of a failed test by clicking on it.

Remediation advice

You can see remediation advice for security issues that Burp Scanner finds under Stacktrace. This includes links to relevant sections of the free Web Security Academy resource, which provide further detail on web security vulnerabilities.

Evidence

You can see evidence for security issues that Burp Scanner finds under Stacktrace. This evidence includes the request sent by Burp Scanner to produce the issue, as well as the response sent by the application.
