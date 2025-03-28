import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from .components.checklist import Checklist
from .components.social_media_tracker import SocialMediaTracker
from .components.gallery_view import GalleryView
from services.data_manager import load_illustrations  # Change to absolute import

class AppWindow(QMainWindow):
    def __init__(self, root_folder):  # Accept root_folder as a parameter
        super().__init__()
        self.setWindowTitle("Illustration Gallery")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.checklist = Checklist()
        self.social_media_tracker = SocialMediaTracker()

        # Load illustrations from the root folder
        illustrations = load_illustrations(root_folder)

        # Pass illustrations to GalleryView
        self.gallery_view = GalleryView(illustrations)

        self.layout.addWidget(self.checklist)
        self.layout.addWidget(self.social_media_tracker)
        self.layout.addWidget(self.gallery_view)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #2E2E2E;  /* Dark gray background */
                color: #FFFFFF;  /* White text for better contrast */
            }
            QLabel {
                color: #FFFFFF;  /* Ensure labels have white text */
            }
            QScrollArea {
                background-color: #2E2E2E;  /* Match scroll area background */
            }
            QFrame {
                background-color: #3E3E3E;  /* Slightly lighter gray for frames */
            }
            QTableWidget {
                background-color: #3A3A3A;  /* Comfortable gray for table background */
                color: #FFFFFF;  /* White text for table content */
                gridline-color: #444444;  /* Subtle gridline color */
            }
            QHeaderView::section {
                background-color: #4A4A4A;  /* Slightly darker gray for table headers */
                color: #FFFFFF;  /* White text for headers */
            }
            QFrame[selected="true"] {
                border: 1px solid blue;  /* Highlight border for selected tile */
                background-color: lightblue;  /* Light blue background for selected tile */
                color: black;  /* Black text for better readability */
            }
        """)

        self.show()