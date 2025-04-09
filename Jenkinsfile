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
                // Instala dependencias del proyecto
                sh 'ls'
                sh 'cd users'
                sh 'ls'
                sh 'npm install'
            }
        }

        stage('Ejecutar pruebas') {
            steps {
                // Ejecuta los tests del proyecto
                sh 'npm run test'
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
