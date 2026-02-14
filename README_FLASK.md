# 🤟 Sign Language Translator & Learning Platform

A modern Flask web application for real-time sign language translation and interactive learning with a beautiful Neumorphism UI design.

## ✨ Features

- **Real-Time Translator**: Translate ASL signs from your webcam with live feedback
- **Learning Hub**: Browse and learn 250+ ASL signs with interactive video library
- **Text-to-Speech**: Automatic speech generation for translated text
- **Search & Filter**: Advanced search with category filtering (Animals, Emotions, Objects)
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Neumorphism UI**: Modern soft UI design with smooth animations and interactions
- **Keyboard Shortcuts**: Ctrl+K to focus search, Esc to close modals

## 🎨 Design Highlights

- **Neumorphism**: Soft shadows, rounded corners, and depth illusion
- **Clean Typography**: Modern sans-serif fonts with clear hierarchy
- **Color Palette**: 
  - Primary: Light Gray (#e8eef2)
  - Accent: Fresh Green (#4CAF50)
  - Text: Dark Gray (#2d3436)
- **Responsive Layout**: Mobile-first approach with breakpoints at 768px and 480px

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone/Navigate to the project directory**
   ```bash
   cd path/to/SLT
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # Activate on Windows
   venv\Scripts\activate
   
   # Activate on macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. **Start the Flask development server**
   ```bash
   python app.py
   ```

2. **Open your browser and navigate to**
   ```
   http://localhost:5000
   ```

3. **Explorer the app**
   - Home page with project overview
   - Translator page with camera integration
   - Learning hub with 250 ASL signs

## 📁 Project Structure

```
SLT/
├── app.py                          # Flask application main file
├── requirements.txt                # Python dependencies
├── INTERFACE.py                    # Original ML interface (legacy)
├── retrain.py                      # Model training script
├── Readme.md                       # Original README
│
├── models/
│   └── FINAL_ASL_250.h5           # Pre-trained ASL model
│
├── src/
│   ├── backbone.py                # ML model backbone
│   ├── config.py                  # Configuration settings
│   ├── landmarks_extraction.py    # MediaPipe utilities
│   ├── utils.py                   # Utility functions
│   └── sign_to_prediction_index_map.json  # Sign mapping
│
├── templates/
│   ├── base.html                  # Base template (navbar, footer)
│   ├── index.html                 # Home page
│   ├── translator.html            # Translator interface
│   └── learn.html                 # Learning hub
│
└── static/
    ├── css/
    │   └── style.css              # Neumorphism styling
    └── js/
        └── app.js                 # JavaScript functionality
```

## 📖 Pages Overview

### 🏠 Home Page (`/`)
- Project introduction and vision
- Key objectives and features
- Quick navigation to Translator and Learning Hub
- Technology stack information

### 🎬 Translator Page (`/translator`)
- Live webcam feed with sign detection
- Real-time translation output
- Text-to-Speech toggle
- FPS and detection status monitoring
- Control buttons: Start, Stop, Clear

### 📚 Learning Hub (`/learn`)
- Searchable catalog of 250 ASL signs
- Category filtering (Animals, Emotions, Objects)
- Neumorphic video card layout
- Modal details view with instructions
- Practice and Save functionality

## 🔧 Configuration

### Flask Settings
Edit `app.py` to modify:
- Debug mode
- Host and port
- Static/template folders

### Neumorphism Colors
Edit `static/css/style.css` to customize:
- Background colors (`:root --bg-primary`, `--bg-secondary`)
- Accent color (`--accent-color`)
- Shadow values (`--shadow-*`)
- Border radius (`--border-radius`)

## 🎯 Future Enhancements

1. **ML Integration**: Connect real ASL detection model
2. **User Accounts**: Save progress and custom sign lists
3. **Video Content**: Add actual ASL demonstration videos
4. **Mobile App**: React Native or Flutter version
5. **API Expansion**: RESTful API for third-party integration
6. **Multi-language**: Support for different sign languages
7. **Advanced Analytics**: Track learning progress
8. **Offline Mode**: Progressive Web App (PWA)

## 🔒 Security Features

- HTML escaping to prevent XSS
- Secure camera permissions handling
- No external API calls by default
- Client-side validation
- CORS ready for future integration

## 🌐 Browser Support

| Browser | Support |
|---------|---------|
| Chrome | ✅ Full |
| Firefox | ✅ Full |
| Safari | ✅ Full |
| Edge | ✅ Full |
| IE 11 | ❌ Not supported |

## 📱 Responsive Breakpoints

- **Desktop**: 1400px+ (Full featured)
- **Tablet**: 768px - 1399px (Adjusted grid)
- **Mobile**: Below 768px (Single column, optimized touch)

## 🎓 Learning Resources

### Getting Started with ASL
1. Start with common signs (hello, thank you, please)
2. Practice basic hand positions
3. Learn about movement and location
4. Use the translator to practice your own signs
5. Record and review your progress

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Video content integration
- Enhanced ML model integration
- Additional language support
- UI/UX improvements

## 📝 License

This project is created for educational and accessibility purposes.

## 👨‍💻 Development Notes

### Adding New Pages
1. Create a new `.html` file in `templates/`
2. Extend `base.html`
3. Add route in `app.py`
4. Add nav link in `base.html`

### Adding New Styles
- Use CSS variables from `:root`
- Follow Neumorphism principles
- Test on mobile devices
- Maintain dark mode compatibility (future)

### Testing
```bash
# Test Flask routes
python -m pytest tests/

# Manual testing checklist
- [ ] All pages load
- [ ] Navigation works
- [ ] Search functionality
- [ ] Camera permissions
- [ ] TTS functionality
- [ ] Responsive on mobile
- [ ] No console errors
```

## 🐛 Troubleshooting

### Camera not working
- Check browser permissions
- Ensure camera is connected
- Use HTTPS on production

### TTS not working
- Check browser support
- Ensure speaker volume
- Try different text inputs

### Slow performance
- Clear browser cache
- Check internet connection
- Reduce video quality

## 📞 Support

For issues or questions related to this Flask application, refer to:
- Flask Documentation: https://flask.palletsprojects.com/
- MediaPipe: https://mediapipe.dev/
- TensorFlow Lite: https://www.tensorflow.org/lite/

---

**Made with ❤️ for the Sign Language Community**

Last Updated: February 2026
