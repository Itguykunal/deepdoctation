# DeepDoctation 🧠📄  
Transform images into structured, editable HTML using Deep Learning and OCR.

## 🚀 Features
- Detects elements like logos, barcodes, color bars, and text.
- Converts scanned documents into HTML with proper formatting.
- Auto-generates tables for data entry usability.
- Built with Flask, YOLOv5, OCR, and Computer Vision.

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

- Place your trained `best.pt` file in the `static/` directory inside the `yolov5` folder.

- In `Images.py`, update the model path:
```python
model = torch.hub.load('ultralytics/yolov5', 'custom', 'Replace with Full Path of best.pt (e.g., yolov5/static/best.pt)')
```

---

## ▶️ Run the Application
```bash
python App.py
```

Open your browser and visit:  
[http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

## 📂 Tech Stack
- Python, Flask
- OpenCV, PyTesseract
- YOLOv5 (Torch + Computer Vision)
- HTML5, CSS3, JavaScript
- jQuery, Pandas

---

## 💡 Author
**Kunal Krishna**
