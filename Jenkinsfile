pipeline {
    environment {
        registry = "eaingaran/http-fun"
        registryCredential = 'dockerhub_id'
        dockerImage = ''
        projectId = 'expanded-aria-326609'
        clusterName = 'autopilot-cluster-1'
        location = 'us-central1'
        credentialsId = 'expanded-aria-326609'
    }
    agent any
    stages {
        stage('Setup up workspace') {
            steps {
                sh 'rm -rf http-fun'
            }
        }
        stage('Checkout Code') {
            steps {
                sh 'git clone https://github.com/eaingaran/http-fun.git'
            }
        }
        stage('Setup venv') {
            steps {
                echo 'setting up venv'
                sh 'python3 -m pip install --upgrade pip'
                sh 'pip3 install --upgrade setuptools'
                sh 'pip3 install virtualenv'
                sh """
                . venv/bin/activate
                pip install -r http-fun/requirements.txt
                """
            }
        }
        stage('creating config') {
            steps {
                sh """
                . venv/bin/activate
                cd http-fun
                python3 make.py
                cp config.ini app/config.ini
                """
            }
        }
        stage('Unit Test') {
            steps {
                sh """
                . venv/bin/activate
                cd http-fun
                python3 -m unittest test/app-test.py
                """
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
                            dockerImage.push("latest")
                        }
                    }
                }
            }
        }
        stage('Deploying image') {
            steps{
                dir('http-fun') {
                    step([$class: 'KubernetesEngineBuilder', projectId: env.credentialsId, clusterName: env.clusterName, location: env.location, manifestPattern: 'deployment.yaml', credentialsId: env.credentialsId, verifyDeployments: true])
                }
            }
        }
    }
}
