# 🔍 Developer Tools Guide: Finding API Parameters

This guide shows you how to use browser developer tools to find the exact API parameter names from econet24.com that you need for requesting new sensor features.

## 📱 What You'll Learn

- How to open browser developer tools
- How to monitor API calls to your ecoNET device
- How to identify parameter keys from API responses
- How to use this information in feature requests

## 🛠️ Step-by-Step Instructions

### Step 1: Open Developer Tools

1. **Open econet24.com** in your web browser
2. **Press `F12`** on your keyboard, OR
3. **Right-click anywhere** on the page → Select "Inspect Element"
4. **Click on the "Network" tab** in the developer tools panel

![Developer Tools Network Tab](https://via.placeholder.com/800x400/2ecc71/ffffff?text=Network+Tab+Open)

### Step 2: Monitor API Calls

1. **Keep the Network tab open**
2. **Refresh the page** (F5) or navigate to different sections
3. **Look for requests** to your device's IP address (e.g., `192.168.1.100`)
4. **Filter by "Fetch/XHR"** to see only API calls

### Step 3: Find Parameter Keys

1. **Click on any API request** to your device in the Network tab
2. **Click the "Response" tab** to see the JSON data
3. **Look for parameter names** like `tempCO`, `statusPump`, etc.
4. **The parameter name is the key** (left side of the colon in JSON)

## 📊 Example: Finding the Boiler Temperature Parameter

### Visual Example

The image below shows how to inspect the "Boiler temperature" tile:

![Parameter Inspection Example](https://via.placeholder.com/800x400/3498db/ffffff?text=Boiler+Temperature+Inspection)

### What to Look For

1. **In the web interface**: Find the "Boiler temperature" tile
2. **In developer tools**: Look for the `onclick` attribute with `popupParam('tempCO','')`
3. **The parameter key**: `tempCO` is what you need for your feature request

### JSON Response Example

```json
{
  "tempCO": 19.6,        ← "tempCO" is the parameter key
  "tempCOSet": 43,       ← "tempCOSet" is the parameter key
  "statusPump": true,    ← "statusPump" is the parameter key
  "fuelLevel": 85        ← "fuelLevel" is the parameter key
}
```

## 🔧 Alternative Method: Use the Test Script

If you prefer not to use browser developer tools, you can use our test script:

```bash
python scripts/test_api_endpoints.py
```

This will show you all available parameters from your device automatically.

## 📝 Using This Information

Once you find a parameter key (like `tempCO`):

1. **Copy the exact parameter name** (case-sensitive)
2. **Use it in your feature request** in the "API Parameter Name" field
3. **Include a screenshot** of where you found it in econet24.com
4. **Reference this guide** if you need help

## 🆘 Troubleshooting

### Common Issues

- **No API calls visible**: Make sure you're on the Network tab and refresh the page
- **Can't find your device IP**: Check your device's network settings
- **Parameter not visible**: Try navigating to different sections of econet24.com

### Need Help?

- Check the [API Documentation](API_V1_DOCUMENTATION.md)
- Use the [test script](../scripts/test_api_endpoints.py)
- Open an issue with your findings

## 📚 Related Documentation

- [API V1 Documentation](API_V1_DOCUMENTATION.md)
- [Cloud Translations Reference](../cloud_translations/MANUAL_TRANSLATION_REFERENCE.md)
- [New Sensor Feature Request Template](../../.github/ISSUE_TEMPLATE/new_sensor_feature.yml)

---

*This guide helps you find the exact parameter names needed for requesting new sensor features. Always verify the parameter exists before submitting a feature request.*
