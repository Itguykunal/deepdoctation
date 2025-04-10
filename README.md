# DeepDoctation 🧠📄  
Transform images into structured, editable HTML using Deep Learning and OCR.

---

## 📦 Project Structure

```
DeepDoctation/
├── App.py                         # Main Flask app entry point
├── Images.py                      # Handles image processing and detection
├── Layout.py                      # Generates layout structure
├── Ocr.py                         # Performs OCR using PyTesseract
├── best.pt                        # YOLOv5 trained model
├── How to use and Working...pdf   # Documentation
├── Readme.md                      # You are here
├── templates/                     # HTML templates for Flask
```

---

## 🚀 Features

- Detects elements like logos, barcodes, color bars, and text
- Converts scanned documents into HTML with proper layout
- Auto-generates tables for structured data representation
- Built with Flask, YOLOv5, OCR, and Computer Vision

---

## 🔧 Installation

### 1. Install Python Packages
```bash
pip install Flask opencv-python pytesseract numpy pillow torch pandas
```

### 2. Install YOLOv5
```bash
git clone https://github.com/ultralytics/yolov5.git
cd yolov5
pip install -U -r requirements.txt
```

- Place your `best.pt` file in the `static/` directory inside the `yolov5` folder.

- In `Images.py`, update the model load line:
```python
model = torch.hub.load('ultralytics/yolov5', 'custom', 'Full/Path/To/best.pt')
```

---

## ▶️ Run the Application
```bash
python App.py
```

Then open your browser and go to:  
[http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

## 📂 Tech Stack
- Python, Flask
- OpenCV, PyTesseract
- YOLOv5, Torch
- HTML5, CSS3, JavaScript
- jQuery, Pandas

---

## 📄 Additional Info

Refer to the included PDF:  
**"How to use and Working of DeepDoctation.pdf"**  
for a detailed walkthrough of the app's inner workings.

---

## 👨‍💻 Author

**Kunal Krishna**
