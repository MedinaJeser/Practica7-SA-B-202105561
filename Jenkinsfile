pipeline {
    agent any

    environment {
        USERS_BASE_IMAGE_NAME = "jsrmedina/users-service-p7"
        COURSES_BASE_IMAGE_NAME = "jsrmedina/courses-service-p7"
        ENROLLMENTS_BASE_IMAGE_NAME = "jsrmedina/enrollments-service-p7"
        EVALUATIONS_BASE_IMAGE_NAME = "jsrmedina/evaluations-service-p7"
        
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

                    env.USERS_FULL_IMAGE_NAME = "${env.USERS_BASE_IMAGE_NAME}:${env.GIT_COMMIT_SHORT}"
                    env.COURSES_FULL_IMAGE_NAME = "${env.COURSES_BASE_IMAGE_NAME}:${env.GIT_COMMIT_SHORT}"   
                    env.ENROLLMENTS_FULL_IMAGE_NAME = "${env.ENROLLMENTS_BASE_IMAGE_NAME}:${env.GIT_COMMIT_SHORT}"
                    env.EVALUATIONS_FULL_IMAGE_NAME = "${env.EVALUATIONS_BASE_IMAGE_NAME}:${env.GIT_COMMIT_SHORT}"                 
                }
            }
        }
        
        // stage('Instalar dependencias Python') {
        //     steps {
        //         // Crear un entorno virtual
        //         script {
        //             sh 'python3 -m venv venv'
        //             sh '. venv/bin/activate && pip install --upgrade pip'
        //             sh '. venv/bin/activate && pip install -r requirements.txt'
        //         }
        //     }
        // }

        stage('Instalar dependencias') {
            steps {
                dir('users') {
                    sh 'npm install'
                }
                dir('courses') {
                    sh 'npm install'
                }
            }
        }

        stage('Ejecutar pruebas') {
            steps {
                dir('users') {
                    sh 'npm run test'
                }
                dir('courses') {
                    sh 'npm run test'
                }
            }
        }

        stage('Construir imagenes de Docker') {
            steps {
                dir('users') {
                    sh "docker build -t ${USERS_FULL_IMAGE_NAME} ."
                }
                dir ('courses') {
                    sh "docker build -t ${env.COURSES_FULL_IMAGE_NAME} ."
                }
                dir ('enrollments') {
                    sh "docker build -t ${env.ENROLLMENTS_FULL_IMAGE_NAME} ."
                }
                dir ('evaluations') {
                    sh "docker build -t ${env.EVALUATIONS_FULL_IMAGE_NAME} ."
                }
            }
        }

        stage('Push a Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push $USERS_FULL_IMAGE_NAME
                    '''
                }
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push $COURSES_FULL_IMAGE_NAME
                    '''
                }
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push $ENROLLMENTS_FULL_IMAGE_NAME
                    '''
                }
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push $EVALUATIONS_FULL_IMAGE_NAME
                    '''
                }
            }
        }

        stage('Configurar GKE') {
            steps {
                sh "sed -i 's|IMAGE_NAME|${USERS_FULL_IMAGE_NAME}|g' ./kubernetes/users.yaml"

                step([$class: 'KubernetesEngineBuilder', 
                        projectId: env.PROJECT_ID, 
                        clusterName: env.CLUSTER_NAME, 
                        location: env.LOCATION,
                        manifestPattern: './kubernetes/users.yaml',
                        credentialsId: env.CREDENTIALS_ID,
                        verifyDeployments: false])

                sh "sed -i 's|IMAGE_NAME|${COURSES_FULL_IMAGE_NAME}|g' ./kubernetes/courses.yaml"

                step([$class: 'KubernetesEngineBuilder', 
                        projectId: env.PROJECT_ID, 
                        clusterName: env.CLUSTER_NAME, 
                        location: env.LOCATION,
                        manifestPattern: './kubernetes/courses.yaml',
                        credentialsId: env.CREDENTIALS_ID,
                        verifyDeployments: false])

                sh "sed -i 's|IMAGE_NAME|${ENROLLMENTS_FULL_IMAGE_NAME}|g' ./kubernetes/enrollments.yaml"

                step([$class: 'KubernetesEngineBuilder', 
                        projectId: env.PROJECT_ID, 
                        clusterName: env.CLUSTER_NAME, 
                        location: env.LOCATION,
                        manifestPattern: './kubernetes/enrollments.yaml',
                        credentialsId: env.CREDENTIALS_ID,
                        verifyDeployments: false])

                sh "sed -i 's|IMAGE_NAME|${EVALUATIONS_FULL_IMAGE_NAME}|g' ./kubernetes/evaluations.yaml"

                step([$class: 'KubernetesEngineBuilder', 
                        projectId: env.PROJECT_ID, 
                        clusterName: env.CLUSTER_NAME, 
                        location: env.LOCATION,
                        manifestPattern: './kubernetes/evaluations.yaml',
                        credentialsId: env.CREDENTIALS_ID,
                        verifyDeployments: false])

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
