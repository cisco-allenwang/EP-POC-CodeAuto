pipeline {
    agent any

    stages {
        stage('SCM') {
            steps {
                checkout scm
            }
        }
        stage('Test/Sonar') {
            steps {
                // Run your Python unit tests and prepare SonarQube output
                sh "pytest --junitxml=reports/test-results.xml"
                
                // Run SonarQube analysis
                script {
                    def scannerHome = tool 'SonarScanner'
                    withSonarQubeEnv('SonarQubeServer') {
                        sh "${scannerHome}/bin/sonar-scanner -Dsonar.projectKey=your_project_key -Dsonar.sources=src -Dsonar.python.coverage.reportPaths=reports/test-results.xml"
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
