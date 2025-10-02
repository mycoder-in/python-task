import os
from PIL import Image

# Input and output folders
input_folder = "C://Users//MYTHILI G//Downloads//Untitled7_20250401173702-removebg-preview.png"  # folder with original images
output_folder = "C://Downloads" #folder to save resized images

# Make sure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Desired size (width, height)
size = (300, 300)

# Loop through all files in the input folder
for filename in os.listdir(input_folder):
    if filename.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
        img_path = os.path.join(input_folder, filename)
        img = Image.open(img_path)

        # Resize image
        img_resized = img.resize(size)

        # Save resized image to output folder
        save_path = os.path.join(output_folder, filename)
        img_resized.save(save_path)

        print(f"Resized and saved: {save_path}")

print("✅ All images have been resized and saved!")
