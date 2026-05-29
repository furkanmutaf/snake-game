import curses
import random
import time

# ayarlar

WIDTH = 60
HEIGHT = 20

SNAKE_CHAR = "#"
FOOD_CHAR = "*"

INITIAL_SPEED = 0.12


# yardımcı

def create_food(snake):

    while True:

        food = (
            random.randint(1, WIDTH - 2),
            random.randint(1, HEIGHT - 2)
        )

        if food not in snake:
            return food


def draw_border(window):
    window.border()


def draw_food(window, food):

    x, y = food

    try:
        window.addstr(y, x, FOOD_CHAR)

    except curses.error:
        pass


def draw_snake(window, snake):

    for segment in snake:

        x, y = segment

        try:
            window.addstr(y, x, SNAKE_CHAR)

        except curses.error:
            pass


def show_score(window, score):

    text = f" Score: {score} "

    window.addstr(0, 2, text)


def show_game_over(window, score):

    window.clear()

    message_1 = "GAME OVER"
    message_2 = f"Final Score: {score}"
    message_3 = "Press Q to quit"

    center_x = WIDTH // 2

    window.addstr(
        HEIGHT // 2 - 1,
        center_x - len(message_1) // 2,
        message_1
    )

    window.addstr(
        HEIGHT // 2,
        center_x - len(message_2) // 2,
        message_2
    )

    window.addstr(
        HEIGHT // 2 + 1,
        center_x - len(message_3) // 2,
        message_3
    )

    window.refresh()

    while True:

        key = window.getch()

        if key in [ord("q"), ord("Q")]:
            break


# yönlendirme

def move_snake(snake, direction):

    head_x, head_y = snake[0]

    if direction == "UP":

        new_head = (head_x, head_y - 1)

    elif direction == "DOWN":

        new_head = (head_x, head_y + 1)

    elif direction == "LEFT":

        new_head = (head_x - 1, head_y)

    else:

        new_head = (head_x + 1, head_y)

    snake.insert(0, new_head)

    return new_head


def remove_tail(snake):

    snake.pop()


def check_collision(snake):

    head_x, head_y = snake[0]

    # duvara çarpma

    if head_x == 0 or head_x == WIDTH - 1:
        return True

    if head_y == 0 or head_y == HEIGHT - 1:
        return True

    # kendine çarpma

    if snake[0] in snake[1:]:
        return True

    return False


def change_direction(key, current_direction):

    if key == curses.KEY_UP and current_direction != "DOWN":
        return "UP"

    elif key == curses.KEY_DOWN and current_direction != "UP":
        return "DOWN"

    elif key == curses.KEY_LEFT and current_direction != "RIGHT":
        return "LEFT"

    elif key == curses.KEY_RIGHT and current_direction != "LEFT":
        return "RIGHT"

    return current_direction


# ana oyun

def main(window):

    curses.curs_set(0)

    window.nodelay(True)

    window.timeout(100)

    # başlangıç yılanı

    snake = [
        (WIDTH // 2, HEIGHT // 2),
        (WIDTH // 2 - 1, HEIGHT // 2),
        (WIDTH // 2 - 2, HEIGHT // 2)
    ]

    direction = "RIGHT"

    food = create_food(snake)

    score = 0

    speed = INITIAL_SPEED

    while True:

        window.clear()

        draw_border(window)

        draw_food(window, food)

        draw_snake(window, snake)

        show_score(window, score)

        window.refresh()

        # tuş alma

        key = window.getch()

        if key in [ord("q"), ord("Q")]:
            break

        direction = change_direction(key, direction)

        # hareket

        new_head = move_snake(snake, direction)

        # yemek yeme

        if new_head == food:

            score += 1

            food = create_food(snake)

            # hız artır

            speed *= 0.95

            if speed < 0.03:
                speed = 0.03

        else:

            remove_tail(snake)

        # çarpışma kontrolü

        if check_collision(snake):
            break

        time.sleep(speed)

    show_game_over(window, score)


# başlat

curses.wrapper(main)