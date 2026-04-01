pipeline {
    agent any

    options {
        timestamps()
    }

    environment {
        PYTHON_VERSION = '3.10'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python') {
            steps {
                sh '''
                    set -e
                    python3 --version
                    python3 -m venv .venv
                    . .venv/bin/activate
                    python -m pip install --upgrade pip
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    set -e
                    . .venv/bin/activate
                    if [ -f requirements.txt ]; then
                        pip install -r requirements.txt
                    fi
                    pip install ruff pytest coverage
                '''
            }
        }

        stage('Lint with Ruff (non-blocking)') {
            steps {
                catchError(buildResult: 'SUCCESS', stageResult: 'UNSTABLE') {
                    sh '''
                        set -e
                        . .venv/bin/activate
                        ruff check --output-format=github --target-version=py310 .
                    '''
                }
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    set -e
                    . .venv/bin/activate
                    coverage run -m pytest -v -s
                '''
            }
        }

        stage('Coverage Report') {
            steps {
                sh '''
                    set -e
                    . .venv/bin/activate
                    coverage report -m
                '''
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: '.coverage', onlyIfSuccessful: false
        }
    }
}
