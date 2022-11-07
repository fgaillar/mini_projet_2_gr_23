import random

board = [[0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0]]
bricks = [[9, 9], [9, 0]], [[9, 9], [0, 9]], [[9, 9], [9, 9]], [[9, 9], [0, 0]], [[9, 0], [0, 0]]
brick = random.choice(bricks)
print(brick)

for x in range(len(brick)):
    for y in range(len(brick)):
        board[x][y] += brick[x][y]
print(board)