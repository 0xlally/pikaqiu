# System requirements for a Kubernetes instance

Source: https://portswigger.net/burp/documentation/dast/setup/self-hosted/kubernetes/k8-system-requirements
Fetched: 2026-06-28T09:15:33.441559+00:00

DAST

System requirements for a Kubernetes instance

Last updated:

June 18, 2026

Read time:

2 Minutes

You can deploy Burp Suite DAST to Kubernetes. We provide a Helm chart with the correct field values to meet the minimum system requirements.

Note

We recommend that you only attempt to deploy and manage Burp Suite DAST in a Kubernetes environment if you have previous Kubernetes experience.

To deploy Burp Suite DAST to Kubernetes, you need an external database that meets our system requirements. You also need a cluster that meets the following requirements:

An ingress solution, for example a load balancer or an ingress controller.

A PersistentVolume with ReadWriteMany access mode. We recommend that this is backed by POSIX-compatible storage.

A PersistentVolumeClaim bound to the PersistentVolume. This must have ReadWriteMany access mode, to allow simultaneous read/write access from multiple nodes. Make sure the PersistentVolumeClaim is located in the namespace where Burp Suite DAST will be deployed.

(Optional) To enable cluster node autoscaling, install and enable the cluster-autoscaler.

Note

We don't recommend object storage solutions such as Google Cloud storage buckets, due to performance and compatibility issues.

Burp Suite DAST can run on an x86-based cluster. There may be additional infrastructure configuration required depending on your Kubernetes environment. Please refer to our Kubernetes support scope and setup guide.

Container system requirements

We specify the hardware resources for the containers in our Helm chart values file.

Note

Make sure your cluster node type is set appropriately for your environment.

CentOS/RHEL v7.x operating systems are not supported for the cluster worker node.

Minimum requirements for general container limits

These are the minimum and maximum limits for all your containers in the namespace.

Field

Value

maxCpuPerContainer

4000m

minCpuPerContainer

100m

maxMemoryPerContainer

8Gi

minMemoryPerContainer

128Mi

Minimum requirements for a web server container

Field

Value

webServerContainerCpu

1400m

webServerContainerMemory

2Gi

Minimum requirements for a DAST server container

Field

Value

enterpriseServerContainerCpu

1400m

enterpriseServerContainerMemory

2Gi

Minimum requirements for a scan container

Field

Value

scanContainerCpu

4000m

scanContainerMemory

8Gi

If you need help with the system requirements, please email our support team.

Next step - System requirements for your external database

CONTINUE
