import os
import json  # For handling configuration files
from src.models.illustration import Illustration
from PIL import Image  # Import Pillow for image resolution handling

CONFIG_FILE = "config.json"  # Configuration file to store the root folder path

class DataManager:
    def __init__(self, gallery_path):
        self.gallery_path = gallery_path

    def load_illustrations(self):
        # Logic to load illustrations from the gallery path
        pass

    def save_progress(self, illustration):
        # Logic to save the progress state of an illustration
        pass

    def load_progress(self, illustration):
        # Logic to load the progress state of an illustration
        pass

    def get_gallery_structure(self):
        # Logic to retrieve the folder structure of the gallery
        pass

    @staticmethod
    def save_root_folder(root_folder):
        """Save the root folder path to a configuration file."""
        with open(CONFIG_FILE, "w") as config:
            json.dump({"root_folder": root_folder}, config)

    @staticmethod
    def load_root_folder():
        """Load the root folder path from the configuration file."""
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as config:
                data = json.load(config)
                return data.get("root_folder")
        return None

def load_illustrations(root_folder):
    illustrations = []
    for item_name in os.listdir(root_folder):
        item_path = os.path.join(root_folder, item_name)
        if os.path.isdir(item_path):  # Process folders
            highest_res_image = get_highest_resolution_image(item_path)
            if highest_res_image:
                illustration = Illustration(
                    title=item_name,  # Use folder name as the title
                    image_path=highest_res_image,  # Path to the highest resolution image
                    last_edited=os.path.getmtime(item_path),  # Use folder's last modified time
                    progress_state="Not Started"  # Default progress state
                )
                illustrations.append(illustration)
        elif os.path.isfile(item_path) and item_name.lower().endswith(('.png', '.jpg', '.jpeg')):  # Process image files
            illustration = Illustration(
                title=os.path.splitext(item_name)[0],  # Use file name without extension as the title
                image_path=item_path,  # Path to the file itself
                last_edited=os.path.getmtime(item_path),  # Use file's last modified time
                progress_state="Not Started"  # Default progress state
            )
            illustrations.append(illustration)
    return illustrations

def get_highest_resolution_image(path):
    """
    If the path is a file, return the file itself.
    If the path is a folder, find the highest resolution image inside it.
    Create a thumbnail for folder images and return its path.
    """
    if os.path.isfile(path):
        return path  # Return the file itself if it's a file

    thumbnail_path = os.path.join(path, "gallery_thumbnail.jpg")
    if os.path.exists(thumbnail_path):
        return thumbnail_path  # Return the existing thumbnail if it exists

    highest_res_image = None
    highest_res = 0

    for root, _, files in os.walk(path):  # Recursively walk through the folder
        for file_name in files:
            if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                file_path = os.path.join(root, file_name)
                try:
                    with Image.open(file_path) as img:
                        # Remove invalid ICC profile in memory
                        if "icc_profile" in img.info:
                            img.info.pop("icc_profile", None)

                        resolution = img.width * img.height
                        if resolution > highest_res:
                            highest_res = resolution
                            highest_res_image = file_path
                except Exception as e:
                    print(f"Error processing image {file_path}: {e}")

    if highest_res_image:
        try:
            with Image.open(highest_res_image) as img:
                # Convert RGBA to RGB if necessary
                if img.mode == "RGBA":
                    img = img.convert("RGB")

                # Create a thumbnail (33% of the original size)
                img.thumbnail((img.width // 3, img.height // 3))
                img.save(thumbnail_path, "JPEG")  # Save the thumbnail in the folder
            return thumbnail_path
        except Exception as e:
            print(f"Error creating thumbnail for {highest_res_image}: {e}")

    return None