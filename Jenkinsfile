pipeline {
    agent any

    environment {
        // Define environment variables
        PROJECT_NAME = "tech-foring-tasks"
        }

    stages {
        stage('Checkout Code') {
            steps {
                // Clone the repository
                checkout scm
            }
        }

        stage('Setup Environment') {
            steps {
                script {
                    // Install dependencies and setup environment
                    sh '''
                        python3 -m venv venv
                        source venv/bin/activate
                        pip install -r requirements.txt
                    '''
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // Run Django tests
                    sh '''
                        source venv/bin/activate
                        python manage.py test
                    '''
                }
            }
        }

    post {
        success {
            echo "Pipeline executed successfully!"
        }
        failure {
            echo "Pipeline failed. Check the logs for details."
        }
    }
}
}
