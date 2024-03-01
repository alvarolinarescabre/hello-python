pipeline {
    agent { 
        kubernetes {
            yamlFile 'k8s/build-pod.yaml'
        }
    }

    environment {
        APP_NAME        = 'hello-python'
    	REPO_URL        = 'ghcr.io'
        REPO_USER       = 'alvarolinarescabre'
        LOGIN_CREDS     = credentials('github_login')
        K8S_DEPLOY_FILE = 'k8s/deployment.yaml'
    }

    options {
        ansiColor('xterm')
        skipDefaultCheckout()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Image') {
            steps {
                container('docker') {
                    sh (label: 'Building Image', script: 'docker build . -t $REPO_URL/$REPO_USER/$APP_NAME:$BUILD_NUMBER')
                    sh (label: 'Image Tagging', script: 'docker tag $REPO_URL/$REPO_USER/$APP_NAME:$BUILD_NUMBER $REPO_URL/$REPO_USER/$APP_NAME:latest')
                    sh (label: 'Docker Image List', script: 'docker image list')
                }
            }
        }

        stage('Push Image to GitHub') {
            steps {
                container('docker') {
                    sh (label: 'Login GitHub', script: "echo $LOGIN_CREDS_PSW | docker login  --username $LOGIN_CREDS_USR --password-stdin $REPO_URL")
                    sh (label: "Push image ${env.BUILD_NUMBER}", script: "docker push $REPO_URL/$REPO_USER/$APP_NAME:$BUILD_NUMBER")
                    sh (label: "Push image 'latest'", script: "docker push $REPO_URL/$REPO_USER/$APP_NAME:latest")
                }
            }
        }

         stage('Deploy to Kubernetes') {
            steps {
                container('docker') {
                    script {
                        sh (label: 'Changes Version', script: "sed -i s/CHANGE_VERSION/$BUILD_NUMBER/g '${WORKSPACE}/${K8S_DEPLOY_FILE}'")
                        sh (label: 'Show Changes', script: "cat ${WORKSPACE}/${env.K8S_DEPLOY_FILE}")
                        sh (label: 'Apply Deployment', script: "kubectl apply -f ${WORKSPACE}/${env.K8S_DEPLOY_FILE}")
                    }
                }
            }
        }	
    }

    post {
        always {
            deleteDir()
        }
        failure {
            echo 'The build failed. Please check the logs.'
        }
    }
}
