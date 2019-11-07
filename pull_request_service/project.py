import yaml
from kubernetes import client, config
from openshift.dynamic import DynamicClient

def __file_to_line(file_name):
    with open(file_name, 'r') as f:
        return f.read()

class ProjectLoader():
    dyn_client = None
    project_list = {}

    def __init__(self):
        k8s_config = config.Configuration()
        # Openshift API tokens never expire, they can be revoked by deleting the associated secret though
        k8s_config.api_key = {"authorization": "Bearer " + __file_to_line('/var/run/secrets/kubernetes.io/serviceaccount/token')}
        k8s_config.ssl_ca_cert = '/var/run/secrets/kubernetes.io/serviceaccount/ca.crt'
        self.dyn_client = DynamicClient(client.ApiClient(k8s_config))
        self.project_list = dyn_client.resources.get(api_version='project.openshift.io/v1', kind='Project').get()

    def print(self):
        for project in self.project_list.items:
            print(project.metadata.name)
