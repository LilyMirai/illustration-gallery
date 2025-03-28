import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))  # Adjusted path

from gui.app_window import AppWindow
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox
from services.data_manager import DataManager  # Import the new methods

def main():
    app = QApplication(sys.argv)

    # Load the root folder from the configuration file
    root_folder = DataManager.load_root_folder()

    if not root_folder:
        # If no root folder is configured, ask the user to select one
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText("No root folder configured. Please select a root folder.")
        msg_box.setWindowTitle("Select Root Folder")
        msg_box.exec_()

        root_folder = QFileDialog.getExistingDirectory(None, "Select Root Folder")
        if not root_folder:
            print("No folder selected. Exiting application.")
            sys.exit(0)

        # Save the selected root folder to the configuration file
        DataManager.save_root_folder(root_folder)

    print(f"Using root folder: {root_folder}")

    window = AppWindow(root_folder)  # Pass root_folder to AppWindow
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()