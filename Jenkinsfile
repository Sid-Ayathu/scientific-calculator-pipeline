// pipeline {
//     // agent {
//     //     docker {
//     //         image 'python:3.10-alpine'
//     //         args '-v /var/run/docker.sock:/var/run/docker.sock'
//     //     }
//     // }

//     agent any

//     environment {
//         DOCKERHUB_USERNAME = 'salvoslayer'
//         IMAGE_NAME = "${DOCKERHUB_USERNAME}/scientific_calculator"
//         DOCKER_CREDENTIALS_ID = 'dockerhub-credentials' 
//     }

//     stages {
//         stage('Checkout') {
//             steps {
//                 deleteDir()  // Clean workspace
//                 git branch: 'main', url: 'https://github.com/Sid-Ayathu/scientific-calculator-pipeline.git'
//             }
//         }

//         stage('Test') {
//             steps {
//                 echo 'Installing dependencies and running tests...'
//                 sh '''
//                     apk add --no-cache py3-pip
//                     pip install -r requirements.txt || true
//                     python3 -m unittest discover -v
//                 '''
//             }
//         }

//         stage('Build Docker Image') {
//             steps {
//                 echo 'Building Docker image...'
//                 sh """
//                     docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} .
//                     docker tag ${IMAGE_NAME}:${BUILD_NUMBER} ${IMAGE_NAME}:latest
//                 """
//             }
//         }

//         stage('Push to Docker Hub') {
//             steps {
//                 echo 'Pushing image to Docker Hub...'
//                 withCredentials([usernamePassword(credentialsId: DOCKER_CREDENTIALS_ID, usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
//                     sh """
//                         echo ${DOCKER_PASS} | docker login -u ${DOCKER_USER} --password-stdin
//                         docker push ${IMAGE_NAME}:${BUILD_NUMBER}
//                         docker push ${IMAGE_NAME}:latest
//                     """
//                 }
//             }
//         }

//         stage('Deploy') {
//             steps {
//                 echo 'Installing Ansible and deploying...'
//                 sh '''
//                     apk add --no-cache ansible
//                     ansible-playbook -i hosts playbook.yml
//                 '''
//             }
//         }
//     }

//     post {
//         success { echo '✅ Pipeline completed successfully!' }
//         failure { echo '❌ Pipeline failed!' }
//     }
// }

//aruns jenkinfile
pipeline {
    agent {
        label 'wsl'   // use a node or agent configured to run in WSL
    }

    environment {
        PATH = "/usr/bin:/usr/local/bin:${env.PATH}"   // make sure WSL binaries are accessible
        PYTHONUNBUFFERED = '1'
        IMAGE_NAME = "scientific-calculator:latest"
    }

    stages {
        stage('Setup Environment') {
            steps {
                sh '''
                echo "Running on $(uname -a)"
                python3 --version || sudo apt install -y python3
                pip3 --version || sudo apt install -y python3-pip
                ansible --version || sudo apt install -y ansible
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                echo "Installing Python dependencies..."
                pip3 install --user -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                echo "Running pytest..."
                python3 -m pytest --maxfail=1 --disable-warnings -q
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                echo "Building Docker image inside WSL..."
                docker --version
                docker build -t $IMAGE_NAME .
                '''
            }
        }

        stage('Push to DockerHub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                    echo "Logging into DockerHub..."
                    echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                    docker push $IMAGE_NAME
                    '''
                }
            }
        }

        stage('Deploy with Ansible') {
            steps {
                sh '''
                echo "Running Ansible deployment..."
                ansible-playbook ansible/deploy.yml
                '''
            }
        }
    }

    post {
        success {
            mail to: 'legendaryedd749@gmail.com',
                subject: "✅ Build Success - ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: "Build succeeded. Docker image pushed successfully to DockerHub."
        }

        failure {
            mail to: 'legendaryedd749@gmail.com',
                subject: "❌ Build Failed - ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: "Build failed. Please check Jenkins logs for details."
        }
    }
}
