pipeline {
    agent any

    environment {
        NODE_ENV = 'test'
        IMAGE_NAME = "jsrmedina/users-service-p7"
        PROJECT_ID = 'sa-projects-10101'
        CLUSTER_NAME = 'cluster-sa-p7'
        LOCATION = 'us-central1-a'
        CREDENTIALS_ID = 'gke-sa-key'
        NAMESPACE = 'sa-p7'
    }

    tools {
        nodejs 'recent node'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Obtener commit hash') {
            steps {
                script {
                    // Obtiene el commit hash corto
                    def commitHash = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
                    
                    // Asigna el commit hash a una variable de entorno
                    env.GIT_COMMIT_SHORT = commitHash

                    env.FULL_IMAGE_NAME = "${env.IMAGE_NAME}:${env.GIT_COMMIT_SHORT}"                    
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
                    sh 'npm run test'
                }
            }
        }

        stage('Construir imagen Docker') {
            steps {
                dir('users') {
                    sh "docker build -t ${FULL_IMAGE_NAME} ."
                }
            }
        }

        stage('Push a Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push $FULL_IMAGE_NAME
                    '''
                }
            }
        }

        stage('Configurar GKE') {
            steps {
                sh "sed -i 's|IMAGE_NAME|${FULL_IMAGE_NAME}|g' ./kubernetes/users.yaml"

                step([$class: 'KubernetesEngineBuilder', 
                        projectId: env.PROJECT_ID, 
                        clusterName: env.CLUSTER_NAME, 
                        location: env.LOCATION,
                        manifestPattern: './kubernetes/users.yaml',
                        credentialsId: env.CREDENTIALS_ID,
                        verifyDeployments: true])

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
