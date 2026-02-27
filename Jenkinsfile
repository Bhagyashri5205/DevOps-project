pipeline {
    agent any

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main',
                url: 'https://github.com/Bhagyashri5205/DevOps-project.git'
            }
        }

        stage('Terraform Security Scan (Trivy)') {
            steps {
                sh '''
                docker run --rm \
                -v $(pwd):/project \
                aquasec/trivy config /project/terraform
                '''
            }
        }

        stage('Terraform Init') {
            steps {
                sh 'terraform init'
            }
        }

        stage('Terraform Plan') {
            steps {
                sh 'terraform plan'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t devsecops-app .'
            }
        }
    }
}