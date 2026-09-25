pipeline {
    agent any

    environment {
        IMAGE_NAME = "chronova-watch-store"
        IMAGE_TAG  = "${BUILD_NUMBER}"
    }

    stages {
        stage("Checkout") {
            steps {
                checkout scm
            }
        }

        stage("Install and Test") {
            steps {
                sh "python3 -m venv venv && . venv/bin/activate && pip install -r requirements.txt && pytest"
            }
        }

        stage("Build Docker Image") {
            steps {
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} -t ${IMAGE_NAME}:latest ."
            }
        }

        stage("Deploy") {
            steps {
                sh "docker rm -f chronova-watch-store-container || true"
                sh "docker run -d --name chronova-watch-store-container -p 5001:5000 ${IMAGE_NAME}:latest"
            }
        }
    }

    post {
        success { echo "Chronova pipeline succeeded" }
        failure { echo "Chronova pipeline failed" }
    }
}