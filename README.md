Pull Request Service
====================
A service to operate within an Openshift cluster, that can manage resource related to pull request environments.

Rationale
---------
Within our Openshift clusters, we provision new projects/namespaces to perform testing of pull requests. This allows us to execute code we develop within the cluster, preview changes as they are likely to be seen once merged etc. To do this, Jenkins pipelines will create these namespaces and deploy services to them. Once the pull request is closed however, these namespaces are no longer needed. Something needs to clean them up, to free up cluster resources. The pull request service is that 'something'.

Requirements
------------

This role is intended to deploy to an Openshift cluster only. Currently it will deploy an Openshift Route for the web-hook URL, and assumes a service account that exists in other Vital Beats infrastructure. Both of these will be changed in the future to allow for more generic kubernetes deployment.This role requires that you have the [Openshift Ansible](https://github.com/openshift/openshift-ansible/tree/release-3.11) repository checked out alongside this one, as it makes use of 3.11 versions of Openshift ansible roles.

Role Variables
--------------

| Variable                                | Description                                                                                  | Default Value | Required |
| --------------------------------------- | -------------------------------------------------------------------------------------------- | ------------- | -------- |
| `openshift_pull_request_project`        | The project namespace to deploy the pull request service into. It will be created if needed. |               | Yes      |
| `openshift_pull_request_install`        | Whether or not to install the pull request service. Boolean value.                           |               | Yes      |
| `openshift_pull_request_hostname`       | The Route URL to expose the pull request service on.                                         |               | Yes      |
| `openshift_pull_request_secret`         | The GitHub webhook token to validate pull request notifications with.                        |               | Yes      |
| `openshift_pull_request_build_key`      | The path to the SSH key to use to checkout and build the pull request service.               |               | Yes      |
| `openshift_pull_request_start_cluster`  | Whether or not to build and deploy the pull request service when running the role.           | True          | No       |
| `openshift_pull_request_limits_cpu`     | The CPU limit to apply to pull request service containers.                                   | 50m           | No       |
| `openshift_pull_request_requests_cpu`   | The requested CPU to apply to pull request service containers.                               | 50m           | No       |
| `openshift_pull_request_limits_memory`  | The memory limit to apply to pull request service containers.                                | 128Mi         | No       |
| `openshift_pull_request_requests_memory`| The requested memory to apply to pull request service containers.                            | 128Mi         | No       |

Mapping Projects
----------------
There are currently two ways to map an Openshift project to a GitHub pull request. Firstly is by naming convention. By naming your project `<repo-name>-pr-<pr-number>`, the service will identify this as a project that needs managing as part of a pull request's lifecycle. Alternatively, the project can be annotated with `com.vitalbeats.pull-request-service/project-name` with the value matching the convention in the first example. This allows you to be more dynamic with your actual project names if needs be.
