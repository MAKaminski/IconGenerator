"""
This script fetches images from Unsplash based on a user-provided theme, resizes them to 64x64 pixels, 
and saves them to a directory. It also provides an option to only fetch images that have an equal aspect ratio.
"""

import os
from PIL import Image, ImageOps
import requests
from io import BytesIO
from termcolor import colored
from dotenv import load_dotenv

load_dotenv()

UNSPLASH_ACCESS_KEY = os.getenv('UNSPLASH_ACCESS_KEY')

def prompt_user_for_theme():
    """
    Prompts the user to enter a theme and returns the entered theme.
    """
    theme = input("Please enter a theme: ")
    print(f"User entered theme: {theme}\n{'-'*50}")
    return theme

def prompt_user_for_inputs():
    """
    Prompts the user to enter a theme, resolution, and batch size, and returns these inputs.
    """
    theme = input("Please enter a theme: ")
    print(f"User entered theme: {theme}")

    print("Please select a resolution:")
    print("1. 64x64")
    print("2. 1000x420")
    print("3. Custom")
    resolution_choice = input("Enter your choice (1, 2, or 3): ")
    if resolution_choice == '1':
        resolution = (64, 64)
    elif resolution_choice == '2':
        resolution = (1000, 420)
    elif resolution_choice == '3':
        width = int(input("Enter custom width: "))
        height = int(input("Enter custom height: "))
        resolution = (width, height)
    else:
        print("Invalid choice. Defaulting to 64x64.")
        resolution = (64, 64)
    print(f"User selected resolution: {resolution}")

    print("Please select a batch size:")
    print("1. 1 image")
    print("2. 10 images")
    print("3. Custom")
    batch_size_choice = input("Enter your choice (1, 2, or 3): ")
    if batch_size_choice == '1':
        batch_size = 1
    elif batch_size_choice == '2':
        batch_size = 10
    elif batch_size_choice == '3':
        batch_size = int(input("Enter custom batch size: "))
    else:
        print("Invalid choice. Defaulting to 1 image.")
        batch_size = 1
    print(f"User selected batch size: {batch_size}")

    print('-'*50)
    return theme, resolution, batch_size

def fetch_images_from_unsplash(theme, resolution, batch_size, config):
    """
    Fetches images from Unsplash based on the provided theme and configuration.
    If 'match_aspect_ratio' in the configuration is True, only fetches images that have an equal aspect ratio.
    Resizes the fetched images to 64x64 pixels and returns them as a list of PIL Image objects.
    """
    print(f"Fetching images for theme: {theme}")
    response = requests.get(f'https://api.unsplash.com/search/photos?query={theme}&client_id={UNSPLASH_ACCESS_KEY}&per_page={batch_size}')

    if response.status_code == 200:
        data = response.json()
        images = []
        for i, result in enumerate(data['results']):
            img_url = result['urls']['small']
            img_response = requests.get(img_url)
            print(f'Response content: {img_response.content}')
            img = Image.open(BytesIO(img_response.content))
            print(f'Image: {img}')
            
            # Check if the image has an equal aspect ratio
            if not config['match_aspect_ratio'] or img.width == img.height:
                # Resize the image to 64x64 pixels
                img = img.resize((64, 64))
                images.append(img)
                print(f"Image {i+1} fetched and resized")
            else:
                print(f"Image {i+1} skipped due to unequal aspect ratio")
        
        print(f"Finished fetching images for theme: {theme}")
        print(f"Number of images retrieved: {len(images)}")
        if len(images) == 0:
            print(colored('No images were retrieved.', 'red'))
        print('-'*50)
        return images
    else:
        print(f"Failed to get images for theme '{theme}' from Unsplash API. Status code: {response.status_code}")
        return []

def convert_to_grayscale_and_contrast(image):
    """
    Converts the provided image to grayscale and applies high contrast.
    Returns the converted image.
    """
    grayscale_image = ImageOps.grayscale(image)
    high_contrast_image = ImageOps.autocontrast(grayscale_image)
    return high_contrast_image

def save_icons_to_directory(icons, theme, prefix):
    """
    Saves the provided icons to the 'app/src/icons/{theme}' directory.
    """
    print(f"Current working directory: {os.getcwd()}")
    if not os.path.exists(f'app/src/icons/{theme}/{prefix}'):
        os.makedirs(f'app/src/icons/{theme}/{prefix}')
    for i, icon in enumerate(icons):
        icon.save(f'app/src/icons/{theme}/{prefix}/{theme}_{prefix}_{i}.png')
        print(f"Saved image: app/src/icons/{theme}/{prefix}/{theme}_{prefix}_{i}.png")
    print(f"Finished saving images for theme: {theme}\{prefix}\n{'-'*50}")

def process_images(theme):
    config = {
        'match_aspect_ratio': False
    }
    icons = fetch_images_from_unsplash(theme, config)
    save_icons_to_directory(icons, theme, prefix="Base")
    grayscale_icons = [convert_to_grayscale_and_contrast(icon) for icon in icons]
    save_icons_to_directory(grayscale_icons, theme, prefix="HighContrast")

def main():
    """
    Main function that prompts the user for a theme, fetches images based on the theme, and saves them to a directory.
    Then converts the images to grayscale with high contrast and saves them to a different directory.
    """
    config = {
        'match_aspect_ratio': False
    }
    theme, resolution, batch_size = prompt_user_for_inputs()
    icons = fetch_images_from_unsplash(theme, resolution, batch_size, config)
    
    # Save the original icons
    save_icons_to_directory(icons, theme, prefix="Base")
    
    # Convert the icons to grayscale with high contrast and save them
    grayscale_icons = [convert_to_grayscale_and_contrast(icon) for icon in icons]
    save_icons_to_directory(grayscale_icons, theme, prefix="HighContrast")

if __name__ == "__main__":
    main()