import cv2
import numpy as np
import os
from PIL import Image

def process_image_to_gif(image_path, output_path, frame_duration):
    # Load the image using OpenCV
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    height, width = img.shape

    # Step 1: Preprocess the Image
    blurred = cv2.GaussianBlur(img, (5, 5), 0)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced_img = clahe.apply(blurred)

    # Step 2: Edge Detection
    sobel_x = cv2.Sobel(enhanced_img, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(enhanced_img, cv2.CV_64F, 0, 1, ksize=3)
    sobel = cv2.magnitude(sobel_x, sobel_y)
    sobel = np.uint8(255 * sobel / np.max(sobel))
    edges = cv2.Canny(sobel, 50, 150)

    # Step 3: Detect the central lines

    horizontal_projection = np.sum(edges, axis=1)
    vertical_projection = np.sum(edges, axis=0)
    h_min = int(height * 0.4)
    h_max = int(height * 0.6)
    v_min = int(width * 0.4)
    v_max = int(width * 0.6)
    h_center = np.argmax(horizontal_projection[h_min:h_max]) + h_min
    v_center = np.argmax(vertical_projection[v_min:v_max]) + v_min

    # Step 4: Crop Frames and create array

    frames_coords = [
        (0, 0, v_center, h_center),             # Top-left
        (0, h_center, v_center, height),        # Bottom-left
        (v_center, h_center, width, height),    # Bottom-right
        (v_center, 0, width, h_center),         # Top-right
    ]

    frames = []
    for (x1, y1, x2, y2) in frames_coords:
        cropped_frame = img[y1:y2, x1:x2]
        pil_frame = Image.fromarray(cropped_frame)
        frames.append(pil_frame)

    # Step 5: Save the frames as a GIF
    frames[0].save(output_path, save_all=True, append_images=frames[1:], duration=frame_duration, loop=0)

def process_folder(input_folder, frame_duration):
    output_folder = os.path.join(input_folder, 'gifs_naiveedge')

    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Process each image in the folder
    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg'):
            image_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, f'{os.path.splitext(filename)[0]}.gif')
            process_image_to_gif(image_path, output_path, frame_duration)

# Example usage:
input_folder = 'test'  # Replace with the path to your folder
frame_duration = 250   # Frame duration in milliseconds
process_folder(input_folder, frame_duration)