# 🤟 Sign Language Translator & Learning Platform

Welcome! This is a beginner-friendly application that helps you translate and learn American Sign Language (ASL) using your webcam.

## 🎯 What Does This Do?

This application has **three main features**:

1. **Real-Time Translator** 📹 - Point your webcam at your hands, and the app recognizes ASL signs in real-time
2. **Learning Hub** 📚 - Browse through 250+ ASL signs with detailed information
3. **Text-to-Speech** 🔊 - Listen to the meaning of signs when you translate them

**Think of it like Google Translate, but for sign language using your camera!**

---

## ⚡ Quick Start (Easiest Way)

### Windows Users:
1. Open the folder where this project is located
2. Double-click **run.bat**
3. Wait for it to start (you'll see "Running on http://localhost:5000" in the terminal)
4. Your browser will open automatically to http://localhost:5000

### Mac/Linux Users:
1. Open Terminal in this folder
2. Run this command:
   ```bash
   chmod +x run.sh
   ./run.sh
   ```
3. Open your browser and go to http://localhost:5000

That's it! You're ready to use the app.

---

## 🔧 Manual Setup (If the Quick Start Doesn't Work)

### Step 1: Install Python (If You Don't Have It)
- Download Python from https://www.python.org/downloads/
- During installation, **check the box** that says "Add Python to PATH"

### Step 2: Open Command Prompt/Terminal
- **Windows**: Press `Win + R`, type `cmd`, and press Enter
- **Mac/Linux**: Open the "Terminal" app

### Step 3: Navigate to Your Project Folder
```bash
cd path/to/SLT
```

### Step 4: Create a Virtual Environment
A virtual environment keeps your project's packages separate from your computer's other projects.

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

After this, you should see `(venv)` at the start of your command line.

### Step 5: Install Required Packages
```bash
pip install -r requirements.txt
```

This downloads and installs all the tools the app needs. It might take 5-10 minutes.

### Step 6: Start the Application
```bash
python app.py
```

### Step 7: Open Your Browser
- Type this in your browser address bar: **http://localhost:5000**
- You'll see the home page with three options

---

## 📖 How to Use the App

### 🏠 Home Page
- Overview of the project
- Links to the translator and learning hub

### 🎬 Translator Page
- **Click "Start Translator"** to turn on your webcam
- **Hold up your hands** in front of the camera to make ASL signs
- **The app will display** what sign it detected and its meaning
- **Click "Stop"** when you're done
- **Enable "Text to Speech"** to hear the meaning out loud

**Tips for best results:**
- Use good lighting (natural light is best)
- Frame your hands and body in the camera
- Hold the sign for about 2-3 seconds
- Keep your hands clear and visible

### 📚 Learning Hub
- Browse all 250+ ASL signs available
- **Search** for specific signs by typing in the search box
- **Click on a sign** to see more details
- Use **Ctrl+K** to quickly focus the search box

---

## 📁 What's in This Folder? (Understanding the Structure)

```
SLT/
├── app.py                    ← This runs the web application
├── requirements.txt          ← List of packages needed
├── models/
│   └── FINAL_ASL_250.h5     ← The AI model (trained to recognize signs)
├── src/
│   ├── backbone.py          ← AI model code
│   ├── landmarks_extraction.py  ← Code to detect hands/body
│   └── sign_to_prediction_index_map.json  ← 250 sign names
├── templates/               ← This folder has the web pages
│   ├── index.html           ← Home page
│   ├── translator.html      ← Translator page
│   └── learn.html           ← Learning page
└── static/                  ← Styling and design files
    ├── css/style.css
    └── js/app.js
```

---

## ⚙️ What Software Does This Need?

The `requirements.txt` file lists everything:

- **Flask** - Makes the web page work
- **OpenCV** - Reads your webcam
- **MediaPipe** - Detects hands and body poses
- **TensorFlow** - The AI engine that recognizes signs
- **NumPy** - Helps process data

Don't worry about understanding these—just run `pip install -r requirements.txt` and you're good!

---

## 🐛 Troubleshooting (When Things Go Wrong)

### "Port 5000 is already in use"
**This means another app is using port 5000.**
- Close any other Flask apps you might have running
- Or edit `app.py` and change line with `port=5000` to `port=5001`

### "Camera not working"
- Check that you allowed the browser to access your camera
- Try a different browser
- Make sure no other app is using your webcam

### "Module not found" error
- Make sure you activated your virtual environment (you should see `(venv)` in your terminal)
- Run: `pip install -r requirements.txt` again

### "Python command not found"
- Reinstall Python and **check "Add Python to PATH"** during installation
- Or use `python3` instead of `python`

---

## 🚀 Next Steps

After you get the app running:
1. **Try the translator** - Perform some ASL signs and see if it recognizes them
2. **Check the learning hub** - Browse signs to understand ASL better
3. **Explore the code** - Open `app.py` and `src/` folder to see how it works

---

## ❓ Common Questions

**Q: Do I need to be fluent in sign language?**
A: No! This app is for learning. Try making signs from the Learning Hub.

**Q: Can I use this on my phone?**
A: The app works best on a computer with a webcam. Mobile support is limited.

**Q: Where does the AI model come from?**
A: It's pre-trained on thousands of ASL signs. The model file is in `models/FINAL_ASL_250.h5`

**Q: Can I add my own signs?**
A: Advanced users can retrain the model, but that requires Python knowledge.

---

## 📚 Learn More

- **About ASL**: https://www.lifeprint.com/ (great ASL learning resource)
- **About Flask**: https://flask.palletsprojects.com/
- **About TensorFlow**: https://www.tensorflow.org/

---

## 🎓 Project Info

- **Built with**: Python, Flask, TensorFlow, OpenCV, MediaPipe
- **Supports**: 250 American Sign Language (ASL) signs
- **Requires**: Python 3.8+ and webcam

---

**Enjoy learning sign language! 🤟**