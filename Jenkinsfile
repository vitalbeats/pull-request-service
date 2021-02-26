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
                container('build') {
                    sh 'docker build --network=host -t registry.vitalbeats.dev/pull-request-service/pull-request-service:latest .'
                }
            }
        }

        stage('Push') {
            when {
                branch 'master'
            }
        
            steps {
                container('build') {
                    sh 'docker push registry.vitalbeats.dev/pull-request-service/pull-request-service:latest'
                }
            }
        }

        stage('Deploy') {
            when {
                branch 'master'
            }

            steps {
                container('build') {
                    sh 'kubectl apply -n pull-request-service -k kustomize/'
                    sh 'kubectl rollout status -w deployment/pull-request-service -n pull-request-service'
                }
            }
        }
    }
}
