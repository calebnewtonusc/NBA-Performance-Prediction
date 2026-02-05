# Contributing to NBA Performance Prediction

Thanks for contributing! This is a collaborative learning project.

## Getting Started

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `source venv/bin/activate` (or `venv\Scripts\activate` on Windows)
4. Install dependencies: `pip install -r requirements.txt`

## Claiming a Task

1. Check the [PROJECT_PLAN.md](docs/PROJECT_PLAN.md)
2. Find an unclaimed milestone
3. Put your name next to "Team Member Assignment"
4. Create a branch: `git checkout -b milestone-X.X-yourname`
5. Push your claim: `git add . && git commit -m "Claiming milestone X.X" && git push`

## Development Workflow

1. **Create a branch** for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** and commit frequently:
   ```bash
   git add .
   git commit -m "Descriptive commit message"
   ```

3. **Write tests** for your code:
   ```bash
   pytest tests/
   ```

4. **Format your code** before committing:
   ```bash
   black src/
   flake8 src/
   ```

5. **Push your branch**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request** on GitHub

## Code Style

- Follow PEP 8 guidelines
- Use `black` for formatting
- Add docstrings to all functions and classes
- Write descriptive variable names
- Keep functions focused and small

## Testing

- Write tests for all new functions
- Aim for >80% code coverage
- Run tests before submitting PR: `pytest tests/`

## Pull Request Guidelines

- Give your PR a clear title
- Describe what you changed and why
- Reference any related issues
- Make sure all tests pass
- Request review from at least one team member

## Questions?

- Create a GitHub Issue for technical questions
- Use Discussions for general questions
- Reach out to the team on your communication channel

## Code Review

- Be respectful and constructive
- Explain your suggestions
- Approve when everything looks good
- The PR author merges after approval

Happy coding!
