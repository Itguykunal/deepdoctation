import os
from flask import Flask, render_template, request, send_file
from Images import perform_object_detection  # Import the function from Images
from Ocr import process_image  # Import the function from Ocr
from Layout import generate_interactive_outlined_image

app = Flask(__name__, static_folder='uploads', template_folder='templates')

# Set the directory for uploading images
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def generate_combined_result(image_path):
    # Perform object detection
    object_detection_result = perform_object_detection(image_path)  # Use the function from Images

    # Perform OCR
    ocr_result = process_image(image_path)  # Use the function from Ocr

    # Generate the interactive outlined image
    output_html_path = os.path.join(app.config['UPLOAD_FOLDER'], 'outlined_image.html')
    generate_interactive_outlined_image(image_path, output_html_path)

    # Read the content of the generated outlined image HTML
    with open(output_html_path, 'r') as html_file:
        outlined_image_content = html_file.read()

    # Combine the results into a single HTML
    combined_result = f"""
    <html>
    <body>
    {object_detection_result}
    {ocr_result}
    {outlined_image_content}
    </body>
    </html>
    """

    # Save the combined result to a file (optional)
    with open("combined_result.html", "w") as file:
        file.write(combined_result)

    return combined_result

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "image" in request.files:
            image = request.files["image"]

            if image.filename != "":
                # Create the "uploads" directory if it doesn't exist
                if not os.path.exists(app.config['UPLOAD_FOLDER']):
                    os.makedirs(app.config['UPLOAD_FOLDER'])

                image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
                image.save(image_path)

                combined_result = generate_combined_result(image_path)

                return render_template("result.html", result_html=combined_result, image_path=image_path)

        elif 'file' in request.files:
            file = request.files['file']

            if file.filename != '':
                # Save the uploaded file
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(file_path)

                combined_result = generate_combined_result(file_path)

                return render_template("result.html", result_html=combined_result, image_path=file_path)

    return render_template("index.html")

@app.route("/download/<path:image_path>")
def download(image_path):
    return send_file("combined_result.html", as_attachment=True, download_name="combined_result.html")

if __name__ == "__main__":
    app.run(debug=True)
