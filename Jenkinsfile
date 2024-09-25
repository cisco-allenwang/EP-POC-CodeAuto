pipeline {
    agent any
    tools {
        sonarQube 'SonarScanner' // This should match the name you provided in the Global Tool Configuration
    }
    stage('SCM') {
        checkout scm
    }
    stages {
        stage('SonarQube analysis') {
            steps {
                script {
                    def scannerHome = tool 'SonarScanner'
                    withSonarQubeEnv('SonarQube') { // This should match the name you provided in the SonarQube server configuration
                        sh "${scannerHome}/bin/sonar-scanner"
                    }
                }
            }
        }
    }

    
}
