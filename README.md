# Practica7-SA-B-202105561

Documentación

# Archivos YAML: Microservicios

## Users

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: users-ms-deployment
  namespace: sa-p7
spec:
  replicas: 1
  selector:
    matchLabels:
      app: users-ms
  template:
    metadata:
      labels:
        app: users-ms
    spec:
      containers:
        - name: users-ms-container
          image: IMAGE_NAME
          ports:
            - containerPort: 3001
          env:
            - name: DATABASE_URL
              value: "mongodb+srv://admin-sa:sacluster00@clustersa.at5ngtq.mongodb.net/users_ms?retryWrites=true&w=majority&appName=ClusterSA"
          resources:
            requests:
              memory: "512Mi"
              cpu: "200m"
            limits:
              memory: "1Gi"
              cpu: "250m"
---
apiVersion: v1
kind: Service
metadata:
  name: users-ms-service
  namespace: sa-p7
spec:
  selector:
    app: users-ms
  ports:
    - protocol: TCP
      port: 3001
      targetPort: 3001
  type: ClusterIP
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: users-ms-hpa
  namespace: sa-p7
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: users-ms-deployment
  minReplicas: 1
  maxReplicas: 2
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 80
```

## Courses

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: courses-ms-deployment
  namespace: sa-p7
spec:
  replicas: 1
  selector:
    matchLabels:
      app: courses-ms
  template:
    metadata:
      labels:
        app: courses-ms
    spec:
      containers:
        - name: courses-ms-container
          image: IMAGE_NAME
          ports:
            - containerPort: 3002
          env:
            - name: DATABASE_URL
              value: "mongodb+srv://admin-sa:sacluster00@clustersa.at5ngtq.mongodb.net/courses_ms?retryWrites=true&w=majority&appName=ClusterSA"
          resources:
            requests:
              memory: "512Mi"
              cpu: "200m"
            limits:
              memory: "1Gi"
              cpu: "250m"
---
apiVersion: v1
kind: Service
metadata:
  name: courses-ms-service
  namespace: sa-p7
spec:
  selector:
    app: courses-ms
  ports:
    - protocol: TCP
      port: 3002
      targetPort: 3002
  type: ClusterIP
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: courses-ms-hpa
  namespace: sa-p7
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: courses-ms-deployment
  minReplicas: 1
  maxReplicas: 2
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 80
```

## Enrollments

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: enrollments-ms-deployment
  namespace: sa-p7
spec:
  replicas: 1
  selector:
    matchLabels:
      app: enrollments-ms
  template:
    metadata:
      labels:
        app: enrollments-ms
    spec:
      containers:
        - name: enrollments-ms-container
          image: IMAGE_NAME
          ports:
            - containerPort: 8002
          env:
            - name: DATABASE_URL
              value: "mongodb+srv://admin-sa:sacluster00@clustersa.at5ngtq.mongodb.net/enrollments_ms?retryWrites=true&w=majority&appName=ClusterSA"
          resources:
            requests:
              memory: "512Mi"
              cpu: "200m"
            limits:
              memory: "1Gi"
              cpu: "250m"
---
apiVersion: v1
kind: Service
metadata:
  name: enrollments-ms-service
  namespace: sa-p7
spec:
  selector:
    app: enrollments-ms
  ports:
    - protocol: TCP
      port: 8002
      targetPort: 8002
  type: ClusterIP
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: enrollments-ms-hpa
  namespace: sa-p7
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: enrollments-ms-deployment
  minReplicas: 1
  maxReplicas: 2
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 80
```

## Evaluations

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: evaluations-ms-deployment
  namespace: sa-p7
spec:
  replicas: 1
  selector:
    matchLabels:
      app: evaluations-ms
  template:
    metadata:
      labels:
        app: evaluations-ms
    spec:
      containers:
        - name: evaluations-ms-container
          image: IMAGE_NAME
          ports:
            - containerPort: 8001
          env:
            - name: DATABASE_URL
              value: "mongodb+srv://admin-sa:sacluster00@clustersa.at5ngtq.mongodb.net/evaluations_ms?retryWrites=true&w=majority&appName=ClusterSA"
          resources:
            requests:
              memory: "512Mi"
              cpu: "200m"
            limits:
              memory: "1Gi"
              cpu: "250m"
---
apiVersion: v1
kind: Service
metadata:
  name: evaluations-ms-service
  namespace: sa-p7
spec:
  selector:
    app: evaluations-ms
  ports:
    - protocol: TCP
      port: 8001
      targetPort: 8001
  type: ClusterIP
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: evaluations-ms-hpa
  namespace: sa-p7
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: evaluations-ms-deployment
  minReplicas: 1
  maxReplicas: 2
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 80
```

# Configuración del pipeline CI/CD para construir, probar y desplegar el código.

```Jenkinsfile
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

```

# Descripción de cómo funciona el pipeline

Este pipeline de Jenkins está diseñado para automatizar el proceso de integración y despliegue continuo (CI/CD) de una arquitectura basada en microservicios. Específicamente, gestiona cuatro servicios principales: users, courses, enrollments y evaluations. El objetivo es garantizar que cada uno de estos servicios se construya, pruebe y despliegue de manera eficiente en un clúster de Google Kubernetes Engine (GKE).

La ejecución del pipeline comienza con la definición de variables de entorno esenciales que permiten una configuración dinámica. Estas variables incluyen los nombres base de las imágenes Docker para cada microservicio, la información del clúster de GKE (como el project ID, el nombre del clúster, la zona y el namespace) y las credenciales necesarias para autenticarse tanto en Docker Hub como en GKE.

Luego, el pipeline se estructura en varias etapas:

- Checkout del repositorio: Se clona el código fuente desde el repositorio configurado en Jenkins. Esta acción permite acceder a todos los archivos necesarios para las siguientes etapas del pipeline.

- Instalación de dependencias: En esta etapa, se ejecuta el comando npm install para los servicios users y courses, lo cual asegura que todas las dependencias definidas en el archivo package.json estén disponibles para ejecutar pruebas o construir las imágenes.

- Ejecución de pruebas: De forma paralela, se ejecutan las pruebas unitarias para los servicios users y courses utilizando npm run test. Esta etapa permite detectar errores lógicos o de implementación antes de proceder con la construcción de imágenes. Es importante notar que los servicios enrollments y evaluations no tienen pruebas definidas en este pipeline.

- Definición del nombre y tag de las imágenes Docker: Se genera una etiqueta única basada en el hash corto del commit actual de Git. Esta etiqueta se concatena con el nombre base de cada imagen para crear identificadores únicos que permiten versionar las imágenes Docker.

- Construcción de imágenes Docker: Cada uno de los cuatro microservicios es empaquetado en una imagen Docker. Esta operación se realiza en paralelo para acelerar el proceso de construcción.

- Subida de imágenes a Docker Hub: Una vez construidas, las imágenes se suben al repositorio remoto Docker Hub utilizando credenciales previamente configuradas en Jenkins. Esta etapa también se ejecuta en paralelo para cada servicio.

- Despliegue en Google Kubernetes Engine (GKE): Finalmente, las imágenes subidas se despliegan en el clúster de Kubernetes. Para ello, se actualizan los archivos YAML de despliegue reemplazando la etiqueta IMAGE_NAME por el nombre completo de la imagen construida. Luego, se utiliza el plugin KubernetesEngineBuilder para aplicar los manifiestos y desplegar cada servicio en su respectivo contenedor dentro del clúster.

Una vez completadas todas las etapas, el pipeline finaliza con una sección post que notifica si la ejecución fue exitosa o si ocurrió algún error. En caso de éxito, se imprime el mensaje "✅ Pipeline finalizada correctamente", y en caso de fallo, se muestra "❌ Error durante la ejecución de la pipeline".

![Docker Hub](./imgs/docker-hub.png)

![Pipeline](./imgs/pipeline.png)

![Jenkins Pipeline](./imgs/jenkins-pipeline.png)

![Jenkins Output](./imgs/jenkins-output.png)

![Deployments Lens](./imgs/deployments-lens.png)

![Deployments Terminal](./imgs/deployments-terminal.png)