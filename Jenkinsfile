

pipeline {
    agent any

    environment {
        DOCKERHUB_CREDS = 'dockerhub-credentials'
        
        DOCKERHUB_USERNAME = 'salvoslayer'
        IMAGE_NAME = "${DOCKERHUB_USERNAME}/scientific-calculator"
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out code...'
            }
        }

        stage('Run Test Cases') {
            steps {
                echo 'Running tests...'
                sh 'pip3 install -r requirements.txt'
                sh 'pytest --junitxml=report.xml'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker image: ${DOCKERHUB_USERNAME}/${IMAGE_NAME}..."
                    
                    def app = docker.build("${DOCKERHUB_USERNAME}/${IMAGE_NAME}")
                }
            }
        }

        stage('Login & Push to Docker Hub') {
            steps {
                script {
                    docker.withRegistry("[https://index.docker.io/v1/](https://index.docker.io/v1/)", DOCKERHUB_CREDS) {
                        echo "Pushing image..."
                        
                        app.push("latest")
                    }
                }
            }
        }

        stage('Deploy on Local System') {
            steps {
                echo 'Deploying new container on local (WSL) system...'
                
                sh 'docker stop ${IMAGE_NAME} || true'
                sh 'docker rm ${IMAGE_NAME} || true'

                sh 'docker run -d --name ${IMAGE_NAME} -p 8081:8080 ${DOCKERHUB_USERNAME}/${IMAGE_NAME}:latest'
            }
        }
    }
    
    post {
        always {
            echo 'Pipeline finished.'
            cleanWs()
        }
    }
}
