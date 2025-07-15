# ecoNET24 Cloud Translation Files

## Overview
This directory contains documentation and saved translation files from the ecoNET24.com cloud service. These files provide official translations used by the ecoNET system.

## Translation File Sources

### JavaScript Translation Files
All translation files are located at: `https://www.econet24.com/static/ui/`

| File | Description | Cache Buster |
|------|-------------|--------------|
| `econet_basicset.js` | Basic language setup and functions | `?f9fb2c1f` |
| `econet_transt.js` | Main translation system (19 languages) | `?8c71c880` |
| `econet_transp1.js` | Translation part 1 | `?ae7cdce1` |
| `econet_transp2.js` | Translation part 2 | `?94994b86` |
| `econet_transp3.js` | Translation part 3 | `?2224d6f0` |
| `econet_transp4.js` | Translation part 4 | `?93f9fa7e` |

### Direct URLs
```
https://www.econet24.com/static/ui/econet_basicset.js?f9fb2c1f
https://www.econet24.com/static/ui/econet_transt.js?8c71c880
https://www.econet24.com/static/ui/econet_transp1.js?ae7cdce1
https://www.econet24.com/static/ui/econet_transp2.js?94994b86
https://www.econet24.com/static/ui/econet_transp3.js?2224d6f0
https://www.econet24.com/static/ui/econet_transp4.js?93f9fa7e
```

## Supported Languages

### Focus Languages (EN, PL, LT)
- **`en`** - English
- **`pl`** - Polish  
- **`lt`** - Lithuanian

### All Supported Languages (19 total)
```javascript
["pl","en","de","fr","uk","da","cz","it","ro","bg","tr","es","hr","hu","sk","sr","lv","nl","ru"]
```

## File Structure

### Translation System Architecture
1. **`econet_basicset.js`** - Language detection and basic setup
2. **`econet_transt.js`** - Core translation functions and language definitions
3. **`econet_transp1-4.js`** - Actual translation data split across 4 files

### Translation Data Format
The translation files contain JavaScript objects with:
- **Language codes** as keys
- **Translation keys** for UI elements
- **Entity names** and descriptions
- **State descriptions** and messages
- **Error messages** and notifications

## How to Access

### Method 1: Browser Developer Tools
1. Open econet24.com in browser
2. Open Developer Tools (F12)
3. Go to Network tab
4. Filter by "js" files
5. Look for the translation files listed above

### Method 2: Direct Download
```bash
# Download all translation files
curl -O "https://www.econet24.com/static/ui/econet_basicset.js?f9fb2c1f"
curl -O "https://www.econet24.com/static/ui/econet_transt.js?8c71c880"
curl -O "https://www.econet24.com/static/ui/econet_transp1.js?ae7cdce1"
curl -O "https://www.econet24.com/static/ui/econet_transp2.js?94994b86"
curl -O "https://www.econet24.com/static/ui/econet_transp3.js?2224d6f0"
curl -O "https://www.econet24.com/static/ui/econet_transp4.js?93f9fa7e"
```

### Method 3: Python Script
Use the provided download script:
```bash
python scripts/download_cloud_translations.py
```

## Usage in Local Integration

### Benefits
- ✅ **Official terminology** - Uses exact terms from ecoNET
- ✅ **Complete coverage** - All available translations
- ✅ **Multi-language support** - 19 languages available
- ✅ **Consistent naming** - Standardized across devices
- ✅ **Regular updates** - Maintained by ecoNET

### Integration Steps
1. **Download** translation files from cloud
2. **Extract** relevant translations (EN, PL, LT)
3. **Convert** to Home Assistant format
4. **Update** local translation files
5. **Test** in Home Assistant environment

## File Organization

```
docs/cloud_translations/
├── README.md                    # This file
├── js_files/                    # Downloaded JS translation files
│   ├── econet_basicset.js
│   ├── econet_transt.js
│   ├── econet_transp1.js
│   ├── econet_transp2.js
│   ├── econet_transp3.js
│   └── econet_transp4.js
├── extracted/                   # Extracted translation data
│   ├── en.json                 # English translations
│   ├── pl.json                 # Polish translations
│   └── lt.json                 # Lithuanian translations
└── comparison/                 # Comparison with local translations
    ├── missing_translations.md
    └── translation_gaps.md
```

## Notes

### Cache Busters
- The `?` parameters in URLs are cache busters
- They may change when files are updated
- Always check for latest versions

### File Updates
- Translation files are updated by ecoNET
- Check periodically for new versions
- Update local copies when new versions are available

### Legal Considerations
- These are publicly accessible files
- Used for reference and improvement of local integration
- Respect ecoNET's terms of service
- Do not redistribute without permission

---

**Last Updated**: 2025-01-09
**Source**: econet24.com
**Integration Version**: v1.1.1 