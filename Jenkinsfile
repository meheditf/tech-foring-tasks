pipeline {
    agent any

    environment {
        // Define environment variables
        PROJECT_NAME = 'tech-foring-tasks'
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
                        #!/bin/bash
                        python3 -m venv venv
                        . venv/bin/activate
                        pip install -r requirements.txt
                    '''
                }
            }
        }
    }
}
