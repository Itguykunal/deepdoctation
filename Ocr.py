import cv2
import pytesseract

def process_image(image_path):
    img = cv2.imread(image_path)
    horizontal_shift = -7.5

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to create a binary image
    ret, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    # Use Tesseract to extract text from the binary image
    data = pytesseract.image_to_data(thresh, output_type=pytesseract.Output.DICT)

    # Create a list to store text elements
    text_elements = []

    # Loop through the extracted text data and store text elements
    for i in range(len(data['text'])):
        if int(data['conf'][i]) > 0:
            x, y, w, h = int(data['left'][i]), int(data['top'][i]), int(data['width'][i]), int(data['height'][i])
            text = data['text'][i]
            text_elements.append((x, y, w, h, text))

    # Sort text elements by Y coordinates
    text_elements.sort(key=lambda item: item[1])

    # Initialize variables to track the maximum extents
    max_x = 0
    max_y = 0

    # Group text elements with similar Y coordinates and adjust Y to align them
    grouped_text = []
    current_line = []
    prev_y = -1

    for element in text_elements:
        x, y, w, h, text = element

        if prev_y == -1 or abs(y - prev_y) < 5:  # Adjust this threshold as needed
            current_line.append(element)
        else:
            if current_line:
                min_y = min(current_line, key=lambda item: item[1])[1]
                for line_element in current_line:
                    ex, ey, ew, eh, etext = line_element
                    ey = min_y
                    max_x = max(max_x, ex + ew)
                    max_y = max(max_y, ey + eh)
                    grouped_text.append((ex, ey, ew, eh, etext))
                current_line = []
            current_line.append(element)
        prev_y = y

    # Handle the last line of text
    if current_line:
        min_y = min(current_line, key=lambda item: item[1])[1]
        for line_element in current_line:
            ex, ey, ew, eh, etext = line_element
            ey = min_y
            max_x = max(max_x, ex + ew)
            max_y = max(max_y, ey + eh)
            grouped_text.append((ex, ey, ew, eh, etext))

    # Define the HTML template with dynamically calculated box size and centered position

    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Editable Invoice</title>
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
        <link rel="stylesheet" href="https://code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">
        <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
        <style>
           #container {{
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}}

#text-box {{
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: {max_x + 20}px;
    height: {max_y + 20}px;
    padding: 10px;
}}
            .editable-text {{
                border: 1px solid transparent; /* Initially, the border is transparent */
                position: absolute;
                padding: 2px;
                cursor: text; /* Change cursor to text when hovering over editable text */
                white-space: nowrap; /* Prevent text from breaking to the next line */
            }}

            .editable-text:hover {{
                border: 1px dashed #000; /* Add a dashed border when hovering */
            }}
    .editable-text.selected {{
        background-color: NA; /* Change the background color to highlight selected elements */
        border: 2px solid black; /* Add a border to selected elements */
    }}
        .selection-box {{
        border: 2px dashed #000; /* Style the selection box with a dashed border */
        position: absolute;
    }}


            @media print {{
                #text-box {{
                    border: none; /* Hide the black border box when printing */
                }}

                .download-button {{
                    display: none;
                }}

                body {{
                    margin: 0; /* Set margin to none for the entire page */
                    transform-origin: top; /* Ensure scaling origin is top for correct positioning */
                }}

                @page {{
                    size: auto;
                    margin: 0mm;
                }}
            }}
        </style>
    </head>
    <body>
    
        <div id="container">
            <div id="text-box">
    """

    # Loop through the grouped text elements and create HTML elements with a left shift
    for element in grouped_text:
        x, y, w, h, text = element

        # Add the contentEditable attribute to make the text elements editable
        html_template += f'<div class="editable-text" style="left:{x}px; top:{y}px; width:{w}px; height:{h}px;" contentEditable="true">{text}</div>\n'

    # Close the text-box and the HTML template
    html_template += """
            </div>
        </div>
    </body>
<script>
    $(document).ready(function() {
        let grid = 5; // Adjust the grid size as needed

        // Function to move the element using arrow keys
        function moveElement(element, direction) {
            const x = parseInt(element.css('left'));
            const y = parseInt(element.css('top'));
            const step = grid;

            if (direction === 'left') {
                element.css('left', x - step + 'px');
            } else if (direction === 'right') {
                element.css('left', x + step + 'px');
            } else if (direction === 'up') {
                element.css('top', y - step + 'px');
            } else if (direction === 'down') {
                element.css('top', y + step + 'px');
            }
        }

        // Initialize draggable elements with grid and draggable options
        $(".editable-text").draggable({
            grid: [grid, grid], // Adjust the grid size as needed for precise positioning
        });

        let isEditing = false;

        // Enable arrow key functionality for moving text elements
        $(document).on('keydown', function(e) {
            const selectedElements = $(".editable-text.selected");
            if (selectedElements.length > 0 && e.key.startsWith('Arrow')) {
                if (isEditing) {
                    selectedElements.each(function() {
                        moveElement($(this), e.key.replace('Arrow', '').toLowerCase());
                    });
                }
                e.preventDefault(); // Prevent scrolling the page with arrow keys
            }
        });

        // Toggle between cursor movement and drag-and-drop on double-click
        $(document).on('dblclick', '.editable-text', function(e) {
            const element = $(this);

            if (element.hasClass('selected')) {
                isEditing = !isEditing;
                if (isEditing) {
                    element.draggable('disable');
                } else {
                    element.draggable('enable');
                }
            }
        });

        // Single click to select and activate cursor movement
        $(document).on('click', '.editable-text', function(e) {
            const element = $(this);

            if (element.hasClass('selected')) {
                if (e.ctrlKey) {
                    element.removeClass('selected');
                }
            } else {
                element.addClass('selected');
            }

            if (isEditing) {
                isEditing = false;
                element.draggable('enable');
            } else {
                // Check if the element is within the bounds of the blue selection box
                const blueBox = $('.selection-box');
                const elementRect = element[0].getBoundingClientRect();
                const blueBoxRect = blueBox[0].getBoundingClientRect();
                if (
                    elementRect.left >= blueBoxRect.left &&
                    elementRect.right <= blueBoxRect.right &&
                    elementRect.top >= blueBoxRect.top &&
                    elementRect.bottom <= blueBoxRect.bottom
                ) {
                    isEditing = true;
                    element.draggable('disable');
                }
            }
        });

        // Delete selected elements on the Delete key press
        $(document).on('keydown', function(e) {
            if (e.which === 46 || e.which === 8) {
                $(".editable-text.selected").remove();
            }
        });
        
        // Enable multiple box selection with the mouse
        let isSelecting = false;
        let startX, startY;

        $(document).on('mousedown', 'body', function(e) {
            if (!e.ctrlKey) {
                $(".editable-text").removeClass('selected');
            }
            isSelecting = true;
            startX = e.pageX;
            startY = e.pageY;
        });

        $(document).on('mousemove', 'body', function(e) {
            if (isSelecting) {
                let selectionBox = $('.selection-box');
                if (!selectionBox.length) {
                    $('body').append('<div class="selection-box"></div>');
                    selectionBox = $('.selection-box');
                }
                selectionBox.css({
                    'display': 'block',
                    'position': 'absolute',
                    'left': Math.min(startX, e.pageX),
                    'top': Math.min(startY, e.pageY),
                    'width': Math.abs(e.pageX - startX),
                    'height': Math.abs(e.pageY - startY),
                });

                $(".editable-text").each(function() {
                    const element = $(this);
                    if (isColliding(selectionBox, element)) {
                        element.addClass('selected');
                    } else {
                        element.removeClass('selected');
                    }
                });
            }
        });

        $(document).on('mouseup', 'body', function() {
            $('.selection-box').remove();
            isSelecting = false;
        });

        // Function to check if two elements are colliding
        function isColliding(elem1, elem2) {
            const rect1 = elem1[0].getBoundingClientRect();
            const rect2 = elem2[0].getBoundingClientRect();
            return (
                rect1.left < rect2.right &&
                rect1.right > rect2.left &&
                rect1.top < rect2.bottom &&
                rect1.bottom > rect2.top
            );
        }
    });
</script>
    </html>
    """

    return html_template