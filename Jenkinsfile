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
              -v $PWD:/workspace \
              -w /workspace/terraform \
              aquasec/trivy:latest \
              config --misconfig-scanners terraform .
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
        withCredentials([[
            $class: 'AmazonWebServicesCredentialsBinding',
            credentialsId: 'aws-credentials'
        ]]) {
            dir('terraform') {
                sh '''
                    export AWS_DEFAULT_REGION=ap-south-1
                    export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
                    export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
                    terraform plan -var="my_ip=0.0.0.0/0"
                '''
            }
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