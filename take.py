import cv2
import os

# Global variables for box size and position
BOX_SIZE = (512, 512)
BOX_COLOR = (0, 255, 0)  # Green color
BOX_THICKNESS = 2
DRAW_BOX = True
IMAGE_DIRECTORY = "images"

direction = "data/Resources"

def draw_center_box(image):
    """Draw a box of size 512x512 at the center of the image."""
    if DRAW_BOX:
        height, width = image.shape[:2]
        # Calculate box coordinates
        x1 = (width - BOX_SIZE[0]) // 2
        y1 = (height - BOX_SIZE[1]) // 2
        x2 = x1 + BOX_SIZE[0]
        y2 = y1 + BOX_SIZE[1]
        # Draw the box
        cv2.rectangle(image, (x1, y1), (x2, y2), BOX_COLOR, BOX_THICKNESS)

def capture_image(frame, count):
    """Capture an image and save it."""
    # Create the images directory if it doesn't exist
    if not os.path.exists(IMAGE_DIRECTORY):
        os.makedirs(IMAGE_DIRECTORY)
    
    # Crop the center region
    height, width = frame.shape[:2]
    x1 = (width - BOX_SIZE[0]) // 2
    y1 = (height - BOX_SIZE[1]) // 2
    x2 = x1 + BOX_SIZE[0]
    y2 = y1 + BOX_SIZE[1]
    cropped_frame = frame[y1:y2, x1:x2]

    # Save the image with a unique name
    filename = os.path.join(IMAGE_DIRECTORY, f"photo{count}.jpg")
    cv2.imwrite(filename, cropped_frame)
    print(f"Image '{filename}' captured!")

def main():
    # Open the default camera (usually the first camera in the system)
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

    # Initialize key variables
    global DRAW_BOX
    DRAW_BOX = True
    image_count = 1

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Check if the frame was captured successfully
        if not ret:
            print("Failed to capture frame.")
            break

        # Draw the center box on the frame
        draw_center_box(frame)

        # Display the frame
        cv2.imshow('Camera View', frame)

        # Capture an image when 'c' key is pressed
        key = cv2.waitKey(1)
        if key == ord('c'):
            capture_image(frame, image_count)
            image_count += 1

        # Disable drawing of the box when 'd' key is pressed
        elif key == ord('d'):
            DRAW_BOX = not DRAW_BOX

        # Break the loop when 'q' key is pressed
        elif key == ord('q'):
            break

    # Release the camera and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
