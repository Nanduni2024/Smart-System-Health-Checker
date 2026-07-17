pipeline {
    agent any

    environment {
        IMAGE_NAME     = "smart-system-health-checker"
        IMAGE_TAG      = "${env.BUILD_NUMBER}"
        CONTAINER_NAME = "health-checker-app"
        APP_PORT       = "8501"
    }

    options {
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {

        stage('1. Checkout') {
            steps {
                echo "Cloning repository..."
                checkout scm
            }
        }

        stage('2. Setup Python') {
            steps {
                echo "Setting up Python virtual environment..."
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                '''
            }
        }

        stage('3. Install Dependencies') {
            steps {
                echo "Installing dependencies from requirements.txt..."
                sh '''
                    . venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('4. Run Tests') {
            steps {
                echo "Running pytest..."
                sh '''
                    . venv/bin/activate
                    pytest tests/ -v --junitxml=test-results.xml
                '''
            }
            post {
                always {
                    junit 'test-results.xml'
                }
            }
        }

        stage('5. Build Docker Image') {
            steps {
                echo "Building Docker image..."
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} -t ${IMAGE_NAME}:latest ."
            }
        }

        stage('6. Stop Old Container') {
            steps {
                echo "Stopping and removing old container (if it exists)..."
                sh '''
                    docker stop ${CONTAINER_NAME} || true
                    docker rm ${CONTAINER_NAME} || true
                '''
            }
        }

        stage('7. Deploy New Container') {
            steps {
                echo "Starting new container..."
                sh '''
                    docker run -d --name ${CONTAINER_NAME} -p ${APP_PORT}:8501 --restart unless-stopped ${IMAGE_NAME}:latest
                '''
            }
        }

        stage('8. Health Check') {
            steps {
                echo "Waiting for app to become healthy..."
                sh '''
                    sleep 10
                    curl --fail http://localhost:${APP_PORT}/_stcore/health
                '''
            }
        }
    }

    post {
        success {
            echo "Pipeline succeeded! App deployed."
        }
        failure {
            echo "Pipeline failed. Check the logs above."
        }
        always {
            echo "Pipeline finished."
        }
    }
}