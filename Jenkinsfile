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
    // 'agent any' tells Jenkins to run on the main Jenkins machine (your Windows machine)
    agent any

    environment {
        DOCKER_USERNAME = 'salvoslayer'
        IMAGE_NAME = 'scientific_calculator'
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

        // Stage 2: Run tests using the 'python' command on Windows
        stage('Test') {
            steps {
                echo 'Running unit tests...'
                // Use 'bat' (Windows Batch) instead of 'sh'
                // Use 'python' instead of 'python3' (typical for Windows)
                bat 'py unit_tests.py'
            }
        }

        // Stage 3: Build the Docker image
        stage('Build Image') {
            steps {
                echo "Building Docker image: ${DOCKER_USERNAME}/${IMAGE_NAME}..."
                // Use 'bat' to run the Docker command
                bat "docker build -t ${DOCKER_USERNAME}/${IMAGE_NAME} ."
            }
        }

        // Stage 4: Push the image to Docker Hub
        stage('Push to Docker Hub') {
            steps {
                echo 'Logging in and pushing to Docker Hub...'
                // This is the corrected 'withCredentials' block
                withCredentials([usernamePassword(credentialsId: DOCKER_CREDENTIALS_ID, usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    // Log in using the injected variables
                    bat "echo ${DOCKER_PASS} | docker login -u ${DOCKER_USER} --password-stdin"
                    // Push the image
                    bat "docker push ${DOCKER_USERNAME}/${IMAGE_NAME}:latest"
                }
            }
        }

        // Stage 5: Deploy using Ansible (run from within WSL)
        stage('Deploy') {
            steps {
                echo 'Deploying container with Ansible via WSL...'
                // This command tells Windows to run the 'ansible-playbook' command
                // inside your default WSL (Ubuntu) environment.
                // It assumes your hosts and playbook.yml file are in the workspace.
                bat 'wsl ansible-playbook -i hosts playbook.yml'
            }
        }
    }
}

