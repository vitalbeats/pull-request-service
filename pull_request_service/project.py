import yaml
from kubernetes import client
from openshift.dynamic import DynamicClient

class ProjectLoader():
    dyn_client = None
    project_list = {}

    def __init__(self):
        k8s_config = client.configuration.Configuration()
        token = ''
        with open('/var/run/secrets/kubernetes.io/serviceaccount/token', 'r') as f:
            token = f.read()
        # Openshift API tokens never expire, they can be revoked by deleting the associated secret though
        k8s_config.api_key = {"authorization": "Bearer " + token}
        k8s_config.ssl_ca_cert = '/var/run/secrets/kubernetes.io/serviceaccount/ca.crt'
        k8s_config.host = 'https://kubernetes.default.svc:443'
        self.dyn_client = DynamicClient(client.ApiClient(configuration=k8s_config))
        self.project_list = self.dyn_client.resources.get(api_version='project.openshift.io/v1', kind='Project').get()

    def print(self):
        for project in self.project_list.items:
            print(project.metadata.name)
