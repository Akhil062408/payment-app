pipeline {
    agent any

    options {
        disableConcurrentBuilds()
        timestamps()
    }

    environment {
        IMAGE_REPO = "mycompany/payment"
        IMAGE_TAG = "${BUILD_NUMBER}"
        IMAGE = "${IMAGE_REPO}:${IMAGE_TAG}"
    }

    stages {

        stage('Build') {
            steps {
                sh '''
                    echo "======================================"
                    echo "BUILD STAGE"
                    echo "======================================"

                    echo "Jenkins Build : ${BUILD_NUMBER}"
                    echo "Git Commit    : ${GIT_COMMIT}"
                    echo "Git Branch    : ${BRANCH_NAME}"
                    echo "Docker Image  : ${IMAGE}"

                    docker build \
                      --build-arg BUILD_NUMBER="${BUILD_NUMBER}" \
                      --build-arg GIT_COMMIT="${GIT_COMMIT}" \
                      --build-arg BRANCH_NAME="${BRANCH_NAME}" \
                      --build-arg APP_VERSION="${BUILD_NUMBER}" \
                      --build-arg DOCKER_IMAGE="${IMAGE}" \
                      -t "${IMAGE}" .
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    echo "======================================"
                    echo "TEST STAGE"
                    echo "======================================"

                    docker run --rm "${IMAGE}" pytest -q
                '''
            }
        }

        stage('Tag') {
            steps {
                sh '''
                    echo "======================================"
                    echo "TAG STAGE"
                    echo "======================================"

                    docker tag "${IMAGE}" "${IMAGE_REPO}:${BUILD_NUMBER}"

                    echo "Image tagged as:"
                    docker images "${IMAGE_REPO}" --format "{{.Repository}}:{{.Tag}}"
                '''
            }
        }

        stage('Push') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'docker-registry',
                        usernameVariable: 'DOCKER_USERNAME',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {
                    sh '''
                        echo "======================================"
                        echo "PUSH STAGE"
                        echo "======================================"

                        echo "${DOCKER_PASSWORD}" | docker login \
                          -u "${DOCKER_USERNAME}" \
                          --password-stdin

                        docker push "${IMAGE}"

                        docker logout
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    echo "======================================"
                    echo "DEPLOY STAGE"
                    echo "======================================"

                    docker stop payment || true
                    docker rm payment || true

                    docker run -d \
                      --name payment \
                      -p 8080:8080 \
                      "${IMAGE}"

                    echo ""
                    echo "======================================"
                    echo "DEPLOYMENT INFORMATION"
                    echo "======================================"

                    echo "Application Version : ${BUILD_NUMBER}"
                    echo "Git Commit          : ${GIT_COMMIT}"
                    echo "Git Branch          : ${BRANCH_NAME}"
                    echo "Docker Image        : ${IMAGE}"
                    echo "Jenkins Build       : #${BUILD_NUMBER}"

                    echo ""
                    echo "Application response:"
                    sleep 3
                    curl -s http://localhost:8080

                    echo ""
                    echo ""
                    echo "Deployment complete."
                '''
            }
        }
    }
}
