pipeline {
    agent {
        kubernetes {
            defaultContainer 'jnlp'
            yamlFile 'agent-pod.yaml'
        }
    }

    options {
        timestamps()
    }
    
    stages {  
        stage('Build') {
            steps {
                container('docker') {
                    sh 'docker build -t pull-request-service:build .'
                }
            }
        }

        stage('Push') {
            when {
                branch 'master'
            }
        
            steps {
                container('docker') {
                    sh 'docker tag pull-request-service:build docker-registry.default.svc:5000/openshift-build/pull-request-service:latest'
                    sh 'docker push docker-registry.default.svc:5000/openshift-build/pull-request-service:latest'
                }
            }
        }
    }
}
