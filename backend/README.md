# Ranked Choice Backend

## Configuring PyCharm to Run Tests with pytest

This guide will walk you through the process of configuring PyCharm to run the tests in this project using pytest.

### Initial Setup

1. **Open the project in PyCharm**
   - Launch PyCharm
   - Select "Open" and navigate to the `ranked-choice` directory
   - Click "OK" to open the project

2. **Configure the Python Interpreter**
   - Go to File > Settings (or PyCharm > Preferences on macOS)
   - Navigate to Project: ranked-choice > Python Interpreter
   - Click the gear icon and select "Add..."
   - Choose "Virtualenv Environment" > "New environment"
   - Set the location to `/home/mike/bin/ranked-choice/.venv` (or your preferred location)
   - Select a base interpreter (Python 3.8+ recommended)
   - Click "OK" to create the virtual environment

3. **Install the project in development mode**
   - Open a terminal in PyCharm (View > Tool Windows > Terminal)
   - Navigate to the backend directory:
     ```
     cd backend
     ```
   - Install the project in development mode:
     ```
     pip install -e .
     ```
   - Install the required dependencies:
     ```
     pip install -r requirements.txt
     ```

### Setting Up pytest in PyCharm

1. **Configure pytest as the default test runner**
   - Go to File > Settings (or PyCharm > Preferences on macOS)
   - Navigate to Tools > Python Integrated Tools
   - In the "Testing" section, select "pytest" as the default test runner
   - Click "OK" to save the settings

2. **Create a pytest Run Configuration**
   - Go to Run > Edit Configurations...
   - Click the "+" button and select "pytest"
   - Name the configuration (e.g., "pytest for ranked-choice")
   - Set the following configuration:
     - Target: Script path
     - Script path: `/home/mike/bin/ranked-choice/backend`
     - Working directory: `/home/mike/bin/ranked-choice/backend`
     - Python interpreter: Select your project interpreter
   - In the "Environment variables" section, click the "..." button and add:
     - DJANGO_SETTINGS_MODULE=ranked_choice.settings
     - PYTHONPATH=/home/mike/bin/ranked-choice/backend
   - Click "OK" to save the configuration
3. Make sure Django isn't taking priority
   - Go to File > Settings
   - Navigate to Language & Frameworks > Django
   - Check the box that says `Do not use Django Test runner`

### Running Tests with pytest

#### Using the pytest Run Configuration

1. **Run all tests**
   - Select the pytest run configuration from the dropdown in the top-right corner
   - Click the green "Run" button (or press Shift+F10)

2. **Run tests with specific markers**
   - Edit the pytest run configuration
   - In the "Additional Arguments" field, add `-m marker_name` (e.g., `-m integration`)
   - Run the configuration

#### Running Individual Tests

1. **Running a specific test file**
   - Open the test file you want to run
   - Right-click anywhere in the file
   - Select "Run 'pytest in test_file.py'"

2. **Running a specific test method**
   - Open the test file
   - Navigate to the test method you want to run
   - Right-click on the method name
   - Select "Run 'pytest: test_method'"

### Debugging Tests

1. **Debug a test**
   - Set breakpoints in your code by clicking in the gutter next to the line numbers
   - Right-click on the test file or method
   - Select "Debug 'pytest in test_file.py'" or "Debug 'pytest: test_method'"
   - When the execution reaches a breakpoint, PyCharm will pause and show the debug window

2. **Using the Debug Console**
   - When paused at a breakpoint, use the Debug Console to inspect variables
   - Type variable names to see their values
   - Execute code to test behavior

### Troubleshooting

- **Missing dependencies**: If you encounter errors about missing dependencies, make sure you've installed all requirements:
  ```
  pip install -r requirements.txt
  ```

- **Path issues**: If PyCharm can't find modules, make sure the project is installed in development mode:
  ```
  pip install -e .
  ```

- **Django settings not found**: Make sure the DJANGO_SETTINGS_MODULE environment variable is set correctly in your run configuration.

- **Database configuration**: The tests now use SQLite in-memory database by default, configured in conftest.py. No need to have PostgreSQL running for tests.

- **Import path issues**: If you encounter errors like "Model class doesn't declare an explicit app_label and isn't in an application in INSTALLED_APPS", check your import statements. Make sure you're using the correct import paths without the "backend." prefix. For example, use `from ranked_choice.core.models import Ballot` instead of `from backend.ranked_choice.core.models import Ballot`.

## Test Structure

The tests are organized as follows:

- `ranked_choice/core/tests/`: Unit and integration tests for the core module
- `ranked_choice/api/tests/`: Tests for the API endpoints

## Notes

- The tests use an SQLite in-memory database for integration testing
- The test database is automatically created and destroyed by the test runner
- Configuration for pytest is in `pytest.ini` and `conftest.py`
