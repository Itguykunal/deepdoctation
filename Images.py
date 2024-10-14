import torch
from PIL import Image
import os
import pandas as pd

def perform_object_detection(image_path):
    # Load YOLOv5 model
    model = torch.hub.load('ultralytics/yolov5', 'custom', '/Users/kunal/Desktop/object/yolov5/static/best.pt')

    # Load the image using PIL
    img = Image.open(image_path)

    # Create an "uploads" folder if it doesn't exist
    if not os.path.exists("uploads"):
        os.mkdir("uploads")

    # Perform object detection
    results = model(img)

    # Extract the detected objects and their coordinates
    objects = results.pandas().xyxy[0]

    # Check if there are detected objects
    if objects.empty:
        return "No objects detected in the image."

    # Calculate the maximum dimensions of the objects
    max_x = objects.iloc[:, 2].max()
    max_y = objects.iloc[:, 3].max()

    # Calculate the container size based on the maximum dimensions
    container_width = max_x + 20  # Add some padding
    container_height = max_y + 20  # Add some padding

    # Create an HTML page with CSS and JavaScript for drag and drop with a grid
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        #container {{
            border: 1px solid white; /* Add a black border around the container */
            width: {container_width}px; /* Set the container width based on the maximum dimensions */
            height: {container_height}px; /* Set the container height based on the maximum dimensions */
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
        }}

        #text-box {{
            position: relative;
            width: 100%;
            height: 100%;
        }}

        .object {{
            position: absolute;
        }}

        .object.selected {{
            border: 2px dashed black; /* Change the border on hover */
        }}

        .delete-button {{
            background-color: black;
            color: white;
            border: 2px dashed black;
            padding: 5px 10px;
            cursor: pointer;
            position: absolute;
            top: 0;
            right: 0;
        }}
    </style>

    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
    </head>
    <body>
    <div id="container">
        <div id="text-box">
    """

    for i, obj in enumerate(objects.iterrows()):
        index, data = obj
        x_min = data[0]
        y_min = data[1]
        x_max = data[2]
        y_max = data[3]

        # Create a unique ID for each object
        object_id = f"object_{i}"

        # Crop the object from the original image
        cropped_img = img.crop((x_min, y_min, x_max, y_max))
        cropped_img_path = os.path.join("uploads", f"cropped_{i}.png")
        cropped_img.save(cropped_img_path)

        # Add the object to the HTML page with its CSS position
        html_content += f"""
        <div class="object" id="{object_id}" style="left:{x_min}px; top:{y_min}px;">
            <img src="{cropped_img_path}">
        </div>
        """

    html_content += """
    </div>
    <script>
    var arrowKeySpeed = 10; // Adjust the speed as needed
    var selectedObject = null;

    $(document).ready(function() {
        $('.object').draggable({
            grid: [10, 10], // Define the grid with your preferred cell size
            start: function(event, ui) {
                selectedObject = $(this);
            }
        });

        $(document).on('keydown', function(e) {
            var keyCode = e.which;

            if (selectedObject) {
                var currentPosition = selectedObject.position();
                var newLeft = currentPosition.left;
                var newTop = currentPosition.top;

                if (keyCode === 37) {
                    newLeft -= arrowKeySpeed;
                } else if (keyCode === 38) {
                    newTop -= arrowKeySpeed;
                } else if (keyCode === 39) {
                    newLeft += arrowKeySpeed;
                } else if (keyCode === 40) {
                    newTop += arrowKeySpeed;
                }

                selectedObject.css({
                    top: newTop,
                    left: newLeft
                });
            }
        });

        // Listen for the "Delete" key (key code 46) and "Backspace" key (key code 8) and call deleteObject
        $(document).on('keydown', function(e) {
            if (e.which === 46 || e.which === 8) {
                if (selectedObject) {
                    deleteObject(selectedObject.attr('id'));
                }
            }
        });

        // Handle the single-click activation and deactivation
        $('.object').on('click', function(e) {
            if (selectedObject && selectedObject[0] === this) {
                // Toggle the selected state of the object
                $(this).toggleClass('selected');
            } else {
                // Activate the clicked object
                selectedObject = $(this);
                $('.object').not(this).removeClass('selected');
                $(this).addClass('selected');
            }
            e.stopPropagation(); // Prevent this click from closing the features
        });

        $(document).on('click', function() {
            // Deactivate all features when clicking anywhere else
            selectedObject = null;
            $('.object').removeClass('selected');
        });
    });

    function deleteObject(objectId) {
        $("#" + objectId).remove();
        selectedObject = null;
        $('.object').removeClass('selected');
    }
    $(document).ready(function() {
        $('#image-container').on('mousedown', function(e) {
            // Create a new crop box when clicking on the image
            var x = e.pageX - $(this).offset().left;
            var y = e.pageY - $(this).offset().top;
            var newCropBox = $('<div class="crop-box"></div>');

            $(this).append(newCropBox);

            newCropBox.css({
                left: x + 'px',
                top: y + 'px'
            });
            e.stopPropagation();
        });
    });
</script>
    </body>
    </html>
    """

    return html_content
