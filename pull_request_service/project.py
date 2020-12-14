import yaml
from kubernetes import client
from openshift.dynamic import DynamicClient
from twisted.python import log

class ProjectList():
    dyn_client = None

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

    def delete(self, project_name):
        projects = self.dyn_client.resources.get(api_version='v1', kind='Namespace').get()
        if projects == None:
            log.msg('Unable to fetch projects.')
        else:
            for project in projects.items:
                if project.metadata.name == project_name:
                    log.msg('Found matching project by name, will delete.')
                    self.dyn_client.resources.get(api_version='v1', kind='Namespace').delete(name=project_name)
                if project.metadata.annotations != None and project.metadata.annotations['com.vitalbeats.pull-request-service/project-name'] == project_name:
                    log.msg('Found matching project by annotation, will delete.')
                    self.dyn_client.resources.get(api_version='v1', kind='Namespace').delete(name=project_name)
