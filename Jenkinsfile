pipeline {
    agent any
    stages {
        stage('Move Directory & Secrets')
        {
            steps {
                sh '''
                sudo chmod +x directory.sh
                ./directory.sh
                '''
            }
        }
        stage('Setup Python Virtual Environments')
        {
            steps {
                sh '''
                cd /var/www/html/tech-foring
                sudo chmod +x envsetup.sh
                ./envsetup.sh
                '''
            }
        }
        stage('Modify Ownership')
        {
            steps {
                sh '''
                sudo chown -R root:www-data /var/www/html/tech-foring
                '''
            }
        }
    }
    post {
        success {
            echo 'Pipeline completed successfully!'
        }

        failure {
            echo 'Pipeline failed.'
        }
    }
}
