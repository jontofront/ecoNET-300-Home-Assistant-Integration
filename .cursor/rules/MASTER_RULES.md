# 🚨 MASTER RULES - ALWAYS CHECK FIRST

## MANDATORY Before Any Code Changes

### 1. ALWAYS READ THESE RULES FIRST

- `.cursor/rules/home-assistant-standards.mdc` - HA integration standards
- `.cursor/rules/econet300-specific.mdc` - Device-specific guidelines
- `.cursor/rules/python-standards.mdc` - Python coding standards
- `.cursor/rules/translation-requirements.mdc` - Translation requirements
- `.cursor/rules/code-style-ruff.mdc` - **Code formatting with Ruff** 🚨
- `.cursor/rules/api-endpoint-validation.mdc` - **API response validation** 🚨

### 2. ALWAYS FOLLOW HA DOCUMENTATION

- Reference: <https://developers.home-assistant.io/docs/development_index>
- Use proper entity lifecycle patterns
- Follow HA integration development guidelines

### 3. ALWAYS CHECK TRANSLATIONS

- Update `strings.json`, `en.json`, and `pl.json` for new entities
- Use camel_to_snake format for translation keys
- Test translations after changes

### 4. ALWAYS VALIDATE API ENDPOINTS

- **ALWAYS check test fixtures** in `tests/fixtures/` before documenting
- **Verify entity types** against actual JSON responses
- **Use fixture data** as source of truth for API behavior
- **Never document without checking** actual response examples

### 5. ALWAYS USE PROPER PATTERNS

- Use proper error handling
- Test your changes
- Use Ruff for code formatting and linting

### 6. 🚨 CRITICAL CODE STYLE RULES

- **ALWAYS use Ruff** for formatting and linting
- **NEVER use Black, isort, or flake8**
- **ALWAYS sort imports alphabetically** within groups
- **NEVER have whitespace in blank lines** (W293 rule)
- **ALWAYS run `ruff check .` before committing**

### 7. ALWAYS CHECK BEFORE COMMITTING

- Run `ruff check .` to catch style issues
- Run `ruff format .` to auto-format code
- Ensure no import sorting issues
- Ensure no blank line whitespace issues
- **Validate API documentation** against test fixtures
- Test your changes work as expected
