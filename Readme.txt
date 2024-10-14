1. Install Python Packages:
pip install Flask opencv-python pytesseract numpy pillow torch pandas

2. Install YOLOv5:
git clone https://github.com/ultralytics/yolov5.git
cd yolov5
pip install -U -r requirements.txt
Save the best.pt file in the static directory inside the yolov5 folder
Open Images.py —

model = torch.hub.load('ultralytics/yolov5', 'custom', ‘Replace with Full Path of best.pt/yolov5/static/best.pt')

3. Run the Application:
python App.py
http://127.0.0.1:5000/