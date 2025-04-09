pipeline {
    agent {
        docker {
            image 'node:18'
            args '-u root:root'  
        }
    }
    stages {
       
        stage('Instalar Dependencias') {
            steps {
                script {
                    // Instalar dependencias dentro del contenedor Docker
                    sh 'cd users'
                    sh 'npm install'
                }
            }
        }

        stage('Ejecutar Pruebas') {
            steps {
                script {
                    // Ejecutar pruebas dentro del contenedor Docker
                    sh 'npm test'
                }
            }
        }
    }
}
