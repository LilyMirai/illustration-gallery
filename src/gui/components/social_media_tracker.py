from PyQt5.QtWidgets import QWidget

class SocialMediaTracker(QWidget):
    def __init__(self):
        super().__init__()
        self.platforms = {
            "Facebook": "",
            "Twitter": "",
            "Instagram": "",
            "LinkedIn": ""
        }

    def update_post(self, platform, content):
        if platform in self.platforms:
            self.platforms[platform] = content

    def get_post(self, platform):
        return self.platforms.get(platform, "")

    def display_posts(self):
        for platform, content in self.platforms.items():
            print(f"{platform}: {content}")