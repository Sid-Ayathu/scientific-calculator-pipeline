// pipeline {
//     // agent {
//     //     label 'wsl'
//     // }
    
//     agent any
//     environment {
//         DOCKERHUB_USER = 'salvoslayer'
//         DOCKER_IMAGE = "${DOCKERHUB_USER}/scientific-calculator"
//     }

//     stages {
//         stage('Checkout') {
//             steps {
//                 git branch: 'main', url: 'https://github.com/Sid-Ayathu/scientific-calculator-pipeline.git'
//             }
//         }

//         stage('Install dependencies & Test') {
//             steps {
//                 sh 'pip install -r requirements.txt'
//                 sh 'python3 -m unittest discover'
//             }
//         }

//         stage('Build Docker Image') {
//             steps {
//                 sh 'docker build -t $DOCKER_IMAGE:latest .'
//             }
//         }

//         stage('Push to Docker Hub') {
//             steps {
//                 withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
//                     sh 'echo $PASS | docker login -u $USER --password-stdin'
//                     sh 'docker push $DOCKER_IMAGE:latest'
//                 }
//             }
//         }

//         stage('Deploy with Ansible') {
//             steps {
//                 sh 'ansible-playbook -i hosts.ini deploy.yml'
//             }
//         }
//     }

//     post {
//         success {
//             echo 'Pipeline finished successfully ✅'
//         }
//         failure {
//             echo 'Pipeline failed ❌'
//         }
        
//     }
// }

pipeline {
    // 'agent any' tells Jenkins to run on the main Jenkins machine (your WSL instance)
    agent any

    environment {
        // Set your Docker Hub username and image name
        DOCKER_USERNAME = 'salvoslayer'
        IMAGE_NAME = 'scientific_calculator'
        // This is the ID of the credential we will create in Jenkins
        DOCKER_CREDENTIALS_ID = 'dockerhub-credentials'
    }

    stages {
        // Stage 1: Pulls the code from GitHub
        stage('Checkout') {
            steps {
                echo 'Pulling code from GitHub...'
                checkout scm
            }
        }

        // Stage 2: Run tests using the 'python3' command on the WSL machine
        stage('Test') {
            steps {
                echo 'Running unit tests...'
                // This requires 'python3' to be installed on your WSL machine
                sh 'python3 unit_tests.py'
            }
        }

        // Stage 3: Build the Docker image
        stage('Build Image') {
            steps {
                echo "Building Docker image: ${DOCKER_USERNAME}/${IMAGE_NAME}..."
                // This requires the 'jenkins' user to have Docker permissions
                sh "docker build -t ${DOCKER_USERNAME}/${IMAGE_NAME} ."
            }
        }

        // Stage 4: Push the image to Docker Hub
        stage('Push to Docker Hub') {
            steps {
                echo 'Logging in and pushing to Docker Hub...'
                // Uses the credential with the ID 'dockerhub-credentials'
                withCredentials([usernamePassword(credentialsId: DOCKER_CREDENTIALS_ID, usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    // Log in using the injected variables
                    sh "echo ${DOCKER_PASS} | docker login -u ${DOCKER_USER} --password-stdin"
                    // Push the image
                    sh "docker push ${DOCKER_USERNAME}/${IMAGE_NAME}:latest"
                }
            }
        }

        // Stage 5: Deploy using Ansible
        stage('Deploy') {
            steps {
                echo 'Deploying container with Ansible...'
                // This requires 'ansible' to be installed on your WSL machine
                // It runs the playbook, which will run 'docker pull' and 'docker run'
                sh 'ansible-playbook -i hosts playbook.yml'
            }
        }
    }
}
