pipeline {
    agent {
        docker {
            image 'node:18' // Usamos una imagen de Node.js (puedes elegir otra versión si prefieres)
            label 'docker' // Asegúrate de que tu agente tenga habilitado Docker
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
