pipeline {
    environment {
    // these should be parameterised and
    // should be overridable from jenkins or any CI/CD system.
        registry = "eaingaran/http-fun"
        registryCredential = 'dockerhub_id' // credential for dockerhub.
        dockerImage = ''
        projectId = 'expanded-aria-326609'
        clusterName = 'autopilot-cluster-1'
        location = 'us-central1'
        credentialsId = 'expanded-aria-326609'  // private key (as a google service account private key)of the service account capable of deploying in GKE cluster
        serviceAccountOwnerEmail = 'sa-owner@expanded-aria-326609.iam.gserviceaccount.com'
        serviceAccountOwner = credentials('sa-owner')  // private key (in an encoded secret text format) of the service account capable of creating GKE clusters.
        shouldCreateCuster = 'false' // Groovy evaluates all non-empty string as true. So it is safer to use a specific string as a condition.
        shouldDeployApp = 'true'    // Any value other than 'true' will be considered as false.
        shouldDeleteCluster = 'false' // CHANGE THIS TO SOMETHING ELSE IF YOU WANT THE SERVICE TO BE ACTIVE. THIS WILL DELETE THE CLUSTER.
        deployWith = 'Helm' // Can take values 'KubernetesEngineBuilder' or 'Helm'. Used to choose the deployment provider.
    }
    options {
        skipDefaultCheckout true
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
                sh 'echo $serviceAccountOwner | base64 -d > http-fun/infra/expanded-aria-326609-cd7b37395be6.json'
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
                expression { shouldCreateCuster == 'true' }
            }
            steps   {
                dir('http-fun/infra')   {
                    sh 'terraform init'
                    sh 'terraform plan -out=tfplan -json'
                    archiveArtifacts artifacts: 'tfplan'
                    sh 'terraform apply -auto-approve -json tfplan'
                }
            }
        }
        // This stage can deploy ONLY if the cluster is ready..
        // using gke autopilot with this would be cost efficient.
        stage('Deploying image (KubernetesEngineBuilder)') {
            when {
                expression { shouldDeployApp == 'true' && deployWith == 'KubernetesEngineBuilder'}
            }
            steps{
                dir('http-fun') {
                    step([$class: 'KubernetesEngineBuilder', projectId: env.projectId, clusterName: env.clusterName, location: env.location, manifestPattern: 'deployment.yaml', credentialsId: env.credentialsId, verifyDeployments: true])
                }
            }
        }
        // This stage can deploy ONLY if the cluster is ready..
        // using gke autopilot with this would be cost efficient.
        stage('Deploying image (Helm)') {
            when {
                expression { shouldDeployApp == 'true' && deployWith == 'Helm'}
            }
            steps{
                dir('http-fun') {
                    sh 'gcloud auth activate-service-account ' + env.serviceAccountOwnerEmail + ' --key-file=infra/expanded-aria-326609-cd7b37395be6.json --project=' + env.projectId
                    sh 'gcloud container clusters get-credentials ' + env.clusterName + ' --region=' + env.location
                    sh 'helm install http-fun helmchart/ --values helmchart/values.yaml'
                }
            }
        }
        stage('Destroy the GKE Cluster')  {
            when {
                expression { shouldDeleteCluster == 'true' }
            }
            steps   {
                dir('http-fun/infra')   {
                    sh 'terraform destroy -auto-approve -json'
                }
            }
        }
    }
    post {
        always {
            echo 'Cleaning up workspace...'
            sh 'rm -rf http-fun'
            sh 'docker system prune --all --force'
        }
    }
}
