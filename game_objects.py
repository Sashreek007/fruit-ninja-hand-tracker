import random


class Fruit:
    def __init__(self, screen_width, screen_height, radius=30, speed=5):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.radius = radius
        self.speed = speed
        self.reset()

    def reset(self):
        self.x = random.randint(100, self.screen_width - 100)
        self.y = 0

    def move(self):
        self.y += self.speed

    def is_off_screen(self):
        return self.y > self.screen_height

    def position(self):
        return (self.x, self.y)


# Same for Bomb:
class Bomb:
    def __init__(self, screen_width, screen_height, radius=30, speed=5):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.radius = radius
        self.speed = speed
        self.reset()

    def reset(self):
        self.x = random.randint(100, self.screen_width - 100)
        self.y = 0

    def move(self):
        self.y += self.speed

    def is_off_screen(self):
        return self.y > self.screen_height

    def position(self):
        return (self.x, self.y)
