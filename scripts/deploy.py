#!/usr/bin/env python3
"""
Deployment Script for CI/CD Demo Pipeline

This script simulates a deployment process by:
1. Gathering build and test information
2. Creating a deployment summary
3. Generating artifacts for archiving

In a real-world scenario, this would deploy to a server, cloud platform,
or container registry. For this demo, we create text-based artifacts.
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path


def get_environment_info():
    """
    Collect environment information for the deployment summary.
    
    Returns:
        dict: Environment information including CI/CD platform details
    """
    return {
        "timestamp": datetime.now().isoformat(),
        "python_version": sys.version,
        "platform": sys.platform,
        "cwd": os.getcwd(),
        "ci_platform": detect_ci_platform(),
        "branch": os.getenv("BRANCH_NAME", os.getenv("GIT_BRANCH", "unknown")),
        "build_number": os.getenv("BUILD_NUMBER", os.getenv("BUILD_ID", "local")),
        "enable_failing_tests": os.getenv("ENABLE_FAILING_TESTS", "false"),
    }


def detect_ci_platform():
    """
    Detect which CI/CD platform is running the build.
    
    Returns:
        str: Name of the CI/CD platform
    """
    if os.getenv("JENKINS_HOME"):
        return "Jenkins"
    elif os.getenv("TEAMCITY_VERSION"):
        return "TeamCity"
    else:
        return "Local/Unknown"


def read_test_results():
    """
    Read and parse test results from the test-results.xml file.
    
    Returns:
        dict: Test result summary
    """
    test_results_file = Path("test-results.xml")
    
    if not test_results_file.exists():
        return {
            "status": "unknown",
            "message": "Test results file not found"
        }
    
    # Simple XML parsing to extract test counts
    # In production, you'd use a proper XML parser
    try:
        content = test_results_file.read_text()
        
        # Extract basic test information
        # This is a simplified approach for demo purposes
        if 'failures="0"' in content and 'errors="0"' in content:
            status = "PASSED"
        else:
            status = "FAILED"
        
        # Count tests (simplified)
        import re
        tests_match = re.search(r'tests="(\d+)"', content)
        failures_match = re.search(r'failures="(\d+)"', content)
        errors_match = re.search(r'errors="(\d+)"', content)
        skipped_match = re.search(r'skipped="(\d+)"', content)
        
        return {
            "status": status,
            "total_tests": int(tests_match.group(1)) if tests_match else 0,
            "failures": int(failures_match.group(1)) if failures_match else 0,
            "errors": int(errors_match.group(1)) if errors_match else 0,
            "skipped": int(skipped_match.group(1)) if skipped_match else 0,
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error parsing test results: {str(e)}"
        }


def create_deployment_summary(artifact_dir):
    """
    Create a human-readable deployment summary file.
    
    Args:
        artifact_dir (Path): Directory to save the summary
    """
    env_info = get_environment_info()
    test_results = read_test_results()
    
    summary_file = artifact_dir / "deployment-summary.txt"
    
    # Create summary content
    summary_lines = [
        "=" * 70,
        "DEPLOYMENT SUMMARY",
        "=" * 70,
        "",
        f"Deployment Timestamp: {env_info['timestamp']}",
        f"CI/CD Platform: {env_info['ci_platform']}",
        f"Branch: {env_info['branch']}",
        f"Build Number: {env_info['build_number']}",
        "",
        "-" * 70,
        "BUILD CONFIGURATION",
        "-" * 70,
        "",
        f"Python Version: {env_info['python_version'].split()[0]}",
        f"Platform: {env_info['platform']}",
        f"Test Failure Mode: {env_info['enable_failing_tests']}",
        "",
        "-" * 70,
        "TEST RESULTS",
        "-" * 70,
        "",
    ]
    
    # Add test results
    if test_results["status"] in ["PASSED", "FAILED"]:
        summary_lines.extend([
            f"Status: {test_results['status']}",
            f"Total Tests: {test_results['total_tests']}",
            f"Passed: {test_results['total_tests'] - test_results['failures'] - test_results['errors']}",
            f"Failed: {test_results['failures']}",
            f"Errors: {test_results['errors']}",
            f"Skipped: {test_results['skipped']}",
        ])
    else:
        summary_lines.append(f"Status: {test_results.get('message', 'Unknown')}")
    
    summary_lines.extend([
        "",
        "-" * 70,
        "DEPLOYMENT STATUS",
        "-" * 70,
        "",
    ])
    
    # Determine overall deployment status
    if test_results["status"] == "PASSED":
        summary_lines.extend([
            "✓ DEPLOYMENT SUCCESSFUL",
            "",
            "All tests passed. The application is ready for deployment.",
            "Artifacts have been generated and are available for distribution.",
        ])
    elif test_results["status"] == "FAILED":
        summary_lines.extend([
            "✗ DEPLOYMENT FAILED",
            "",
            "Some tests failed. Review the test results before deploying.",
            "This build should not be deployed to production.",
        ])
    else:
        summary_lines.extend([
            "⚠ DEPLOYMENT STATUS UNKNOWN",
            "",
            "Unable to determine test results. Manual verification required.",
        ])
    
    summary_lines.extend([
        "",
        "=" * 70,
        "END OF DEPLOYMENT SUMMARY",
        "=" * 70,
    ])
    
    # Write summary file
    summary_file.write_text("\n".join(summary_lines))
    print(f"✓ Created deployment summary: {summary_file}")


def create_deployment_metadata(artifact_dir):
    """
    Create a machine-readable JSON metadata file.
    
    Args:
        artifact_dir (Path): Directory to save the metadata
    """
    env_info = get_environment_info()
    test_results = read_test_results()
    
    metadata = {
        "deployment": {
            "timestamp": env_info["timestamp"],
            "platform": env_info["ci_platform"],
            "branch": env_info["branch"],
            "build_number": env_info["build_number"],
        },
        "environment": {
            "python_version": env_info["python_version"].split()[0],
            "platform": env_info["platform"],
            "enable_failing_tests": env_info["enable_failing_tests"],
        },
        "test_results": test_results,
        "artifacts": {
            "summary": "deployment-summary.txt",
            "metadata": "deployment-metadata.json",
            "application": "calculator-app.txt",
        }
    }
    
    metadata_file = artifact_dir / "deployment-metadata.json"
    metadata_file.write_text(json.dumps(metadata, indent=2))
    print(f"✓ Created deployment metadata: {metadata_file}")


def create_application_artifact(artifact_dir):
    """
    Create a simulated application artifact.
    
    In a real deployment, this would be a compiled binary, Docker image,
    or packaged application. For this demo, we create a text file.
    
    Args:
        artifact_dir (Path): Directory to save the artifact
    """
    env_info = get_environment_info()
    
    artifact_content = [
        "# Calculator Application - Deployment Artifact",
        "",
        f"Version: 1.0.0",
        f"Build Date: {env_info['timestamp']}",
        f"Build Number: {env_info['build_number']}",
        f"Branch: {env_info['branch']}",
        "",
        "## Application Information",
        "",
        "This is a simulated deployment artifact for the Calculator application.",
        "In a real-world scenario, this would be:",
        "- A Docker image",
        "- A compiled binary",
        "- A packaged application (JAR, WAR, ZIP, etc.)",
        "- A deployment package for a cloud platform",
        "",
        "## Deployment Instructions",
        "",
        "1. Extract this artifact to the target environment",
        "2. Install dependencies: pip install -r requirements.txt",
        "3. Run the application: python -m src.calculator",
        "4. Verify functionality with included tests",
        "",
        "## Support",
        "",
        "For issues or questions, refer to the project README.md",
    ]
    
    artifact_file = artifact_dir / "calculator-app.txt"
    artifact_file.write_text("\n".join(artifact_content))
    print(f"✓ Created application artifact: {artifact_file}")


def main():
    """
    Main deployment function.
    
    This orchestrates the entire deployment process:
    1. Create artifact directory
    2. Generate deployment summary
    3. Create metadata file
    4. Package application artifact
    """
    print("=" * 70)
    print("DEPLOYMENT SCRIPT")
    print("=" * 70)
    print()
    
    # Determine artifact directory
    artifact_dir = Path(os.getenv("ARTIFACT_DIR", "artifacts"))
    
    # Create artifact directory if it doesn't exist
    artifact_dir.mkdir(parents=True, exist_ok=True)
    print(f"Artifact directory: {artifact_dir.absolute()}")
    print()
    
    # Generate deployment artifacts
    print("Generating deployment artifacts...")
    print()
    
    try:
        create_deployment_summary(artifact_dir)
        create_deployment_metadata(artifact_dir)
        create_application_artifact(artifact_dir)
        
        print()
        print("=" * 70)
        print("DEPLOYMENT COMPLETE")
        print("=" * 70)
        print()
        print(f"All artifacts have been created in: {artifact_dir.absolute()}")
        print()
        print("Artifacts generated:")
        for artifact_file in artifact_dir.iterdir():
            print(f"  - {artifact_file.name} ({artifact_file.stat().st_size} bytes)")
        
        return 0
        
    except Exception as e:
        print()
        print("=" * 70)
        print("DEPLOYMENT FAILED")
        print("=" * 70)
        print()
        print(f"Error: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
