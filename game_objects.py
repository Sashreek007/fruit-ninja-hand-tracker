import random


class Balloon:
    def __init__(self, screen_width, screen_height, btype="normal"):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.type = btype
        self.radius = 30
        self.speed = random.randint(5, 10)
        self.reset()
        self.dx = random.uniform(-2, 2)  # initial sideways drift

    def reset(self):
        self.x = random.randint(100, self.screen_width - 100)
        self.y = self.screen_height  # ✅ Start at bottom!

    def move(self, speed_multiplier=1.0, score=0):
        # Increase drift with score for more wind effect
        max_drift = min(2 + score // 50, 5)
        self.dx += random.uniform(-0.2, 0.2)
        self.dx = max(min(self.dx, max_drift), -max_drift)

        self.x += self.dx
        self.y -= self.speed * speed_multiplier  # ✅ Float UPWARD!

        if self.x < 50 or self.x > self.screen_width - 50:
            self.dx *= -1  # bounce off sides

    def is_off_screen(self):
        # ✅ Off screen when fully above the top
        return self.y < -self.radius

    def position(self):
        return (self.x, self.y)
