import cv2
import numpy as np
import base64

def generate_interactive_outlined_image(input_image_path, output_html_path):
    # Load image, convert to grayscale, Otsu's threshold
    image = cv2.imread(input_image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Find number of rows
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 1))
    horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
    cnts = cv2.findContours(horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    rows = 0
    outline_image = np.ones_like(thresh) * 255  # Create a white image to draw outlines
    for c in cnts:
        cv2.drawContours(outline_image, [c], -1, (0, 0, 0), 2)
        rows += 1

    # Find number of columns
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 25))
    vertical = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
    cnts = cv2.findContours(vertical, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    columns = 0
    for c in cnts:
        cv2.drawContours(outline_image, [c], -1, (0, 0, 0), 2)
        columns += 1

    # Convert the NumPy array to bytes
    _, buffer = cv2.imencode('.png', outline_image)
    outline_image_base64 = base64.b64encode(buffer).decode('utf-8')

    # Create HTML content with centering CSS and JavaScript for movement
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Outlined Image</title>
        <style>
            body {{
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }}
            canvas {{
                outline: 2px solid black;  /* Remove the black border around the canvas */
            }}
            #toggleButton {{
                position: absolute;
                bottom: 100px;
                right: -800px;
            }}
        </style>
    </head>
    <body>
        <canvas id="imageCanvas" width="{outline_image.shape[1]}" height="{outline_image.shape[0]}"></canvas>
        <button id="toggleButton">Toggle Drag and Drop</button>

        <script>
            var canvas = document.getElementById('imageCanvas');
            var ctx = canvas.getContext('2d');
            var image = new Image();
            image.src = 'data:image/png;base64,{outline_image_base64}';
            var xPos = 0;
            var yPos = 0;
            var grid = 1; // Set the grid size to 5
            var isDragging = false;

            function drawImage() {{
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                ctx.drawImage(image, xPos, yPos);
            }}

            function handleArrowKeys(e) {{
                if (isDragging) {{
                    switch (e.key) {{
                        case 'ArrowUp':
                            yPos -= grid;
                            break;
                        case 'ArrowDown':
                            yPos += grid;
                            break;
                        case 'ArrowLeft':
                            xPos -= grid;
                            break;
                        case 'ArrowRight':
                            xPos += grid;
                            break;
                    }}
                    drawImage();
                }}
            }}

            function toggleDragging() {{
                isDragging = !isDragging;
                document.getElementById('toggleButton').innerText = isDragging ? 'Disable Drag and Drop' : 'Enable Drag and Drop';
            }}

            image.onload = drawImage;
            window.addEventListener('keydown', handleArrowKeys);
            document.getElementById('toggleButton').addEventListener('click', toggleDragging);
        </script>
    </body>
    </html>
    """

    # Save HTML content to a file
    with open(output_html_path, 'w') as html_file:
        html_file.write(html_content)

