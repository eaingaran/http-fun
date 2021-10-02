pipeline {
    environment {
    // these should be parameterised and
    // should be overridable from jenkins or any CI/CD system.
        registry = "eaingaran/http-fun"
        registryCredential = 'dockerhub_id'
        dockerImage = ''
        projectId = 'expanded-aria-326609'
        clusterName = 'autopilot-cluster-1'
        location = 'us-central1'
        credentialsId = 'expanded-aria-326609'
        shouldCreateCuster = false
        shouldDeployApp = false
        shouldDeleteCluster = false
    }
    agent any
    stages {
        stage('Setup up workspace') {
            steps {
                sh 'rm -rf http-fun'
            }
        }
        // manual cloning is required to get the whole repository for commit hashes (using make.py)
        stage('Checkout Code') {
            steps {
                sh 'git clone https://github.com/eaingaran/http-fun.git'
            }
        }
        // use venv to avoid contamination of agents
        stage('Setup venv') {
            steps {
                echo 'setting up venv'
                sh 'python3 -m pip install --upgrade pip'
                sh 'pip3 install --upgrade setuptools'
                sh 'pip3 install virtualenv'
                dir('http-fun') {
                    sh """
                    python3 -m virtualenv -p python3 venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                    """
                }
            }
        }
        stage('creating config') {
            steps {
                dir('http-fun') {
                    sh """
                    . venv/bin/activate
                    python3 make.py
                    cp config.ini app/config.ini
                    """
                }
            }
        }
        stage('Unit Test') {
            steps {
                dir('http-fun') {
                    sh """
                    . venv/bin/activate
                    python3 -m unittest test/app-test.py
                    """
                }
            }
        }
        stage('Build image') {
            steps {
                dir('http-fun') {
                  script  {
                    dockerImage = docker.build registry + ":v1.$BUILD_NUMBER"
                  }
                }

            }
        }
        stage('Uploading image') {
            steps {
                dir('http-fun') {
                    script  {
                        docker.withRegistry('https://registry.hub.docker.com', registryCredential) {
                            dockerImage.push()
                            dockerImage.push("latest")  // tag the image with "latest" as well
                        }
                    }
                }
            }
        }
        stage('Create a GKE Cluster')   {
            when {
                expression { shouldCreateCuster }
            }
            steps   {
                dir('http-fun/infra')   {
                    sh 'terraform validate' // for testing, remove it later
                    sh 'terraform apply'
                }
            }
        }
        // This stage can deploy ONLY if the cluster is ready..
        // using gke autopilot with this would be cost efficient.
        stage('Deploying image') {
            when {
                expression { shouldDeployApp }
            }
            steps{
                dir('http-fun') {
                    step([$class: 'KubernetesEngineBuilder', projectId: env.projectId, clusterName: env.clusterName, location: env.location, manifestPattern: 'deployment.yaml', credentialsId: env.credentialsId, verifyDeployments: true])
                }
            }
        }
        stage('Destroy the GKE Cluster')  {
            when {
                expression { shouldDeleteCluster }
            }
            steps   {
                dir('http-fun/infra')   {
                    sh 'terraform destroy'
                }
            }
        }
        stage('Cleanup Workspace')  {
            steps   {
                sh 'rm -rf http-fun'
                sh 'docker system prune --all --force'
            }
        }
    }
}
