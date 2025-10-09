pipeline {
    agent {
        // Run inside a Linux container to ensure sh commands work
        docker {
            image 'python:3.10-alpine'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    environment {
        DOCKERHUB_USERNAME = 'salvoslayer'
        IMAGE_NAME = "${DOCKERHUB_USERNAME}/scientific_calculator"
        DOCKER_CREDENTIALS_ID = 'dockerhub-credentials' 
    }

    stages {
        stage('Checkout') {
            steps {
                deleteDir()  // Clean workspace
                git branch: 'main', url: 'https://github.com/Sid-Ayathu/scientific-calculator-pipeline.git'
            }
        }

        stage('Test') {
            steps {
                echo 'Installing dependencies and running tests...'
                sh '''
                    apk add --no-cache py3-pip
                    pip install -r requirements.txt || true
                    python3 -m unittest discover -v
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                sh """
                    docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} .
                    docker tag ${IMAGE_NAME}:${BUILD_NUMBER} ${IMAGE_NAME}:latest
                """
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo 'Pushing image to Docker Hub...'
                withCredentials([usernamePassword(credentialsId: DOCKER_CREDENTIALS_ID, usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh """
                        echo ${DOCKER_PASS} | docker login -u ${DOCKER_USER} --password-stdin
                        docker push ${IMAGE_NAME}:${BUILD_NUMBER}
                        docker push ${IMAGE_NAME}:latest
                    """
                }
            }
        }

        stage('Deploy') {
            steps {
                echo 'Installing Ansible and deploying...'
                sh '''
                    apk add --no-cache ansible
                    ansible-playbook -i hosts playbook.yml
                '''
            }
        }
    }

    post {
        success { echo '✅ Pipeline completed successfully!' }
        failure { echo '❌ Pipeline failed!' }
    }
}
