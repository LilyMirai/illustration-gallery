import os
import json  # For handling configuration files
from src.models.illustration import Illustration
from PIL import Image  # Import Pillow for image resolution handling
from PyQt5.QtGui import QIcon  # Import QIcon for file icon usage

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
    tagged_folders = []

    for item_name in os.listdir(root_folder):
        item_path = os.path.join(root_folder, item_name)
        display_name = item_name
        tags = []

        # Extract all tags and clean display name
        while "[" in display_name and "]" in display_name:
            start = display_name.find("[") + 1
            end = display_name.find("]")
            tags.append(display_name[start:end])
            display_name = display_name[end + 1:].strip()

        if os.path.isdir(item_path):  # Process folders
            highest_res_image = get_highest_resolution_image(item_path)
            if highest_res_image:
                tagged_folders.append({
                    "tags": tags,
                    "display_name": display_name,
                    "path": item_path,
                    "highest_res_image": highest_res_image,
                    "last_edited": os.path.getmtime(item_path)
                })
            elif any(file.lower().endswith('.clip') for file in os.listdir(item_path)):  # Check for .clip files
                tagged_folders.append({
                    "tags": tags,
                    "display_name": display_name,
                    "path": item_path,
                    "highest_res_image": None,  # No image, but will use .clip fallback
                    "last_edited": os.path.getmtime(item_path)
                })
        elif os.path.isfile(item_path) and item_name.lower().endswith(('.png', '.jpg', '.jpeg')):  # Process image files
            illustration = Illustration(
                title=display_name,
                image_path=item_path,
                last_edited=os.path.getmtime(item_path),
                progress_state="Not Started"
            )
            illustration.tags = tags  # Add tags to the illustration
            illustrations.append(illustration)

    # Sort tagged folders based on tag priority
    tag_priority = {"Aa - Current": 0, "Done": 1, "WIP": 2, "FullPiece": 3, "Graphic Design": 4}
    tagged_folders.sort(key=lambda x: min(tag_priority.get(tag, 5) for tag in x["tags"]))

    # Add tagged folders to illustrations
    for folder in tagged_folders:
        illustration = Illustration(
            title=folder["display_name"],
            image_path=folder["highest_res_image"] or folder["path"],  # Use folder path if no image
            last_edited=folder["last_edited"],
            progress_state="Not Started"
        )
        illustration.tags = folder["tags"]  # Add tags to the illustration
        illustrations.append(illustration)

    return illustrations

def get_highest_resolution_image(path, grid_height=150):
    """
    If the path is a file, return the file itself.
    If the path is a folder, find the highest resolution image inside it.
    Create a thumbnail for folder images and return its path.
    If no image is found but a .clip file exists, use a file icon as the thumbnail.
    """
    if os.path.isfile(path):
        return path  # Return the file itself if it's a file

    thumbnail_path = os.path.join(path, "gallery_thumbnail.png")  # Save as PNG
    if os.path.exists(thumbnail_path):
        return thumbnail_path  # Return the existing thumbnail if it exists

    highest_res_image = None
    highest_res = 0
    clip_file = None

    for root, _, files in os.walk(path):  # Recursively walk through the folder
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
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
            elif file_name.lower().endswith('.clip'):
                clip_file = file_path  # Track the .clip file if no image is found

    if highest_res_image:
        try:
            with Image.open(highest_res_image) as img:
                # Convert RGBA to RGB if necessary
                if img.mode == "RGBA":
                    img = img.convert("RGB")

                # Calculate the scaling factor to ensure the height matches grid_height
                scale_factor = grid_height / img.height
                new_width = int(img.width * scale_factor)
                new_height = grid_height

                # Create a thumbnail with the new dimensions
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)  # Use LANCZOS for resizing

                # Remove ICC profile before saving to avoid libpng warnings
                img.save(thumbnail_path, "PNG")  # Save the thumbnail as PNG
            return thumbnail_path
        except Exception as e:
            print(f"Error creating thumbnail for {highest_res_image}: {e}")

    # If no image is found but a .clip file exists, use a file icon
    if clip_file:
        try:
            icon = QIcon.fromTheme("text-x-generic")  # Use a generic file icon
            pixmap = icon.pixmap(grid_height, grid_height)  # Create a pixmap for the icon
            pixmap.save(thumbnail_path, "PNG")  # Save the icon as a thumbnail
            return thumbnail_path
        except Exception as e:
            print(f"Error creating thumbnail for .clip file {clip_file}: {e}")

    return None