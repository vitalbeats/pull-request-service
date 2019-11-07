import yaml
from kubernetes import client, config
from openshift.dynamic import DynamicClient

class ProjectLoader():
    k8s_client = config.new_client_from_config()
    dyn_client = DynamicClient(k8s_client)
    project_list = dyn_client.resources.get(api_version='project.openshift.io/v1', kind='Project').get()

    def print(self):
        for project in self.project_list.items:
            print(project.metadata.name)
