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
        stage('Checkout Repository') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            parallel {
                stage ('USERS: Install dependencies') {
                    steps {
                        dir('users') {
                            sh 'npm install'
                        }
                    }
                }

                stage ('COURSES: Install dependencies') {
                    steps {
                        dir('courses') {
                            sh 'npm install'
                        }
                    }
                }
            }
        }
        
        stage('Execute tests') {
            parallel {
                stage ('USERS: Execute tests') {
                    steps {
                        dir('users') {
                            sh 'npm run test'
                        }
                    }
                }

                stage ('COURSES: Execute tests') {
                    steps {
                        dir('courses') {
                            sh 'npm run test'
                        }
                    }
                }
            }
        }

        stage('Set image name and tag') {
                steps {
                    script {
                        def commitHash = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
                        env.GIT_COMMIT_SHORT = commitHash
                        env.USERS_FULL_IMAGE_NAME = "${env.USERS_BASE_IMAGE_NAME}:${env.GIT_COMMIT_SHORT}"
                        env.COURSES_FULL_IMAGE_NAME = "${env.COURSES_BASE_IMAGE_NAME}:${env.GIT_COMMIT_SHORT}"   
                        env.ENROLLMENTS_FULL_IMAGE_NAME = "${env.ENROLLMENTS_BASE_IMAGE_NAME}:${env.GIT_COMMIT_SHORT}"
                        env.EVALUATIONS_FULL_IMAGE_NAME = "${env.EVALUATIONS_BASE_IMAGE_NAME}:${env.GIT_COMMIT_SHORT}"                 
                    }
                }
            }
        
        stage('Build Docker images') {
            parallel {
                stage('Build USERS Docker image') {
                    steps {
                        dir('users') {
                            sh "docker build -t ${USERS_FULL_IMAGE_NAME} ."
                        }
                    }
                }
                stage('Build COURSES Docker image') {
                    steps {
                        dir('courses') {
                            sh "docker build -t ${COURSES_FULL_IMAGE_NAME} ."
                        }
                    }
                }
                stage('Build ENROLLMENTS Docker image') {
                    steps {
                        dir('enrollments') {
                            sh "docker build -t ${ENROLLMENTS_FULL_IMAGE_NAME} ."
                        }
                    }
                }
                stage('Build EVALUATIONS Docker image') {
                    steps {
                        dir('evaluations') {
                            sh "docker build -t ${EVALUATIONS_FULL_IMAGE_NAME} ."
                        }
                    }
                }        
            }
        }

        stage('Push Docker images') {
            parallel {
                stage('Push USERS Docker image') {
                    steps {
                        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                            sh '''
                                echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                                docker push $USERS_FULL_IMAGE_NAME
                            '''
                        }
                    }
                }
                stage('Push COURSES Docker image') {
                    steps {
                        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                            sh '''
                                echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                                docker push $COURSES_FULL_IMAGE_NAME
                            '''
                        }
                    }
                }
                stage('Push ENROLLMENTS Docker image') {
                    steps {
                        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                            sh '''
                                echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                                docker push $ENROLLMENTS_FULL_IMAGE_NAME
                            '''
                        }
                    }
                }
                stage('Push EVALUATIONS Docker image') {
                    steps {
                        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                            sh '''
                                echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                                docker push $EVALUATIONS_FULL_IMAGE_NAME
                            '''
                        }
                    }
                }
            }
        }
        
        stage('Deploy to Google Kubernetes') {
            steps {
                
                // Users deployment
                sh "sed -i 's|IMAGE_NAME|${USERS_FULL_IMAGE_NAME}|g' ./kubernetes/users.yaml"

                step([$class: 'KubernetesEngineBuilder', 
                        projectId: env.PROJECT_ID, 
                        clusterName: env.CLUSTER_NAME, 
                        location: env.LOCATION,
                        manifestPattern: './kubernetes/users.yaml',
                        credentialsId: env.CREDENTIALS_ID,
                        verifyDeployments: false])


                // Courses deployment
                sh "sed -i 's|IMAGE_NAME|${COURSES_FULL_IMAGE_NAME}|g' ./kubernetes/courses.yaml"

                step([$class: 'KubernetesEngineBuilder', 
                        projectId: env.PROJECT_ID, 
                        clusterName: env.CLUSTER_NAME, 
                        location: env.LOCATION,
                        manifestPattern: './kubernetes/courses.yaml',
                        credentialsId: env.CREDENTIALS_ID,
                        verifyDeployments: false])

                // Enrollments deployment
                sh "sed -i 's|IMAGE_NAME|${ENROLLMENTS_FULL_IMAGE_NAME}|g' ./kubernetes/enrollments.yaml"

                step([$class: 'KubernetesEngineBuilder', 
                        projectId: env.PROJECT_ID, 
                        clusterName: env.CLUSTER_NAME, 
                        location: env.LOCATION,
                        manifestPattern: './kubernetes/enrollments.yaml',
                        credentialsId: env.CREDENTIALS_ID,
                        verifyDeployments: false])

                // Evaluations deployment
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
            echo '✅ Pipeline finalizada correctamente'
        }
        failure {
            echo '❌ Error durante la ejecución de la pipeline'
        }
    }
}
