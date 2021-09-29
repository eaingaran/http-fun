pipeline {
    environment {
        python_path = ''
    }
    agent any
    stages {
        stage('Clean up workspace') {
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
                python3 app/make.py
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
