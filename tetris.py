import curses
import random
import time

BOARD_WIDTH = 10
BOARD_HEIGHT = 20
TICK_RATE = 0.5  # seconds per tick

# Define shapes with rotation states
SHAPES = {
    'I': [
        [[1, 1, 1, 1]],
        [[1], [1], [1], [1]],
    ],
    'O': [
        [[1, 1],
         [1, 1]],
    ],
    'T': [
        [[0, 1, 0],
         [1, 1, 1]],
        [[1, 0],
         [1, 1],
         [1, 0]],
        [[1, 1, 1],
         [0, 1, 0]],
        [[0, 1],
         [1, 1],
         [0, 1]],
    ],
    'S': [
        [[0, 1, 1],
         [1, 1, 0]],
        [[1, 0],
         [1, 1],
         [0, 1]],
    ],
    'Z': [
        [[1, 1, 0],
         [0, 1, 1]],
        [[0, 1],
         [1, 1],
         [1, 0]],
    ],
    'J': [
        [[1, 0, 0],
         [1, 1, 1]],
        [[1, 1],
         [1, 0],
         [1, 0]],
        [[1, 1, 1],
         [0, 0, 1]],
        [[0, 1],
         [0, 1],
         [1, 1]],
    ],
    'L': [
        [[0, 0, 1],
         [1, 1, 1]],
        [[1, 0],
         [1, 0],
         [1, 1]],
        [[1, 1, 1],
         [1, 0, 0]],
        [[1, 1],
         [0, 1],
         [0, 1]],
    ],
}
SHAPE_KEYS = list(SHAPES.keys())


def create_board():
    return [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]


class Piece:
    def __init__(self, shape_key):
        self.shape_key = shape_key
        self.rotations = SHAPES[shape_key]
        self.rotation = 0
        self.shape = self.rotations[self.rotation]
        self.x = BOARD_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self, board):
        new_rotation = (self.rotation + 1) % len(self.rotations)
        new_shape = self.rotations[new_rotation]
        if not self._collision(board, self.x, self.y, new_shape):
            self.rotation = new_rotation
            self.shape = new_shape

    def move(self, board, dx, dy):
        if not self._collision(board, self.x + dx, self.y + dy, self.shape):
            self.x += dx
            self.y += dy
            return True
        return False

    def drop(self, board):
        while self.move(board, 0, 1):
            pass

    def _collision(self, board, x, y, shape):
        for cy, row in enumerate(shape):
            for cx, cell in enumerate(row):
                if cell:
                    board_x = x + cx
                    board_y = y + cy
                    if board_x < 0 or board_x >= BOARD_WIDTH or board_y >= BOARD_HEIGHT:
                        return True
                    if board_y >= 0 and board[board_y][board_x]:
                        return True
        return False

    def merge(self, board):
        for cy, row in enumerate(self.shape):
            for cx, cell in enumerate(row):
                if cell:
                    board_y = self.y + cy
                    board_x = self.x + cx
                    if 0 <= board_y < BOARD_HEIGHT and 0 <= board_x < BOARD_WIDTH:
                        board[board_y][board_x] = 1


def clear_lines(board):
    new_board = [row for row in board if any(cell == 0 for cell in row)]
    cleared = BOARD_HEIGHT - len(new_board)
    while len(new_board) < BOARD_HEIGHT:
        new_board.insert(0, [0 for _ in range(BOARD_WIDTH)])
    return new_board, cleared


def draw_board(stdscr, board, piece):
    stdscr.clear()
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell:
                stdscr.addstr(y, x * 2, '[]')
            else:
                stdscr.addstr(y, x * 2, '  ')
    # draw current piece
    for cy, prow in enumerate(piece.shape):
        for cx, cell in enumerate(prow):
            if cell:
                y = piece.y + cy
                x = (piece.x + cx) * 2
                if y >= 0:
                    stdscr.addstr(y, x, '[]')
    stdscr.refresh()


def tetris(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    board = create_board()
    piece = Piece(random.choice(SHAPE_KEYS))
    last_tick = time.time()
    score = 0

    while True:
        now = time.time()
        if now - last_tick > TICK_RATE:
            moved = piece.move(board, 0, 1)
            if not moved:
                piece.merge(board)
                board, cleared = clear_lines(board)
                score += cleared
                piece = Piece(random.choice(SHAPE_KEYS))
                if piece._collision(board, piece.x, piece.y, piece.shape):
                    break  # game over
            last_tick = now

        draw_board(stdscr, board, piece)
        stdscr.addstr(0, BOARD_WIDTH * 2 + 2, f"Score: {score}")
        stdscr.refresh()
        key = stdscr.getch()
        if key == curses.KEY_LEFT:
            piece.move(board, -1, 0)
        elif key == curses.KEY_RIGHT:
            piece.move(board, 1, 0)
        elif key == curses.KEY_DOWN:
            piece.move(board, 0, 1)
        elif key == curses.KEY_UP:
            piece.rotate(board)
        elif key == ord(' '):
            piece.drop(board)
        elif key == ord('q'):
            break
        time.sleep(0.01)

    stdscr.nodelay(False)
    stdscr.addstr(BOARD_HEIGHT // 2, BOARD_WIDTH - 4, 'Game Over')
    stdscr.addstr(BOARD_HEIGHT // 2 + 1, BOARD_WIDTH - 5, f'Score: {score}')
    stdscr.addstr(BOARD_HEIGHT // 2 + 2, BOARD_WIDTH - 8, 'Press any key')
    stdscr.getch()


def main():
    curses.wrapper(tetris)


if __name__ == '__main__':
    main()
