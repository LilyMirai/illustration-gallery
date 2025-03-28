import sys
import os

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QScrollArea, QFrame, QHBoxLayout, QSizePolicy  # Import additional widgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QEvent
from services.data_manager import get_highest_resolution_image  # Import the helper function
import subprocess
from PIL import Image  # Import the Image module from Pillow
from io import BytesIO  # For in-memory thumbnail creation

class GalleryView(QWidget):
    def __init__(self, illustrations, grid_height=150):  # Add grid_height parameter
        super().__init__()
        self.illustrations = illustrations
        self.grid_height = grid_height  # Store grid height
        self.selected_frame = None  # Track the currently selected frame
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
                # Ensure thumbnails are resized to match the grid height
                thumbnail_path = get_highest_resolution_image(illustration.image_path, self.grid_height)
                pixmap = QPixmap(thumbnail_path)

                # Create a layout for each grid cell
                cell_layout = QVBoxLayout()
                tile_frame = QFrame()
                tile_frame.setLayout(cell_layout)
                tile_frame.setFrameShape(QFrame.StyledPanel)
                tile_frame.setStyleSheet("border: 1px solid lightgray;")
                tile_frame.setCursor(Qt.PointingHandCursor)

                # Handle click events
                tile_frame.installEventFilter(self)
                tile_frame.setProperty("path", illustration.image_path)

                thumbnail = QLabel()
                thumbnail.setPixmap(pixmap)
                thumbnail.setAlignment(Qt.AlignCenter)

                # Add title label below the image with tag-based styling
                truncated_title = illustration.title[:30] + "..." if len(illustration.title) > 30 else illustration.title
                title_label = QLabel(truncated_title)
                title_label.setAlignment(Qt.AlignCenter)

                # Apply styles based on tags
                if hasattr(illustration, "tags"):
                    tags = illustration.tags if isinstance(illustration.tags, list) else [illustration.tags]
                    for tag in tags:
                        if "WIP" in tag:
                            title_label.setStyleSheet("background-color: #FFFACD; color: black;")  # Soft yellow
                        elif "FullPiece" in tag:
                            title_label.setStyleSheet("background-color: #90EE90; color: black;")  # Soft green
                        if "Done" in tag:
                            truncated_title = f"✓ {truncated_title}"  # Add checkmark for "Done"
                            title_label.setText(truncated_title)
                            title_label.setStyleSheet("background-color: #D3D3D3; color: black;")  # Soft gray

                # Add thumbnail and title to the cell layout
                cell_layout.addWidget(thumbnail)
                cell_layout.addWidget(title_label)

                # Add the tile frame to the grid
                grid_layout.addWidget(tile_frame, index // 4, index % 4)  # Ensure 4 images per row
            except Exception as e:
                print(f"Error displaying illustration {illustration.image_path}: {e}")

        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area)

        # Add a label to display the number of illustrations loaded
        footer_layout = QHBoxLayout()
        footer_layout.addStretch()  # Push the label to the right
        count_label = QLabel(f"Illustrations loaded: {len(self.illustrations)}")
        count_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        count_label.setStyleSheet("color: #FFFFFF;")  # Match the dark theme
        footer_layout.addWidget(count_label)
        layout.addLayout(footer_layout)

        self.setLayout(layout)

    def eventFilter(self, source, event):
        if event.type() == QEvent.MouseButtonPress and isinstance(source, QFrame):
            self.highlight_frame(source)
            return True
        elif event.type() == QEvent.MouseButtonDblClick and isinstance(source, QFrame):
            path = source.property("path")
            if path:
                self.open_path_in_explorer(path)
            return True
        return super().eventFilter(source, event)

    def highlight_frame(self, frame):
        """Highlight the selected frame and reset the previous selection."""
        if self.selected_frame:
            self.selected_frame.setStyleSheet("border: 1px solid lightgray;")  # Reset previous selection
        frame.setStyleSheet("border: 1px solid blue; background-color: lightblue;")  # Highlight selected frame
        self.selected_frame = frame

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