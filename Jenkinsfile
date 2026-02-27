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
              -v $(pwd)/terraform:/project \
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
    environment {
        AWS_ACCESS_KEY_ID = credentials('aws-access-key')
        AWS_SECRET_ACCESS_KEY = credentials('aws-secret-key')
        AWS_DEFAULT_REGION = 'ap-south-1'
    }
    steps {
        dir('terraform') {
            sh 'terraform plan -var=my_ip=0.0.0.0/0'
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