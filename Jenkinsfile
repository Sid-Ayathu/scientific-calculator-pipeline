pipeline {
    // agent {
    //     label 'wsl'
    // }
    
    agent any
    environment {
        DOCKERHUB_USER = 'salvoslayer'
        DOCKER_IMAGE = "${DOCKERHUB_USER}/scientific-calculator"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Sid-Ayathu/scientific-calculator-pipeline.git'
            }
        }

        stage('Install dependencies & Test') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'python3 -m unittest discover'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE:latest .'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                    sh 'echo $PASS | docker login -u $USER --password-stdin'
                    sh 'docker push $DOCKER_IMAGE:latest'
                }
            }
        }

        stage('Deploy with Ansible') {
            steps {
                sh 'ansible-playbook -i hosts.ini deploy.yml'
            }
        }
    }

    post {
        success {
            echo 'Pipeline finished successfully ✅'
        }
        failure {
            echo 'Pipeline failed ❌'
        }
        
    }
}
