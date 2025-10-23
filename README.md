# TeamCity Configuration

This directory contains the TeamCity pipeline configuration written in Kotlin DSL.

## Files

- **settings.kts**: Main TeamCity configuration file defining the build pipeline

## How TeamCity Configuration Works

TeamCity uses a "Configuration as Code" approach with Kotlin DSL:

1. **Automatic Detection**: When you connect TeamCity to this repository, it automatically detects the `.teamcity/` directory
2. **Version Control**: Configuration is stored in VCS alongside your code
3. **Type Safety**: Kotlin provides compile-time checking and IDE support
4. **Reusability**: Easy to create templates and share configuration

## Setting Up in TeamCity

### Option 1: Automatic Setup (Recommended)

1. In TeamCity, create a new project
2. Connect it to your repository
3. TeamCity will detect the `.teamcity/settings.kts` file
4. Choose "Import settings from VCS"
5. TeamCity will create the build configurations automatically

### Option 2: Manual Setup

If you prefer to configure manually through the UI:

1. Create a new Build Configuration
2. Add VCS root pointing to this repository
3. Add build steps matching the configuration in `settings.kts`
4. Set the `ENABLE_FAILING_TESTS` parameter as needed

## Build Configurations

This configuration defines two build types:

### 1. CI/CD Demo Pipeline (Passing)
- `ENABLE_FAILING_TESTS=false`
- All tests pass
- Shows successful pipeline execution

### 2. CI/CD Demo Pipeline (Failing)
- `ENABLE_FAILING_TESTS=true`
- Some tests fail intentionally
- Demonstrates error handling and reporting

## Parameters

You can modify these parameters in TeamCity UI:

- **ENABLE_FAILING_TESTS**: Set to `true` to enable failing tests
- **PYTHON_VERSION**: Python version to use (default: 3.11)
- **ARTIFACT_DIR**: Directory for deployment artifacts

## Comparing with Jenkins

Key differences from Jenkins:

| Aspect | Jenkins | TeamCity |
|--------|---------|----------|
| Configuration | Groovy (Jenkinsfile) | Kotlin DSL (settings.kts) |
| Location | Root directory | .teamcity/ directory |
| UI Integration | Basic | Rich, interactive |
| Test Reporting | Plugin-based | Built-in |
| Artifact Handling | Manual archiving | Declarative rules |

## Troubleshooting

If TeamCity doesn't detect the configuration:

1. Ensure the file is named exactly `settings.kts`
2. Check that it's in the `.teamcity/` directory
3. Verify the Kotlin syntax is valid
4. Check TeamCity logs for parsing errors

## Learn More

- [TeamCity Kotlin DSL Documentation](https://www.jetbrains.com/help/teamcity/kotlin-dsl.html)
- [Build Configuration Settings](https://www.jetbrains.com/help/teamcity/build-configuration-settings.html)
