import random

RIGHT = (0, 1)
LEFT = (0, -1)
UP = (-1, 0)
DOWN = (1, 0)


class Snake:
    def __init__(self, init_body, init_direction):
        self.body = init_body
        self.direction = init_direction

    def take_step(self, position):
        self.body = [position] + self.body[:-1]

    def extend(self):
        self.body.append(self.get_head())

    def set_direction(self, direction):
        self.direction = direction

    def get_head(self):
        return self.body[0]


class Apple:
    def __init__(self, height, width):
        self.position = (random.randint(0, height - 1), random.randint(0, width - 1))


class Game:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.snake = Snake([(self.height / 2, self.width / 2)], None)
        self.apple = Apple(height, width)
        self.score = 0

    def play(self):
        while True:
            self.render_board()
            self.get_input()
            self.make_move()

    def get_input(self):
        move = raw_input().capitalize()
        if move == "W" and self.snake.direction != DOWN:
            self.snake.direction = UP
        elif move == "A" and self.snake.direction != RIGHT:
            self.snake.direction = LEFT
        elif move == "S" and self.snake.direction != UP:
            self.snake.direction = DOWN
        elif move == "D" and self.snake.direction != LEFT:
            self.snake.direction = RIGHT

    def make_move(self):
        new_pos = tuple(map(sum, zip(self.snake.get_head(), self.snake.direction)))

        # death by itself
        if new_pos in self.snake.body:
            print(
                "You ate yourself - GAME OVER! \nFinal Score: " + str(self.score) + "\n"
            )
            quit()

        # death by bounds - TODO: add wrapping?
        elif (
            new_pos[0] < 0
            or new_pos[0] >= self.height
            or new_pos[1] < 0
            or new_pos[1] >= self.width
        ):
            print(
                "You ran out of bounds - GAME OVER! \nFinal Score: "
                + str(self.score)
                + "\n"
            )
            quit()

        # eat apple
        elif new_pos == self.apple.position:
            del self.apple
            self.snake.extend()
            self.snake.take_step(new_pos)
            self.score += 1
            self.apple = Apple(self.height, self.width)

        # normal step
        else:
            self.snake.take_step(new_pos)

    def render_board(self):
        matrix = self.board_matrix()
        snake_matrix = self.add_snake_to_matrix(matrix)
        apple_pos = self.apple.position
        horizontal_boarders = "+" + "-" * self.width + "+"
        print(horizontal_boarders)
        matrix[apple_pos[0]][apple_pos[1]] = "A"
        for row in snake_matrix:
            line = ""
            for r in row:
                if r is None:
                    line += " "
                else:
                    line += r
            print("|" + line + "|")
        print(horizontal_boarders)

    def add_snake_to_matrix(self, matrix):
        (xhead, yhead), positions = self.snake.get_head(), self.snake.body[1:]
        matrix[xhead][yhead] = "X"
        for x, y in positions:
            matrix[x][y] = "O"
        return matrix

    def board_matrix(self):
        return [[None for _ in range(self.width)] for _ in range(self.height)]


game = Game(15, 25)
game.play()
