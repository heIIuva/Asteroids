# main.py

import tkinter as tk
from config import (CANVAS_WIDTH, CANVAS_HEIGHT, SHIP_IMAGE, MISSILE_IMAGE, ROCK_IMAGE,
                    NEBULA_IMAGE, SPLASH_IMAGE, SHIP_THRUST_IMAGE, FPS)
from vector import Vector
from ship import Ship
from image_manager import ImageManager
from game_logic import GameLogic

class RiceRocksApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Asteroids Game")

        self.canvas = tk.Canvas(master, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="black")
        self.canvas.pack()

        # images loader
        self.img_manager = ImageManager()
        self.img_manager.load_image("ship", SHIP_IMAGE)
        self.img_manager.load_image("ship_thrust", SHIP_THRUST_IMAGE)  # загружаем thrust-изображение корабля
        self.img_manager.load_image("missile", MISSILE_IMAGE)
        self.img_manager.load_image("rock", ROCK_IMAGE)
        self.img_manager.load_image("nebula", NEBULA_IMAGE)
        self.img_manager.load_image("splash", SPLASH_IMAGE)

        self.images = {
            "ship": self.img_manager.get_image("ship"),
            "ship_thrust": self.img_manager.get_image("ship_thrust"),
            "missile": self.img_manager.get_image("missile"),
            "rock": self.img_manager.get_image("rock"),
            "nebula": self.img_manager.get_image("nebula"),
            "splash": self.img_manager.get_image("splash")
        }

        # init ship
        ship_pos = Vector(CANVAS_WIDTH/2, CANVAS_HEIGHT/2)
        ship_vel = Vector(0, 0)
        self.ship = Ship(ship_pos, ship_vel, 0, "ship", "ship_thrust", self.img_manager)

        # init game logic
        self.game = GameLogic(self.ship, self.images, self.img_manager)

        # button handlers bounds
        self.master.bind("<KeyPress>", self.on_key_press)
        self.master.bind("<KeyRelease>", self.on_key_release)
        self.master.bind("<Button-1>", self.on_mouse_click)

        self.keys = set()

        self.drawn_images = []

        # game start
        self.update_game()
        self.master.after(1000, self.spawn_rock_periodically)

    def on_key_press(self, event):
        self.keys.add(event.keysym)
        self.handle_keys()

    def on_key_release(self, event):
        if event.keysym in self.keys:
            self.keys.remove(event.keysym)
        self.handle_keys()

    def handle_keys(self):
        self.ship.stop_rotate()

        if "Left" in self.keys:
            self.ship.rotate_left()
        if "Right" in self.keys:
            self.ship.rotate_right()
        if "Up" in self.keys:
            self.ship.set_thrust(True)
        else:
            self.ship.set_thrust(False)
        if "space" in self.keys:
            self.game.shoot()

    def on_mouse_click(self, event):
        if not self.game.started:
            self.game.start()

    def spawn_rock_periodically(self):
        if self.game.started:
            self.game.add_rock()
        self.master.after(1000, self.spawn_rock_periodically)

    def update_game(self):
        self.canvas.delete("all")
        self.drawn_images = []
        self.game.update()
        self.game.draw(self.canvas, self.drawn_images)
        self.master.after(int(1000/FPS), self.update_game)

if __name__ == "__main__":
    root = tk.Tk()
    app = RiceRocksApp(root)
    root.mainloop()
