from PyQt5.QtWidgets import QWidget

class Checklist(QWidget):  # Ensure Checklist inherits from QWidget
    def __init__(self):
        super().__init__()
        self.items = []

    def add_item(self, item):
        self.items.append({"item": item, "completed": False})

    def complete_item(self, index):
        if 0 <= index < len(self.items):
            self.items[index]["completed"] = True

    def remove_item(self, index):
        if 0 <= index < len(self.items):
            del self.items[index]

    def get_items(self):
        return self.items

    def display_checklist(self):
        checklist_display = ""
        for index, item in enumerate(self.items):
            status = "✓" if item["completed"] else "✗"
            checklist_display += f"{index + 1}. [{status}] {item['item']}\n"
        return checklist_display.strip()