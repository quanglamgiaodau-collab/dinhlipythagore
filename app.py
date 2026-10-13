import random
import tkinter as tk

# Các thông số cơ bản của trò chơi
WIDTH = 600
HEIGHT = 400
SPEED = 100  # Tốc độ di chuyển (mili-giây), số càng nhỏ rắn chạy càng nhanh
SPACE_SIZE = 20
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"  # Màu xanh lá cho rắn
FOOD_COLOR = "#FF0000"  # Màu đỏ cho mồi
BACKGROUND_COLOR = "#000000"  # Màu đen cho nền


class Snake:

  def __init__(self):
    self.body_size = BODY_PARTS
    self.coordinates = []
    self.squares = []

    for i in range(BODY_PARTS):
      self.coordinates.append([100 - (i * SPACE_SIZE), 100])

    for x, y in self.coordinates:
      square = canvas.create_rectangle(
          x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake"
      )
      self.squares.append(square)


class Food:

  def __init__(self):
    x = random.randint(0, (WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
    y = random.randint(0, (HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE

    self.coordinates = [x, y]
    canvas.create_oval(
        x,
        y,
        x + SPACE_SIZE,
        y + SPACE_SIZE,
        fill=FOOD_COLOR,
        tag="food",
    )


def next_turn(snake, food):
  x, y = snake.coordinates[0]

  if direction == "up":
    y -= SPACE_SIZE
  elif direction == "down":
    y += SPACE_SIZE
  elif direction == "left":
    x -= SPACE_SIZE
  elif direction == "right":
    x += SPACE_SIZE

  # Thêm đầu mới cho rắn
  snake.coordinates.insert(0, [x, y])
  square = canvas.create_rectangle(
      x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR
  )
  snake.squares.insert(0, square)

  # Kiểm tra xem rắn có ăn mồi không
  if x == food.coordinates[0] and y == food.coordinates[1]:
    global score
    score += 1
    label.config(text=f"Điểm: {score}")
    canvas.delete("food")
    food = Food()
  else:
    # Xóa khúc đuôi cuối cùng nếu không ăn mồi để giữ nguyên độ dài
    del snake.coordinates[-1]
    canvas.delete(snake.squares[-1])
    del snake.squares[-1]

  if check_game_over(snake):
    game_over()
  else:
    window.after(SPEED, next_turn, snake, food)


def change_direction(new_direction):
  global direction

  if new_direction == "left":
    if direction != "right":
      direction = new_direction
  elif new_direction == "right":
    if direction != "left":
      direction = new_direction
  elif new_direction == "up":
    if direction != "down":
      direction = new_direction
  elif new_direction == "down":
    if direction != "up":
      direction = new_direction


def check_game_over(snake):
  x, y = snake.coordinates[0]

  # Kiểm tra chạm tường
  if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
    return True

  # Kiểm tra tự cắn đuôi
  for body_part in snake.coordinates[1:]:
    if x == body_part[0] and y == body_part[1]:
      return True

  return False


def game_over():
  canvas.delete(tk.ALL)
  canvas.create_text(
      WIDTH / 2,
      HEIGHT / 2,
      font=("consolas", 70),
      text="THUA RỒI!",
      fill="red",
      tag="gameover",
  )


# Khởi tạo cửa sổ trò chơi
window = tk.Tk()
window.title("Trò chơi Con Rắn - Python")
window.resizable(False, False)

score = 0
direction = "right"

label = tk.Label(window, text=f"Điểm: {score}", font=("consolas", 20))
label.pack()

canvas = tk.Canvas(
    window, bg=BACKGROUND_COLOR, height=HEIGHT, width=WIDTH
)
canvas.pack()

window.update()

# Căn giữa cửa sổ trên màn hình
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Bắt sự kiện bàn phím (Phím mũi tên)
window.bind("<Left>", lambda event: change_direction("left"))
window.bind("<Right>", lambda event: change_direction("right"))
window.bind("<Up>", lambda event: change_direction("up"))
window.bind("<Down>", lambda event: change_direction("down"))

# Khởi chạy rắn và mồi
snake = Snake()
food = Food()
window.after(SPEED, next_turn, snake, food)

window.mainloop()
