class UserData:
    def __init__(self, gallery_root_path):
        self.gallery_root_path = gallery_root_path

    def get_gallery_root_path(self):
        return self.gallery_root_path

    def set_gallery_root_path(self, path):
        self.gallery_root_path = path