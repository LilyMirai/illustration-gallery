import sys
import os

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QScrollArea, QFrame
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QEvent
from services.data_manager import get_highest_resolution_image  # Import the new helper function
import subprocess
from PIL import Image  # Import the Image module from Pillow
from io import BytesIO  # For in-memory thumbnail creation

class GalleryView(QWidget):
    def __init__(self, illustrations):
        super().__init__()
        self.illustrations = illustrations
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Add a scrollable area for the grid layout
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        grid_layout = QGridLayout(scroll_content)

        # Populate the grid with illustrations
        for index, illustration in enumerate(self.illustrations):
            try:
                if os.path.isdir(illustration.image_path):
                    pixmap = QPixmap(illustration.image_path)  # Use the saved thumbnail
                else:
                    # Create an in-memory thumbnail for root directory files
                    with Image.open(illustration.image_path) as img:
                        img.thumbnail((150, 150))  # Adjust thumbnail size
                        buffer = BytesIO()
                        img.save(buffer, format="JPEG")
                        pixmap = QPixmap()
                        pixmap.loadFromData(buffer.getvalue())

                # Create a layout for each grid cell
                cell_layout = QVBoxLayout()
                tile_frame = QFrame()
                tile_frame.setLayout(cell_layout)
                tile_frame.setFrameShape(QFrame.StyledPanel)
                tile_frame.setStyleSheet("border: 1px solid lightgray;")
                tile_frame.setCursor(Qt.PointingHandCursor)

                # Handle double-click events
                tile_frame.installEventFilter(self)
                tile_frame.setProperty("path", illustration.image_path)

                thumbnail = QLabel()
                thumbnail.setPixmap(pixmap)
                thumbnail.setAlignment(Qt.AlignCenter)

                # Add title label below the image
                truncated_title = illustration.title[:30] + "..." if len(illustration.title) > 30 else illustration.title
                title_label = QLabel(truncated_title)
                title_label.setAlignment(Qt.AlignCenter)

                # Add thumbnail and title to the cell layout
                cell_layout.addWidget(thumbnail)
                cell_layout.addWidget(title_label)

                # Add the tile frame to the grid
                grid_layout.addWidget(tile_frame, index // 4, index % 4)
            except Exception as e:
                print(f"Error displaying illustration {illustration.image_path}: {e}")

        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area)
        self.setLayout(layout)

    def eventFilter(self, source, event):
        if event.type() == QEvent.MouseButtonDblClick and isinstance(source, QFrame):
            path = source.property("path")
            if path:
                self.open_path_in_explorer(path)
            return True
        return super().eventFilter(source, event)

    def open_path_in_explorer(self, path):
        try:
            if os.path.isfile(path):  # If it's a file, open the folder and select the file
                if sys.platform == "win32":
                    subprocess.Popen(['explorer', '/select,', os.path.normpath(path)])
                else:
                    print("File selection is only supported on Windows.")
            elif os.path.isdir(path):  # If it's a folder, open the folder
                if sys.platform == "win32":
                    subprocess.Popen(['explorer', os.path.normpath(path)])
                else:
                    print("Folder opening is only supported on Windows.")
        except Exception as e:
            print(f"Failed to open path: {e}")