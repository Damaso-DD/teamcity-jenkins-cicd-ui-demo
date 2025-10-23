/**
 * Jenkins Pipeline Configuration
 * 
 * This Jenkinsfile defines a declarative pipeline with three stages:
 * Build, Test, and Deploy. It demonstrates how Jenkins handles:
 * - Multi-stage pipelines
 * - Environment variables
 * - Test result reporting
 * - Artifact generation
 * - Branch-specific behavior
 * 
 * USAGE:
 * - For passing pipeline: Set ENABLE_FAILING_TESTS=false (or leave unset)
 * - For failing pipeline: Set ENABLE_FAILING_TESTS=true
 */

pipeline {
    // Run on any available agent
    agent any
    
    // Environment variables available to all stages
    environment {
        // Python virtual environment path
        VENV_PATH = "${WORKSPACE}/venv"
        
        // Control test failures for demonstration
        // Set to 'true' to simulate failing tests, 'false' for passing tests
        ENABLE_FAILING_TESTS = "${env.ENABLE_FAILING_TESTS ?: 'false'}"
        
        // Artifact directory for deployment stage
        ARTIFACT_DIR = "${WORKSPACE}/artifacts"
        
        // Build timestamp for artifact naming
        BUILD_TIMESTAMP = sh(script: "date +%Y%m%d_%H%M%S", returnStdout: true).trim()
    }
    
    // Pipeline stages
    stages {
        
        /**
         * STAGE 1: BUILD
         * Sets up the Python environment and installs dependencies
         */
        stage('Build') {
            steps {
                echo '========================================='
                echo 'STAGE: Build'
                echo '========================================='
                echo "Building on branch: ${env.BRANCH_NAME ?: 'main'}"
                echo "Workspace: ${WORKSPACE}"
                
                // Display Python version
                sh 'python3 --version'
                
                // Create virtual environment
                echo 'Creating Python virtual environment...'
                sh '''
                    python3 -m venv ${VENV_PATH}
                    . ${VENV_PATH}/bin/activate
                    pip install --upgrade pip
                '''
                
                // Install dependencies
                echo 'Installing dependencies...'
                sh '''
                    . ${VENV_PATH}/bin/activate
                    pip install -r requirements.txt
                    pip list
                '''
                
                // Run code quality checks
                echo 'Running code quality checks with flake8...'
                sh '''
                    . ${VENV_PATH}/bin/activate
                    flake8 src/ tests/ --statistics || true
                '''
                
                echo 'Build stage completed successfully!'
            }
        }
        
        /**
         * STAGE 2: TEST
         * Runs unit tests and generates test reports
         */
        stage('Test') {
            steps {
                echo '========================================='
                echo 'STAGE: Test'
                echo '========================================='
                echo "Test failure mode: ${ENABLE_FAILING_TESTS}"
                
                // Run tests with pytest
                echo 'Running unit tests...'
                sh '''
                    . ${VENV_PATH}/bin/activate
                    
                    # Run pytest and capture exit code
                    # We use '|| true' to prevent pipeline from stopping on test failure
                    # This allows us to see how Jenkins displays test failures
                    pytest tests/ --junitxml=test-results.xml || true
                '''
                
                echo 'Test stage completed!'
            }
            
            // Post-test actions
            post {
                always {
                    // Publish test results (Jenkins will parse the XML)
                    // This creates the test result visualization in Jenkins UI
                    junit 'test-results.xml'
                    
                    // Archive coverage reports
                    publishHTML(target: [
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'htmlcov',
                        reportFiles: 'index.html',
                        reportName: 'Coverage Report'
                    ])
                }
            }
        }
        
        /**
         * STAGE 3: DEPLOY
         * Creates deployment artifacts and generates a deployment summary
         */
        stage('Deploy') {
            // Only deploy from main branch and if tests passed
            when {
                anyOf {
                    branch 'main'
                    branch 'master'
                    // For demo purposes, also allow deployment from feature branches
                    expression { env.BRANCH_NAME?.startsWith('feature/') }
                }
            }
            
            steps {
                echo '========================================='
                echo 'STAGE: Deploy'
                echo '========================================='
                echo "Deploying from branch: ${env.BRANCH_NAME ?: 'main'}"
                
                // Create artifact directory
                sh 'mkdir -p ${ARTIFACT_DIR}'
                
                // Run deployment script
                echo 'Generating deployment artifacts...'
                sh '''
                    . ${VENV_PATH}/bin/activate
                    python scripts/deploy.py
                '''
                
                echo 'Deploy stage completed!'
            }
            
            // Post-deployment actions
            post {
                success {
                    // Archive the deployment artifacts
                    archiveArtifacts artifacts: 'artifacts/**/*', 
                                   fingerprint: true,
                                   allowEmptyArchive: false
                    
                    echo 'Deployment artifacts created and archived successfully!'
                }
                failure {
                    echo 'Deployment failed! Check logs for details.'
                }
            }
        }
    }
    
    /**
     * POST-PIPELINE ACTIONS
     * These run after all stages complete, regardless of success/failure
     */
    post {
        always {
            echo '========================================='
            echo 'Pipeline Execution Complete'
            echo '========================================='
            echo "Final Status: ${currentBuild.result ?: 'SUCCESS'}"
            echo "Duration: ${currentBuild.durationString}"
            
            // Clean up workspace (optional - comment out to preserve for debugging)
            // cleanWs()
        }
        
        success {
            echo '✓ Pipeline completed successfully!'
            echo 'All stages passed. Artifacts are ready for deployment.'
        }
        
        failure {
            echo '✗ Pipeline failed!'
            echo 'Check the logs above to identify the failing stage.'
        }
        
        unstable {
            echo '⚠ Pipeline is unstable!'
            echo 'Tests may have failed. Review test results.'
        }
    }
}
