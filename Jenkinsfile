pipeline {
    agent any

    environment {
        NODE_ENV = 'test'
        IMAGE_NAME = "jsrmedina/users-service-p7:${commit}"

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
                // Clona el repositorio
                checkout scm
            }
        }

        stage('Obtener commit hash') {
            steps {
                script {
                    def commit = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
                    env.IMAGE_NAME = "jeser/users-service:${commit}"
                }
            }
        }

        // stage('Instalar dependencias') {
        //     steps {
        //         dir('users') {
        //             sh 'npm install'
        //         }
        //     }
        // }

        // stage('Ejecutar pruebas') {
        //     steps {
        //         dir('users') {
        //             // Ejecuta los tests de la aplicación
        //             sh 'npm run test'
        //         }
        //     }
        // }

        // stage('Construir imagen Docker') {
        //     steps {
        //         dir('users') {
        //             sh "docker build -t $IMAGE_NAME ."
        //         }
        //     }
        // }

        // stage('Push a Docker Hub') {
        //     steps {
        //         withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
        //             sh '''
        //                 echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
        //                 docker push $IMAGE_NAME
        //             '''
        //         }
        //     }
        // }

        stage('Configurar GKE') {
            steps {
                step([$class: 'KubernetesEngineBuilder', projectId: env.PROJECT_ID, clusterName: env.CLUSTER_NAME, location: env.LOCATION, manifestPattern: './kubernetes/namespace.yaml', credentialsId: env.CREDENTIALS_ID, verifyDeployments: true])
                
                echo 'Deployment Finished ...'
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
