import curses
import time
import random

# Game setup
PADDLE_HEIGHT = 4
BALL_CHAR = 'O'
PADDLE_CHAR = '|'
BLANK_CHAR = ' '

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)

    sh, sw = stdscr.getmaxyx()
    ball_y, ball_x = sh//2, sw//2
    ball_dir_y = random.choice([-1, 1])
    ball_dir_x = random.choice([-1, 1])

    paddle1_y = paddle2_y = sh//2 - PADDLE_HEIGHT//2
    paddle_x_offset = 3

    score1, score2 = 0, 0

    while True:
        stdscr.clear()

        # Draw paddles
        for i in range(PADDLE_HEIGHT):
            stdscr.addch(paddle1_y + i, paddle_x_offset, PADDLE_CHAR)
            stdscr.addch(paddle2_y + i, sw - paddle_x_offset, PADDLE_CHAR)

        # Draw ball
        stdscr.addch(ball_y, ball_x, BALL_CHAR)

        # Scoreboard
        score_text = f'{score1} | {score2}'
        stdscr.addstr(1, sw//2 - len(score_text)//2, score_text)

        stdscr.refresh()

        # Input handling
        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == curses.KEY_UP:
            paddle2_y = max(paddle2_y - 1, 0)
        elif key == curses.KEY_DOWN:
            paddle2_y = min(paddle2_y + 1, sh - PADDLE_HEIGHT)
        elif key == ord('w'):
            paddle1_y = max(paddle1_y - 1, 0)
        elif key == ord('s'):
            paddle1_y = min(paddle1_y + 1, sh - PADDLE_HEIGHT)

        # Ball movement
        ball_y += ball_dir_y
        ball_x += ball_dir_x

        # Bounce off top/bottom
        if ball_y <= 0 or ball_y >= sh - 1:
            ball_dir_y *= -1

        # Paddle collision
        if ball_x == paddle_x_offset + 1:
            if paddle1_y <= ball_y <= paddle1_y + PADDLE_HEIGHT:
                ball_dir_x *= -1
        elif ball_x == sw - paddle_x_offset - 1:
            if paddle2_y <= ball_y <= paddle2_y + PADDLE_HEIGHT:
                ball_dir_x *= -1

        # Score check
        if ball_x <= 0:
            score2 += 1
            ball_y, ball_x = sh//2, sw//2
            ball_dir_x = 1
        elif ball_x >= sw - 1:
            score1 += 1
            ball_y, ball_x = sh//2, sw//2
            ball_dir_x = -1

        time.sleep(0.05)

if __name__ == "__main__":
    curses.wrapper(main)
