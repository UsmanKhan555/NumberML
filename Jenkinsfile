pipeline {
    agent any
    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t mnist-classification .'
                }
            }
        }
        stage('Run Tests') {
            steps {
                script {
                    sh 'docker run mnist-classification pytest'
                }
            }
        }
    }
}
