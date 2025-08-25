#!/usr/bin/env python3
"""
Download ecoNET24 cloud translation files.
This script downloads the official translation files from econet24.com for reference.
"""

import os
import sys
import requests
from pathlib import Path
from urllib.parse import urljoin

# Base URL for ecoNET24 translation files
BASE_URL = "https://www.econet24.com/static/ui/"

# Translation files with their cache busters
TRANSLATION_FILES = {
    "econet_basicset.js": "?f9fb2c1f",
    "econet_transt.js": "?8c71c880", 
    "econet_transp1.js": "?ae7cdce1",
    "econet_transp2.js": "?94994b86",
    "econet_transp3.js": "?2224d6f0",
    "econet_transp4.js": "?93f9fa7e",
    # Controller and device setup files
    "dev_set1.js": "?332fd073",
    "dev_set2.js": "?94aabcac", 
    "dev_set3.js": "?4fc3a2c6",
    "dev_set4.js": "?8ba3d676",
    "dev_set5.js": "?20666c27"
}

# Output directory
OUTPUT_DIR = Path("docs/cloud_translations/js_files")

def download_file(url, output_path):
    """Download a file from URL to output path."""
    try:
        print(f"📥 Downloading: {url}")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Create directory if it doesn't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        print(f"✅ Saved: {output_path}")
        return True
        
    except requests.RequestException as e:
        print(f"❌ Failed to download {url}: {e}")
        return False
    except Exception as e:
        print(f"❌ Error saving {output_path}: {e}")
        return False

def download_all_translations():
    """Download all translation files from ecoNET24."""
    print("🚀 Starting download of ecoNET24 translation files...")
    print(f"📁 Output directory: {OUTPUT_DIR.absolute()}")
    
    success_count = 0
    total_count = len(TRANSLATION_FILES)
    
    for filename, cache_buster in TRANSLATION_FILES.items():
        url = urljoin(BASE_URL, filename + cache_buster)
        output_path = OUTPUT_DIR / filename
        
        if download_file(url, output_path):
            success_count += 1
    
    print(f"\n📊 Download Summary:")
    print(f"✅ Successful: {success_count}/{total_count}")
    print(f"❌ Failed: {total_count - success_count}/{total_count}")
    
    if success_count == total_count:
        print("🎉 All translation files downloaded successfully!")
        return True
    else:
        print("⚠️  Some files failed to download. Check the errors above.")
        return False

def create_download_info():
    """Create a download info file with URLs and metadata."""
    info_file = OUTPUT_DIR / "download_info.txt"
    
    info_content = f"""# ecoNET24 Translation Files Download Info

Downloaded on: {Path().cwd()}
Source: {BASE_URL}

## Files Downloaded:
"""
    
    for filename, cache_buster in TRANSLATION_FILES.items():
        url = urljoin(BASE_URL, filename + cache_buster)
        info_content += f"- {filename}: {url}\n"
    
    info_content += f"""
## Total Files: {len(TRANSLATION_FILES)}

## Usage:
These files contain the official ecoNET24 translations and can be used as reference
for improving the local Home Assistant integration translations.

## Note:
- Cache busters may change when files are updated
- Check periodically for new versions
- Respect ecoNET's terms of service
"""
    
    try:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        with open(info_file, 'w', encoding='utf-8') as f:
            f.write(info_content)
        print(f"📝 Created download info: {info_file}")
    except Exception as e:
        print(f"❌ Failed to create download info: {e}")

def main():
    """Main function."""
    print("🔍 ecoNET24 Cloud Translation Downloader")
    print("=" * 50)
    
    # Check if output directory exists
    if OUTPUT_DIR.exists():
        print(f"📁 Output directory exists: {OUTPUT_DIR}")
        response = input("Do you want to overwrite existing files? (y/N): ")
        if response.lower() != 'y':
            print("❌ Download cancelled.")
            return False
    
    # Download files
    success = download_all_translations()
    
    if success:
        # Create download info
        create_download_info()
        
        print("\n📋 Next Steps:")
        print("1. Review downloaded files in docs/cloud_translations/js_files/")
        print("2. Extract relevant translations (EN, PL, LT)")
        print("3. Convert to Home Assistant format")
        print("4. Update local translation files")
        print("5. Test in Home Assistant environment")
    
    return success

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n❌ Download cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1) 