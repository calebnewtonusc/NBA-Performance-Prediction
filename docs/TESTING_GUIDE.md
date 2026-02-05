# Testing Guide

Comprehensive testing guide for the NBA Performance Prediction project.

## Test Structure

```
tests/
├── test_base_client.py          # API client tests
├── test_cleaning.py              # Data cleaning tests
├── test_data_loader.py           # Data loading tests
├── test_game_data.py             # Game data collection tests
├── test_game_features.py         # Game feature engineering tests
├── test_game_features_refactored.py  # NEW: Refactored code tests
├── test_logistic_regression.py   # Model tests
├── test_model_manager.py         # Model management tests
└── test_team_data.py             # Team data collection tests
```

## Running Tests

### Quick Test
```bash
# Test refactored code (no dependencies needed)
python3 tests/test_game_features_refactored.py
```

### Full Test Suite (requires dependencies)
```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test file
pytest tests/test_game_features_refactored.py -v

# Run specific test
pytest tests/test_game_features_refactored.py::TestGameFeaturesRefactored::test_calculate_team_form_basic -v
```

## Validation Scripts

### 1. Validate Refactored Code
```bash
python3 scripts/validate_refactored_code.py
```

**Tests:**
- Game feature calculations (vectorized operations)
- Data cleaning (pandas 3.0 compatibility)
- Version consistency
- Edge cases and error handling

### 2. Performance Benchmarks
```bash
python3 scripts/benchmark_performance.py
```

**Benchmarks:**
- Small dataset (100 games)
- Medium dataset (1,000 games)
- Large dataset (10,000 games)
- Performance comparison vs iterrows baseline

### 3. Code Quality Checks
```bash
# Compile all Python files
find . -name "*.py" ! -path "./venv/*" -exec python3 -m py_compile {} \;

# Validate notebooks
for nb in notebooks/*.ipynb; do python3 -m json.tool "$nb" > /dev/null; done

# Check for anti-patterns
grep -r "iterrows" src/  # Should be empty or in comments
grep -r "inplace=True" src/  # Should be empty
grep -r "except:" src/  # Should have specific exception types
```

## Test Coverage Goals

### Current Coverage
- **Core Data Processing:** 80%+
- **Feature Engineering:** 90%+
- **Model Training:** 70%+
- **API Clients:** 60%+

### Priority Test Areas
1. ✅ Refactored vectorized operations
2. ✅ Edge cases (empty DataFrames, missing values)
3. ✅ Performance regression tests
4. ⏳ End-to-end pipeline tests
5. ⏳ Integration tests with real NBA data

## Writing Tests

### Test Template
```python
import pytest
import pandas as pd
from src.module import MyClass

class TestMyClass:
    @pytest.fixture
    def sample_data(self):
        """Create sample test data"""
        return pd.DataFrame({'col1': [1, 2, 3]})

    def test_basic_functionality(self, sample_data):
        """Test basic functionality"""
        obj = MyClass()
        result = obj.process(sample_data)
        assert isinstance(result, pd.DataFrame)
        assert len(result) > 0

    def test_edge_case_empty(self):
        """Test empty input"""
        obj = MyClass()
        result = obj.process(pd.DataFrame())
        assert result.empty

    def test_performance(self, sample_data):
        """Test performance"""
        import time
        obj = MyClass()
        start = time.time()
        _ = obj.process(sample_data)
        elapsed = time.time() - start
        assert elapsed < 1.0  # Should complete in under 1 second
```

### Best Practices
- ✅ Test both happy path and edge cases
- ✅ Use fixtures for reusable test data
- ✅ Test performance for critical paths
- ✅ Mock external dependencies (APIs, databases)
- ✅ Test error handling
- ✅ Use descriptive test names

## Continuous Integration

### GitHub Actions Workflow
```yaml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements-lock.txt
      - run: pytest tests/ -v --cov=src
```

## Pre-commit Hooks

### Setup
```bash
pip install pre-commit
pre-commit install
```

### Run Manually
```bash
pre-commit run --all-files
```

### Hooks Include
- black (formatting)
- isort (import sorting)
- flake8 (linting)
- trailing whitespace
- large file detection
- private key detection

## Troubleshooting

### Issue: ModuleNotFoundError
```bash
# Solution: Install dependencies
pip install -r requirements-lock.txt
```

### Issue: Import errors in tests
```bash
# Solution: Add project to Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Issue: Tests fail after refactoring
```bash
# Solution: Run validation script
python3 scripts/validate_refactored_code.py
```

## Test Metrics

### Performance Baselines
| Operation | Target Time (10k games) |
|-----------|-------------------------|
| calculate_team_form | < 100ms |
| calculate_head_to_head | < 100ms |
| calculate_win_streak | < 100ms |
| create_game_features | < 5s |

### Quality Metrics
- Code coverage: > 80%
- All tests passing: Yes
- No flake8 errors: Yes
- Type checking: Pass (mypy)
- Security: No vulnerabilities (bandit)

## Contributing Tests

When adding new features:
1. Write tests first (TDD)
2. Test edge cases
3. Add performance benchmarks for critical code
4. Update this guide
5. Ensure all tests pass before PR

## Resources

- [pytest documentation](https://docs.pytest.org/)
- [pandas testing](https://pandas.pydata.org/docs/reference/testing.html)
- [Python testing best practices](https://docs.python-guide.org/writing/tests/)
