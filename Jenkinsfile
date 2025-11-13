pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = "unique-ellipse-477612-c7"
        GKE_CLUSTER_NAME = "mlops-cluster"
        GCP_REGION = "us-central1"
        SERVICE_NAME = "anime-recommender"

        // Google Cloud SDK path in the Jenkins container
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

        // Build and Push Docker Image to GCR
        stage('Build and Push Docker Image to GCR'){
            steps {
                withCredentials([file(credentialsId: 'gcloud-service-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script {
                        echo 'Building and Pushing Docker image to GCR...'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}
                        gcloud auth configure-docker --quiet
                        docker build --platform linux/amd64 -t gcr.io/${GCP_PROJECT}/${SERVICE_NAME}:latest .
                        docker push gcr.io/${GCP_PROJECT}/${SERVICE_NAME}:latest 
                        '''
                    }
                }
            }
        }

        // Deploy to GKE Cluster
        stage('Deploy to GKE cluster'){
            steps{
                withCredentials([file(credentialsId: 'gcloud-service-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script{
                        echo 'Deploying to GKE Cluster...'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}
                        gcloud container clusters get-credentials ${GKE_CLUSTER_NAME} --region ${GCP_REGION}
                        kubectl apply -f deployment.yaml
                        '''
                    }
                }
            }
        }
    }
}