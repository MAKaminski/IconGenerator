# Unsplash Image Fetcher

This script fetches images from Unsplash based on a user-provided theme, resizes them to 64x64 pixels, and saves them to a directory. It also provides an option to only fetch images that have an equal aspect ratio. After fetching and saving the original images, the script converts them to grayscale with high contrast and saves them to a different directory.

## Prerequisites

- Python 3.6 or higher
- The following Python packages: `PIL`, `requests`, `termcolor`
- An Unsplash Access Key

## Setup

1. Clone this repository.
2. Install the required Python packages using pip:

    ```bash
    pip install pillow requests termcolor
    ```

3. Replace `UNSPLASH_ACCESS_KEY` in `main.py` with your Unsplash Access Key.

## Usage

Run `main.py`:

```bash
python main.py

When prompted, enter a theme. The script will fetch images based on this theme from Unsplash, resize them to 64x64 pixels, and save them to the 'app/src/icons/{theme}/Base' directory. It will then convert the images to grayscale with high contrast and save them to the 'app/src/icons/{theme}/HighContrast' directory.

Configuration
You can modify the config dictionary in the main function in main.py to change the script's behavior. Currently, the only configuration option is match_aspect_ratio, which determines whether the script should only fetch images that have an equal aspect ratio. Set it to True to only fetch square images, or False to fetch images of any aspect ratio.

```

This README provides a brief description of the program, instructions for setting up and running the program, and information about the program's configuration options. You can add more sections as needed, such as a section for contributing guidelines or a section for license information.

## Operations

1) The program starts by executing the main function.

2) The main function first sets up a configuration dictionary. Currently, the only configuration option is match_aspect_ratio, which is set to False by default. This means that by default, the program will fetch images of any aspect ratio.

3) The main function then calls prompt_user_for_theme to prompt the user to enter a theme. The entered theme is returned and stored in the theme variable.

4) The main function calls fetch_images_from_unsplash with the entered theme and the configuration dictionary. This function fetches images from Unsplash based on the theme and configuration, resizes them to 64x64 pixels, and returns them as a list of PIL Image objects.

5) The main function calls save_icons_to_directory with the list of images, the theme, and the prefix "Base". This function saves the images to the 'app/src/icons/{theme}/Base' directory.

6) The main function converts each image in the list to grayscale with high contrast by calling convert_to_grayscale_and_contrast in a list comprehension. The grayscale images are stored in a new list.

7) The main function calls save_icons_to_directory again, this time with the list of grayscale images, the theme, and the prefix "HighContrast". This function saves the grayscale images to the 'app/src/icons/{theme}/HighContrast' directory.

8) The program ends after the main function finishes executing.