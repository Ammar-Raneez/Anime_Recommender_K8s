pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = "unique-ellipse-477612-c7"
        GCP_REGION = "us-central1"
        SERVICE_NAME = "hotel-prediction-mlops"

        // Google Cloud SDK path on the Jenkins container
        GCLOUD_PATH = "/lib/google-cloud-sdk/bin"
    }

    stages {
        // this stage clones the repo to Jenkins (this is done within Jenkins pipeline by default)
        stage('Clone repo to Jenkins') {
            steps {
                script {
                    echo 'Cloning repo to Jenkins...'
                }
            }
        }

        // Set up Python virtual environment and application setup.py
        stage('Set up virtual environment and install dependencies') {
            steps {
                script {
                    echo 'Setting up virtual environment and installing dependencies...'
                    sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    '''
                }
            }
        }

        // Pull DVC data from GCP bucket
        stage('Pull DVC data from GCP bucket') {
            steps {
                withCredentials([file(credentialsId: 'gcloud-service-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script {
                        echo 'Pulling DVC data from GCP bucket...'
                        sh '''
                        . ${VENV_DIR}/bin/activate
                        dvc pull
                        '''
                    }
                }
            }
        }
    }
}