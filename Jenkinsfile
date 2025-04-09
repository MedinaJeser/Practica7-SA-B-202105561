pipeline {
    agent any

    environment {
        NODE_ENV = 'test'
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
