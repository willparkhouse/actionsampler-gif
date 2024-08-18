from PIL import Image, ImageSequence
import os
import numpy as np

def process_image_to_gif(image_path, output_path, frame_duration):
    img = Image.open(image_path)
    img_width, img_height = img.size
    frame_width = img_width // 2
    frame_height = img_height // 2
    frames = [
        img.crop((0, 0, frame_width, frame_height)),                    # Top-left
        img.crop((0, frame_height, frame_width, img_height)),           # Bottom-left
        img.crop((frame_width, frame_height, img_width, img_height)),   # Bottom-right
        img.crop((frame_width, 0, img_width, frame_height)),            # Top-right
        img.crop((frame_width, 0, img_width, frame_height)),            # Top-right
        img.crop((frame_width, frame_height, img_width, img_height)),   # Bottom-right
        img.crop((0, frame_height, frame_width, img_height)),           # Bottom-left
        img.crop((0, 0, frame_width, frame_height))                     # Top-left
    ]
    frames[0].save(output_path, save_all=True, append_images=frames[1:], duration=frame_duration, loop=0)

def process_folder(input_folder, frame_duration):
    output_folder = os.path.join(input_folder, 'gifs_boom')

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