# Database Tests

This directory contains tests for the database implementation of the video generation project.

## Running the Tests

To run the tests, you need to have pytest installed:

```bash
pip install pytest
```

Then, from the backend directory, run:

```bash
pytest
```

This will run all the tests in the `tests` directory.

## Running Specific Tests

You can run specific tests by specifying the test file or test function:

```bash
# Run a specific test file
pytest tests/test_database.py

# Run a specific test function
pytest tests/test_database.py::test_project_create

# Run tests matching a pattern
pytest -k "project"  # Runs all tests with "project" in the name
```

## Test Structure

The tests are organized as follows:

- `test_database.py`: Tests for the database implementation, including:
  - Project CRUD operations
  - Asset CRUD operations
  - File storage operations

## Test Database

The tests use a temporary SQLite database that is created and destroyed for each test run. This ensures that the tests don't interfere with your development database.

## Test Coverage

You can measure test coverage to see how much of your code is being tested:

```bash
pip install pytest-cov
pytest --cov=backend
```

This will show you the percentage of your code that is covered by tests.

The tests cover the following functionality:

- Creating, retrieving, updating, and deleting projects
- Creating, retrieving, updating, and deleting assets
- Saving and loading files
- JSON serialization and deserialization
- Metadata handling
- File storage operations

## Adding New Tests

To add new tests, simply add new test functions to the existing test file or create a new test file in the `tests` directory. Test functions should start with `test_` and test files should start with `test_`.

For example:

```python
def test_my_new_feature():
    # Test code here
    assert True
```
