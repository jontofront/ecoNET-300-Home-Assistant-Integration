# ecoNET Cloud Translations

## 📁 Directory Structure

### 🆕 Clean & Organized Files
- **`clean_translations/`** - Main translation files and documentation
  - `TRANSLATIONS_REFERENCE.md` - Complete reference guide
  - `translations_en.json` - English translations (1105 parameters)
  - `translations_pl.json` - Polish translations (1101 parameters)
  - `translations_fr.json` - French translations (872 parameters)

### 📚 Legacy Files (Kept for Reference)
- **`legacy_files/`** - Original files and comprehensive datasets
  - `all_languages_translations.json` - Complete multi-language dataset
  - `robust_translations.json` - Enhanced translations with context
  - `raw_translations.json` - Original raw data
  - Various documentation files

### 🔧 Tools
- `extract_clean_translations.py` - Script to extract clean translations
- `extract_french_translations.py` - Script to extract French translations from cloud JS files
- `available_languages.txt` - List of supported languages

## 🚀 Quick Start

1. **For Home Assistant integration**: Use files in `clean_translations/`
2. **For reference**: Check `TRANSLATIONS_REFERENCE.md`
3. **For development**: Use the extraction scripts to create new language files

## 🌐 Available Languages

Currently available in clean format:
- ✅ **English (EN)** - 1105 parameters
- ✅ **Polish (PL)** - 1101 parameters
- ✅ **French (FR)** - 872 parameters (extracted from cloud)

Other languages available in legacy files:
- Czech, Russian, Croatian, Latvian, Spanish, Bulgarian, Hungarian, Italian, Romanian, Turkish, Ukrainian

## 📖 Documentation

See `clean_translations/TRANSLATIONS_REFERENCE.md` for complete usage guide and examples.
