---
title: AI Hair Studio Gemini
emoji: 🎨
colorFrom: pink
colorTo: purple
sdk: gradio
sdk_version: 5.35.0
app_file: app.py
pinned: false
short_description: AI Hair Stylist powered by Gemini 2.0 Flash
license: mit
---

# 🎨 AI Hair Stylist

**Professional hair transformation and evaluation system powered by Gemini 2.0 Flash**

## ✨ Features

- 🎯 **Face Preservation**: Doesn't distort your original photo, only transforms your hair
- 🎨 **Tonal Analysis**: Skin tone-compatible color selection 
- 📱 **HD Quality**: High resolution photo processing
- 🤖 **Dual AI**: Hair transformation + suitability evaluation
- 💬 **Chat Interface**: Easy to use with natural language
- 🌍 **Multi-language**: Full English & Turkish support

## 🚀 How to Use

1. **Get API Key**: Get your free API key from [Google AI Studio](https://ai.google.dev/)
2. **Start System**: Enter your API key and click "Start System"
3. **Upload Photo**: Upload a clear photo of yourself
4. **Write Request**: Type your hair change request in chat
5. **See Result**: Your new hair style appears automatically and AI analyzes it

## 💡 Example Requests

**English:**
- "Honey blonde hair color"
- "Natural brown long hair"
- "Modern short bob cut"
- "Chocolate tone medium hair"
- "Golden blonde wavy hair"

**Turkish:**
- "Bal sarısı saç rengi"
- "Doğal kahverengi uzun saç"
- "Modern kısa bob kesimi"
- "Çikolata tonunda orta boy saç"
- "Altın sarısı dalgalı saç"

## 🌍 Language Support

- 🇺🇸 **English**: Full interface and AI responses in English
- 🇹🇷 **Turkish**: Full interface and AI responses in Turkish
- 🔄 **Switch**: Easy language switching with buttons

## 🛠️ Technology

- **AI Model**: Google Gemini 2.0 Flash Experimental
- **Image Generation**: Native multimodal generation
- **Interface**: Gradio 4.0+
- **Platform**: Hugging Face Spaces

## 📋 Requirements

```
google-genai>=1.0.0
gradio>=4.0.0
pillow>=9.0.0
numpy>=1.21.0
```

## 🔐 API Key

This app uses Google Gemini API. You can get your own API key from [ai.google.dev](https://ai.google.dev/). Your API key is stored securely and used only for AI processing.

## ⚡ Quick Start

1. Run the Spaces
2. Choose your language (🇺🇸 English / 🇹🇷 Turkish)
3. Enter your API key
4. Upload your photo  
5. Type "How would blonde hair look on me?"
6. See the result! 🎨

## 🎯 Key Benefits

- ✅ **Ultra-precise editing**: Only hair area is modified
- ✅ **Natural results**: AI analyzes skin tone for best color match
- ✅ **Professional evaluation**: Detailed analysis of suitability
- ✅ **High quality**: HD resolution preservation
- ✅ **User-friendly**: Simple chat interface
- ✅ **Multi-language**: Works in English and Turkish

## 🔧 Installation & Deployment

### **Hugging Face Spaces (Recommended)**
1. Create a new Space on Hugging Face
2. Select "Gradio" as the SDK
3. Upload all files:
   - `app.py`
   - `requirements.txt` 
   - `README.md`
4. Space will automatically deploy on port 7860

### **Local Development**
```bash
git clone <repository>
cd ai-hair-stylist
pip install -r requirements.txt
python app.py
```

**Port Management:**
- 🏠 **Local**: Automatically finds available port
- 🌐 **Spaces**: Uses standard port 7860
- 🔄 **Auto-detection**: No port conflicts
- 📱 **Auto-browser**: Opens automatically when local

### **Environment Detection**
The app automatically detects if it's running on:
- **Hugging Face Spaces**: Uses optimized settings
- **Local Environment**: Enables sharing and browser auto-open

## 📞 Support

- **Language Issues**: Use the language toggle buttons
- **API Errors**: Check your Gemini API key
- **Photo Issues**: Use clear, front-facing photos
- **Quality Issues**: Specify exact color tones in requests

---

**🎯 Made with ❤️ using Gemini 2.0 Flash**

*Transform your look with AI-powered precision!*