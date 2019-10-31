Pull Request Service
====================
A service to operate within an Openshift cluster, that can manage resource related to pull request environments.

Rationale
---------
Within our Openshift clusters, we provision new projects/namespaces to perform testing of pull requests. This allows us to execute code we develop within the cluster, preview changes as they are likely to be seen once merged etc. To do this, Jenkins pipelines will create these namespaces and deploy services to them. Once the pull request is closed however, these namespaces are no longer needed. Something needs to clean them up, to free up cluster resources. The pull request service is that 'something'.