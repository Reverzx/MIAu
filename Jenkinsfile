pipeline {
    agent any

    parameters {
        choice(name: 'TEST_SUITE', choices: ['regression', 'smoke', 'api', 'ui'], description: 'Select a test siut to run')
    }

    triggers {
        cron('H 7 * * *')
    }

    environment {
        VENV_DIR = 'venv'
    }

    stages {
        stage('Checkout source code') {
            steps {
                 git url: 'git@github.com:Reverzx/MIAu.git', branch: 'main', credentialsId: 'github-ssh'
            }
        }

        stage('Set up virtual env and install dependencies') {
            steps {
                 script {
                     sh """
                        python3 -m venv ${env.VENV_DIR}
                        . ${env.VENV_DIR}/bin/activate
                        pip install --upgrade pip
                        pip install -r requirements.txt
                        pip install allure-pytest
                        rm -rf allure-results
                     """
                 }
            }
        }

        stage('Run tests') {
            steps {
                script {
                    def isCron = currentBuild.rawBuild.getCauses().toString().contains("TimerTrigger")
                    def suite = isCron ? 'regression' : params.TEST_SUITE
                    echo "Launching tests with marker: ${suite}"
                    sh ". ${env.VENV_DIR}/bin/activate && pytest -m ${suite} --alluredir=allure-results"
                }
            }
        }

        stage('Allure Report') {
            steps {
                echo 'Generating Allure report...'
                allure([
                    includeProperties: false,
                    jdk: '',
                    results: [[path: 'allure-results']]
                ])
            }
        }
    }

    post {
        failure {
            echo 'Build failed. Attempting to generate Allure report in the post block...'
            script {
                try {
                    allure([
                        includeProperties: false,
                        jdk: '',
                        results: [[path: 'allure-results']]
                    ])
                } catch (Exception e) {
                    echo "Failed to generate Allure report after the failure: ${e.message}"
                }
            }
        }
    }
}
