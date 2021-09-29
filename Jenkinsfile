pipeline {
    environment {
        python_path = ''
    }
    agent any
    stages {
        stage('Checkout Code') {
            steps {
                script {
                    git branch: "master",
                        credentialsId: 'github-app-jenkins',
                        url: 'https://github.com/eaingaran/http-fun.git'
                }
            }
        }
        stage('Unit Test') {
            steps {
                echo 'setting up venv'
                sh 'python3 -m pip install --upgrade pip'
                sh 'pip3 install --upgrade setuptools'
                sh 'pip3 install virtualenv'
                python_path = sh(script: 'which python3', returnStdout: true)
                sh 'virtualenv -p ' + python_path + ' venv'
                sh 'source venv/bin/activate'
                sh 'which python3'
                sh 'deactivate'
            }
        }
        stage('Build and Upload image') {
            steps {
                echo 'Yet to be implemented'
            }
        }
        stage('Deploy Image') {
            steps {
                echo 'Yet to be implemented'
            }
        }
    }
}
