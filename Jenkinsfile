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
              -v $WORKSPACE/terraform:/project \
              aquasec/trivy:latest \
              config --misconfig-scanners terraform /project
        '''
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
            sh 'terraform plan -var="my_ip=0.0.0.0/0"'
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