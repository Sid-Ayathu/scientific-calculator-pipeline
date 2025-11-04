def app
pipeline {
    // This pipeline must run on an agent that has Docker installed.
    // The Jenkins controller (your WSL instance) *can* be the agent,
    // but you must install Docker in WSL first:
    // sudo apt install docker.io -y
    // sudo usermod -aG docker jenkins  (Gives Jenkins permission to use Docker)
    // sudo systemctl restart jenkins
    agent any

    environment {
        DOCKERHUB_CREDS = 'dockerhub-credentials'
        DOCKERHUB_USERNAME = 'salvoslayer'
        IMAGE_NAME = 'scientific-calculator'
    }

    stages {
        stage('Checkout') {
            // This 'Pull GitHub repo' step is now handled by Jenkins
            // when it reads this file from your SCM.
            steps {
                echo 'Checking out code...'
                // 'checkout scm' is automatic when using 'Pipeline from SCM'
            }
        }

        stage('Run Test Cases') {
            steps {
                // Assuming you use Python/pytest, as in the previous file.
                // If you use Java/Maven, this would be: sh 'mvn clean test'
                echo 'Running tests...'
                sh 'pip3 install -r requirements.txt'
                // --- THIS IS THE FIX ---
                // We must explicitly install pytest since requirements.txt is empty
                sh 'pip3 install pytest'
                
                // We use 'python3 -m pytest' instead of just 'pytest'
                // to ensure the 'jenkins' user can find the module
                // it just installed in its local directory.
                sh 'python3 -m pytest --junitxml=report.xml'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker image: ${DOCKERHUB_USERNAME}/${IMAGE_NAME}..."
                    // Use the Dockerfile in your repo
                    app = docker.build("${DOCKERHUB_USERNAME}/${IMAGE_NAME}")
                }
            }
        }

        stage('Login & Push to Docker Hub') {
            steps {
                script {
                    // Use the Credentials Binding plugin (docker.withRegistry)
                    docker.withRegistry('https://index.docker.io/v1/', DOCKERHUB_CREDS) {
                        echo "Pushing image..."
                        // Tags and pushes the image
                        app.push('latest')
                    }
                }
            }
        }


        stage('Deploy on Local System') {
            steps {
                echo 'Deploying new container on local (WSL) system...'
                // This stops and removes any *old* container
                sh 'docker stop ${IMAGE_NAME} || true'
                sh 'docker rm ${IMAGE_NAME} || true'

                // This runs the *new* image you just pushed
                sh 'docker run -d --name ${IMAGE_NAME} -p 8081:8080 ${DOCKERHUB_USERNAME}/${IMAGE_NAME}:latest'
                // Note: I'm using port 8081 on the host to avoid colliding with Jenkins on 8080
            }
        }
    }
    
    post {
        // This 'post' block runs after all stages are finished
        always {
            // Publish the test results
            junit 'report.xml'
            
            echo 'Pipeline finished.'
            
            // This cleans up the workspace for the next build.
            cleanWs()
        }
    }
}






