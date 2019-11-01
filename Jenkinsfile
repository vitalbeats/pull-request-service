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
        stage('Prepare') {
            steps {
                container('python') {
                    sh 'pip3 install poetry'
                }
            }
        }
    
        stage('Build') {
            steps {
                container('python') {
                    sh 'poetry install && poetry build'
                }
            }
        }

        stage('Test') {
            steps {
                container('python') {
                    sh 'poetry run pytest'
                }
            }
        }

        stage('Docker') {
            when {
                branch 'master'
            }
        
            steps {
                container('docker') {
                    sh 'docker build -t docker-registry.default.svc:5000/openshift-build/pull-request-service:latest .'
                    sh 'docker push docker-registry.default.svc:5000/openshift-build/pull-request-service:latest'
                }
            }
        }
    }
}
