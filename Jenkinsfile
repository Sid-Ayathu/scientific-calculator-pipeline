def app
pipeline {
    agent any

    environment {
        DOCKERHUB_CREDS = 'dockerhub-credentials'
        DOCKERHUB_USERNAME = 'salvoslayer'
        IMAGE_NAME = 'scientific-calculator'
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
                sh 'pip3 install pytest'
                sh 'python3 -m pytest --junitxml=report.xml'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker image: ${DOCKERHUB_USERNAME}/${IMAGE_NAME}..."
                    app = docker.build("${DOCKERHUB_USERNAME}/${IMAGE_NAME}")
                }
            }
        }

        stage('Login & Push to Docker Hub') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', DOCKERHUB_CREDS) {
                        echo "Pushing image..."
                        // Tags and pushes the imag
                        app.push('latest')
                    }
                }
            }
        }


        stage('Deploy on Local System (with Ansible)') {
            steps {
                echo 'Deploying new container via Ansible...'
                // This one command runs the playbook we created.
                // We pass the Jenkins environment variables to the playbook
                // using '--extra-vars' so Ansible can use them.
                sh '''
                    ansible-playbook deploy.yml --extra-vars " \
                        docker_username=${DOCKERHUB_USERNAME} \
                        app_image_name=${IMAGE_NAME} \
                        host_port=8081 \
                        container_port=8080"
                '''
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







