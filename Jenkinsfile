pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'  // Directory for the virtual environment
    }

    stages {
        stage('SCM') {
            steps {
                checkout scm
            }
        }
        stage('Setup Python Environment') {
            steps {
                // Install Python and create a virtual environment
                sh '''
                    python3 -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install pytest
                '''
            }
        }
        stage('Test/Sonar') {
            steps {
                // Run your Python unit tests and prepare SonarQube output
                sh '''
                    . ${VENV_DIR}/bin/activate
                    pytest --junitxml=reports/test-results.xml
                '''
                
                // Run SonarQube analysis
                script {
                    def scannerHome = tool 'SonarScanner'
                    withSonarQubeEnv('SonarQubeServer') {
                        sh """
                            . ${VENV_DIR}/bin/activate
                            ${scannerHome}/bin/sonar-scanner -Dsonar.projectKey=your_project_key -Dsonar.sources=src -Dsonar.python.coverage.reportPaths=reports/test-results.xml
                        """
                    }
                }
                
                // Wait for SonarQube Quality Gate result
                script {
                    def qg = waitForQualityGate() // Reuse taskId previously
                    if (qg.status != 'OK') {
                        echo "Pipeline aborted due to quality gate failure: ${qg.status}"
                        error "Quality Gate failed"
                    } else {
                        echo "Quality Gate Status : ${qg.status}"
                    }
                    sendSparkMessage("** Sonar Quality Gate Status : ${qg.status} **")
                }
            }
            post {
                success {
                    junit testResults: 'reports/test-results.xml', allowEmptyResults: true
                }
            }
        }
    }
}
