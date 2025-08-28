# Home Assistant Development Guidelines

*Based on: https://developers.home-assistant.io/docs/development_guidelines*

## Style Guidelines

Home Assistant enforces quite strict **PEP8** style and **PEP 257** (Docstring Conventions) compliance on all code submitted.

We use **Ruff** for code formatting. Every pull request is automatically checked as part of the linting process and we never merge submissions that diverge.

### Summary of Most Relevant Points

- **Comments** should be full sentences and end with a period
- **Imports** should be ordered
- **Constants** and the content of lists and dictionaries should be in alphabetical order

It is advisable to adjust IDE or editor settings to match those requirements.

## Our Recommendations

For some cases PEPs don't make a statement. This section covers our recommendations about the code style. Those points were collected from the existing code and based on what contributors and developers were using the most. This is basically a majority decision, thus you may not agree with it. But we would like to encourage you follow those recommendations to keep the code consistent.

### File Headers

The docstring in the file header should describe what the file is about.

```python
"""Support for MQTT lights."""
```

### Log Messages

There is **no need to add the platform or component name** to the log messages. This will be added automatically. Like `syslog` messages there **shouldn't be any period at the end**. A widely used style is shown below but you are free to compose the messages as you like.

```python
_LOGGER.error("No route to device: %s", self._resource)
```

Example output:
```
2017-05-01 14:28:07 ERROR [homeassistant.components.sensor.arest] No route to device: 192.168.0.18
```

**Important**: Do not print out API keys, tokens, usernames or passwords (even if they are wrong). Be restrictive with `_LOGGER.info`, use `_LOGGER.debug` for anything which is not targeting the user.

### Use New Style String Formatting

**Prefer f-strings** over `%` or `str.format()`.

```python
# New - CORRECT
f"{some_value} {some_other_value}"

# Old - WRONG
"{} {}".format("New", "style")
"%s %s" % ("Old", "style")
```

**Exception**: Use percentage formatting for logging to avoid formatting the log message when it is suppressed.

```python
_LOGGER.info("Can't connect to the webservice %s at %s", string1, string2)
```

### Typing

We encourage the use of **fully typing your code**. This helps with finding/preventing issues and bugs in our codebase, but also helps fellow contributors making adjustments to your code in the future as well.

By default, Home Assistant will statically check for type hints in our automated CI process. Python modules can be included for strict checking, if they are fully typed, by adding an entry to the `.strict-typing` file in the root of the Home Assistant Core project.

## Implementation for ecoNET-300 Integration

### Code Quality Requirements
- All code must pass **Ruff linting** and formatting
- All code must pass **type checking (mypy)**
- All tests must pass
- Code must be properly formatted
- Follow Home Assistant integration patterns
- Maintain backward compatibility
- Document all public APIs

### Testing Requirements
- All code must have proper test coverage
- Use **pytest** for testing
- Follow Home Assistant testing patterns
- Mock external dependencies

### Integration Standards
- Follow Home Assistant integration architecture
- Use proper entity descriptions
- Implement proper error handling
- Follow async/await patterns correctly

### Common Mistakes to Avoid
- ❌ Don't use old-style string formatting (`%` or `.format()`)
- ❌ Don't add periods to log messages
- ❌ Don't log sensitive information (API keys, tokens, etc.)
- ❌ Don't skip type hints
- ❌ Don't ignore linting errors
- ❌ Don't use f-strings in logging (use percentage formatting)

### Pre-commit Configuration
The project uses a simplified pre-commit configuration with:
- **Ruff** for code formatting and linting
- **Codespell** for spelling checks
- **MyPy** for type checking
