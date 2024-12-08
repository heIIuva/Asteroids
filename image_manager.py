# image_manager.py
import os
from PIL import Image, ImageTk

class ImageManager:
    def __init__(self):
        self.images = {}  # Здесь храним PIL.Image

    def load_image(self, name, path):
        if not os.path.exists(path):
            raise FileNotFoundError(f"Image not found: {path}")
        pil_img = Image.open(path).convert("RGBA")
        self.images[name] = pil_img

    def get_image(self, name):
        return self.images.get(name, None)

    def get_rotated_image(self, name, angle_degrees):
        if name not in self.images:
            return None
        pil_img = self.images[name]
        # Поворот изображения (против часовой стрелки), поэтому -angle_degrees
        rotated = pil_img.rotate(-angle_degrees, expand=True)
        return ImageTk.PhotoImage(rotated)
