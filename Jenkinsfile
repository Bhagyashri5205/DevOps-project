pipeline {
    agent any

    options {
        skipDefaultCheckout(true)
    }

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Terraform Security Scan (Trivy)') {
            steps {
                sh '''
                docker run --rm \
                    -v $(pwd):/project \
                aquasec/trivy config /project                '''
            }
        }

        stage('Terraform Init') {
          steps {
          dir('terraform') {
            sh 'terraform init'
         }
          }
        }


        stage('Terraform Plan') {
           steps {
           dir('terraform') {
            sh 'terraform plan'
          }
         }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t devsecops-app .'
            }
        }
    }
}