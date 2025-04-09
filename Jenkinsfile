pipeline {
    agent any

    environment {
        NODE_ENV = 'test'
        IMAGE_NAME = "jsrmedina/users-service-p7:${commit}"
    }

    tools {
        nodejs 'recent node'
    }

    stages {
        stage('Checkout') {
            steps {
                // Clona el repositorio
                checkout scm
            }
        }

        stage('Obtener commit hash') {
            steps {
                script {
                    def commit = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
                    env.IMAGE_NAME = "jeser/users-service:${commit}"
                }
            }
        }

        stage('Instalar dependencias') {
            steps {
                dir('users') {
                    sh 'npm install'
                }
            }
        }

        stage('Ejecutar pruebas') {
            steps {
                dir('users') {
                    // Ejecuta los tests de la aplicación
                    sh 'npm run test'
                }
            }
        }

        stage('Construir imagen Docker') {
            steps {
                dir('users') {
                    sh "docker build -t $IMAGE_NAME ."
                }
            }
        }

        stage('Push a Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push $IMAGE_NAME
                    '''
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline finalizada'
        }
        success {
            echo '✅ Todo salió bien'
        }
        failure {
            echo '❌ Algo falló'
        }
    }
}
