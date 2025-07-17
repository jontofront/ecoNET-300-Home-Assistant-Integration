# 🚨 MASTER RULES - ALWAYS CHECK FIRST

## MANDATORY: Before Any Code Changes

### 1. ALWAYS READ THESE RULES FIRST:
- `.cursor/rules/home-assistant-standards.mdc` - HA integration standards
- `.cursor/rules/econet300-specific.mdc` - Device-specific guidelines  
- `.cursor/rules/python-standards.mdc` - Python coding standards
- `.cursor/rules/translation-requirements.mdc` - Translation requirements

### 2. ALWAYS FOLLOW HA DOCUMENTATION:
- Reference: https://developers.home-assistant.io/docs/development_index
- Use proper entity lifecycle patterns
- Follow HA integration development guidelines

### 3. ALWAYS CHECK TRANSLATIONS:
- Update `strings.json`, `en.json`, and `pl.json` for new entities
- Use camel_to_snake format for translation keys
- Test translations after changes

### 4. ALWAYS USE PROPER PATTERNS:
- Follow existing codebase patterns
- Use type hints and proper error handling
- Implement async/await for I/O operations

## ❌ NEVER:
- Make changes without reading rules first
- Ignore HA documentation standards
- Skip translation updates for new entities
- Use blocking operations in async functions
- Hardcode values (use constants)

## ✅ ALWAYS:
- Read rules before coding
- Follow HA standards
- Update translations
- Use proper error handling
- Test your changes 