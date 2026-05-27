#cmd 
#pip install pygame 
import random
import tkinter as tk


class BrickBreakerGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Brick Breaker")

        self.width = 800
        self.height = 600
        self.bg_color = "#111827"

        self.canvas = tk.Canvas(
            root,
            width=self.width,
            height=self.height,
            bg=self.bg_color,
            highlightthickness=0,
        )
        self.canvas.pack()

        self.score = 0
        self.lives = 3
        self.game_running = True
        self.message_item = None

        self.paddle_width = 360
        self.paddle_height = 14
        self.paddle_speed = 10
        self.paddle_dx = 0

        paddle_x1 = (self.width - self.paddle_width) / 2
        paddle_y1 = self.height - 40
        paddle_x2 = paddle_x1 + self.paddle_width
        paddle_y2 = paddle_y1 + self.paddle_height

        self.paddle = self.canvas.create_rectangle(
            paddle_x1,
            paddle_y1,
            paddle_x2,
            paddle_y2,
            fill="#22c55e",
            outline="",
        )

        self.ball_radius = 9
        self.ball_speed = 5
        self.ball_dx = random.choice([-1, 1]) * self.ball_speed
        self.ball_dy = -self.ball_speed
        self.ball = self.canvas.create_oval(0, 0, 0, 0, fill="#fbbf24", outline="")
        self.reset_ball_position()

        self.bricks = []
        self.create_bricks(rows=6, cols=10)

        self.score_text = self.canvas.create_text(
            12,
            12,
            anchor="nw",
            fill="white",
            font=("Consolas", 14, "bold"),
            text="Score: 0",
        )
        self.lives_text = self.canvas.create_text(
            self.width - 12,
            12,
            anchor="ne",
            fill="white",
            font=("Consolas", 14, "bold"),
            text="Lives: 3",
        )

        self.root.bind("<KeyPress-Left>", self.on_key_press)
        self.root.bind("<KeyPress-Right>", self.on_key_press)
        self.root.bind("<KeyRelease-Left>", self.on_key_release)
        self.root.bind("<KeyRelease-Right>", self.on_key_release)
        self.root.bind("<KeyPress-space>", self.on_space)

        self.game_loop()

    def create_bricks(self, rows, cols):
        self.clear_bricks()

        margin_x = 40
        margin_top = 60
        gap = 6
        brick_height = 22
        total_gap = (cols - 1) * gap
        brick_width = (self.width - 2 * margin_x - total_gap) / cols

        palette = ["#ef4444", "#f97316", "#eab308", "#22c55e", "#3b82f6", "#a855f7"]

        for row in range(rows):
            for col in range(cols):
                x1 = margin_x + col * (brick_width + gap)
                y1 = margin_top + row * (brick_height + gap)
                x2 = x1 + brick_width
                y2 = y1 + brick_height
                brick = self.canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=palette[row % len(palette)],
                    outline="",
                )
                self.bricks.append(brick)

    def clear_bricks(self):
        for brick in self.bricks:
            self.canvas.delete(brick)
        self.bricks = []

    def reset_ball_position(self):
        paddle_coords = self.canvas.coords(self.paddle)
        paddle_center_x = (paddle_coords[0] + paddle_coords[2]) / 2
        x1 = paddle_center_x - self.ball_radius
        y1 = paddle_coords[1] - 2 * self.ball_radius - 2
        x2 = paddle_center_x + self.ball_radius
        y2 = paddle_coords[1] - 2
        self.canvas.coords(self.ball, x1, y1, x2, y2)

    def on_key_press(self, event):
        if event.keysym == "Left":
            self.paddle_dx = -self.paddle_speed
        elif event.keysym == "Right":
            self.paddle_dx = self.paddle_speed

    def on_key_release(self, event):
        # Keep moving only if the released key matches current direction.
        if event.keysym == "Left" and self.paddle_dx < 0:
            self.paddle_dx = 0
        elif event.keysym == "Right" and self.paddle_dx > 0:
            self.paddle_dx = 0

    def on_space(self, _event):
        if not self.game_running:
            self.restart_game()

    def restart_game(self):
        self.score = 0
        self.lives = 3
        self.game_running = True
        self.ball_dx = random.choice([-1, 1]) * self.ball_speed
        self.ball_dy = -self.ball_speed
        self.canvas.itemconfigure(self.score_text, text="Score: 0")
        self.canvas.itemconfigure(self.lives_text, text="Lives: 3")
        self.canvas.coords(
            self.paddle,
            (self.width - self.paddle_width) / 2,
            self.height - 40,
            (self.width + self.paddle_width) / 2,
            self.height - 40 + self.paddle_height,
        )
        self.reset_ball_position()
        self.create_bricks(rows=6, cols=10)
        if self.message_item:
            self.canvas.delete(self.message_item)
            self.message_item = None

    def show_message(self, text, color="#f8fafc"):
        if self.message_item:
            self.canvas.delete(self.message_item)
        self.message_item = self.canvas.create_text(
            self.width / 2,
            self.height / 2,
            fill=color,
            font=("Consolas", 24, "bold"),
            text=text,
            justify="center",
        )

    def move_paddle(self):
        self.canvas.move(self.paddle, self.paddle_dx, 0)
        x1, y1, x2, y2 = self.canvas.coords(self.paddle)

        if x1 < 0:
            self.canvas.move(self.paddle, -x1, 0)
        elif x2 > self.width:
            self.canvas.move(self.paddle, self.width - x2, 0)

    def move_ball(self):
        self.canvas.move(self.ball, self.ball_dx, self.ball_dy)
        x1, y1, x2, y2 = self.canvas.coords(self.ball)

        if x1 <= 0 or x2 >= self.width:
            self.ball_dx *= -1
        if y1 <= 0:
            self.ball_dy *= -1

        if y2 >= self.height:
            self.lives -= 1
            self.canvas.itemconfigure(self.lives_text, text=f"Lives: {self.lives}")
            if self.lives <= 0:
                self.game_running = False
                self.show_message("Game Over\nPress Space to Restart", color="#f87171")
            else:
                self.ball_dx = random.choice([-1, 1]) * self.ball_speed
                self.ball_dy = -self.ball_speed
                self.reset_ball_position()

    def check_collisions(self):
        ball_coords = self.canvas.coords(self.ball)
        overlapping = self.canvas.find_overlapping(*ball_coords)

        if self.paddle in overlapping:
            self.handle_paddle_bounce()

        for brick in list(self.bricks):
            if brick in overlapping:
                self.bricks.remove(brick)
                self.canvas.delete(brick)
                self.ball_dy *= -1
                self.score += 10
                self.canvas.itemconfigure(self.score_text, text=f"Score: {self.score}")
                break

        if not self.bricks and self.game_running:
            self.game_running = False
            self.show_message("You Win!\nPress Space to Play Again", color="#34d399")

    def handle_paddle_bounce(self):
        paddle_x1, _, paddle_x2, _ = self.canvas.coords(self.paddle)
        ball_x1, _, ball_x2, _ = self.canvas.coords(self.ball)
        paddle_center = (paddle_x1 + paddle_x2) / 2
        ball_center = (ball_x1 + ball_x2) / 2

        # Change horizontal speed by hit position for better control.
        relative_intersect = (ball_center - paddle_center) / (self.paddle_width / 2)
        self.ball_dx = relative_intersect * (self.ball_speed + 2)
        self.ball_dy = -abs(self.ball_dy)

    def game_loop(self):
        if self.game_running:
            self.move_paddle()
            self.move_ball()
            self.check_collisions()

        self.root.after(16, self.game_loop)


def main():
    root = tk.Tk()
    game = BrickBreakerGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
