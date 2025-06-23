import random


class Balloon:
    def __init__(self, screen_width, screen_height, balloon_type="normal"):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.radius = 30
        self.speed = random.randint(3, 6)  # ✅ Slower base speed
        self.reset()
        self.dx = random.randint(-2, 2)
        self.type = balloon_type

    def reset(self):
        self.x = random.randint(100, self.screen_width - 100)
        self.y = self.screen_height

    def move(self, speed_multiplier=1.0, score=0):
        self.y -= self.speed * speed_multiplier
        self.x += self.dx
        if self.x < 50 or self.x > self.screen_width - 50:
            self.dx *= -1

    def is_off_screen(self):
        return self.y < -50  # flying up off screen

    def position(self):
        return (self.x, self.y)
