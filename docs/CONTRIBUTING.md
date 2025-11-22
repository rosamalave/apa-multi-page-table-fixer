# Contributing Guidelines

Thank you for your interest in contributing to PDF Table Title Fixer!

## Code Style

### Python Standards

- Follow **PEP 8** style guide
- Use **snake_case** for variables, functions, and modules
- Maximum line length: **79 characters**
- Use **type hints** for function parameters and return values

### Docstrings

- Use triple double quotes: `"""Docstring"""`
- Write in **English with simple words**
- Use imperative mood: "Returns the object X" not "Return the object X"
- Follow PEP 257 conventions

### Commits

- Use **semantic commit format**: `<type>[scope]: <description>`
- Include both **English and Spanish** in commit messages:
  ```
  feat[gui]: Add file selector component / Agregar componente selector de archivos
  ```
- Keep commit titles under 50 characters
- Use present imperative: "Add", "Fix", "Refactor"

## Development Setup

1. **Fork the repository**

2. **Clone your fork**:
   ```bash
   git clone https://github.com/your-username/pdf-table-title-fixer.git
   cd pdf-table-title-fixer
   ```

3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements-dev.txt
   ```

5. **Run tests**:
   ```bash
   pytest
   ```

## Adding New Features

### Adding a New APA Rule

1. Create a new file in `src/rules/` or `src/rules/future_rules/`
2. Inherit from `BaseRule`
3. Implement required methods
4. Add tests in `tests/`
5. Update documentation

### Adding GUI Components

1. Create component in `src/gui/components/`
2. Follow Fluent Design theme guidelines
3. Use CustomTkinter widgets
4. Add to main window if needed

## Testing

- Write tests for all new features
- Aim for high code coverage
- Run tests before submitting PR:
  ```bash
  pytest --cov=src tests/
  ```

## Pull Request Process

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**:
   - Write code following style guidelines
   - Add tests
   - Update documentation

3. **Commit your changes**:
   ```bash
   git commit -m "feat[scope]: Description / Descripción"
   ```

4. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create a Pull Request**:
   - Describe your changes clearly
   - Reference any related issues
   - Ensure all tests pass

## Code Review

- All PRs require review before merging
- Address review comments promptly
- Keep PRs focused and reasonably sized

## Questions?

Feel free to open an issue for questions or discussions!

