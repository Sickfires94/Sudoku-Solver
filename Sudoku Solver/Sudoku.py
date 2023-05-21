from math import sqrt


class sudoku:

# Initializes the game and keeps track of numbers placed and maintains consistency for other boxes

    def __init__(self, grid):
        self.grid = grid
        self.move = 0
        self.box_size = int(sqrt(len(self.grid)))  # sqrt(len(self.grid) + 1) finds the size of the box
        self.size = len(self.grid)
          # Heuristic
        self.solved  = False

        check_rows = [[False for i in range(len(grid))] for j in range(len(grid))]
        check_cols = [[False for i in range(len(grid))] for j in range(len(grid))]
        check_boxes = [[False for i in range(len(grid))] for j in range(len(grid))]
        self.no_of_nums = [9 for i in range(9)]              # keeps track of how many digits left to place
        for row in range(len(grid)):
            for col in range(len(grid)):
                if grid[row][col] == 0:
                    continue
                check_rows[row][grid[row][col] - 1] = True  # grid[row][col] - 1 to map --> number = 1 to index = 0
                check_cols[col][grid[row][col] - 1] = True  # number = 9 to index = 8
                check_boxes[self.findBox(row, col)][
                    grid[row][col] - 1] = True
                self.no_of_nums[grid[row][col] - 1] -= 1         # -1 to map --> number = 1 to index = 0
                                                    # keeps track of how many more numbers to place
        self.check_buddy = [check_rows, check_cols, check_boxes]
        self.score = self.heuristic()

# Checks if the game is completed

    def checkComplete(self):
        for checks in self.check_buddy:
            for list in checks:
                for nums in list:
                    if nums == False:
                        return False
        print("Completed!!!!")
        return True

    def findBox(self, row, col):
        return int(int(row / self.box_size) * self.box_size + col / self.box_size)

# Places a number in the specified position if possible

    def make_move(self, num, row, col):

        if not self.possibleMove(num - 1, row, col):
            print("Invalid Move: num = ", num , " pos = ", row, ", ", col)
            return

        self.score = self.heuristic()
        self.check_buddy[0][row][num - 1] = True
        self.check_buddy[1][col][num - 1] = True
        self.check_buddy[2][self.findBox(row, col)][num - 1] = True

        self.grid[row][col] = num
        self.move += 1
        self.score = self.heuristic()
        self.solved = self.checkComplete()

# Clears the number in a cell

    def undo_move(self, row, col):
        num = self.grid[row][col]

        self.check_buddy[0][row][num - 1] = False
        self.check_buddy[1][col][num - 1] = False
        self.check_buddy[2][self.findBox(row, col)][num - 1] = False

        self.move -= 1
        self.grid[row][col] = 0

# prints the grid

    def print_grid(self):
        for row in range(self.size):
            if (row % self.box_size == 0):
                print("-----------------------------------")

            line = ""
            for col in range(self.size):
                if (col % self.box_size == 0):
                    line += " |"
                line += " " + str(self.grid[row][col])

            print(line)


# Returns the number of completed and almost completed (1 less) rows + cols + boxes

    def heuristic(self):
        score = 27

        # TODO think of a way to first fill boxes with least amount of options


        for i in self.check_buddy[0]:
            buffer = True
            for j in i:
                if j:
                    continue
                if buffer:
                    buffer = False
                score -= 1
                break

        for i in self.check_buddy[1]:
            buffer = True
            buffer2 = True
            for j in i:
                if j:
                    continue
                if buffer:
                    buffer = False
                score -= 1
                break


        for i in self.check_buddy[2]:
            buffer = True
            buffer2 = True
            for j in i:
                if j:
                    continue
                if buffer:
                    buffer = False
                score -= 1
                break

        return score + self.move/18

# Checks if every cell can have atleast 1 number

    def checkConsistency(self):
        for row in range(len(self.grid)):
            for col in range(len(self.grid)):
                consistent = False
                for i in range(len(self.grid)):
                    if self.grid[row][col] != 0:
                        consistent = True
                        break
                    if not self.check_buddy[0][row][i] and not self.check_buddy[1][col][i] and not self.check_buddy[2][self.findBox(row, col)][i]:
                        consistent = True
                        break

                if not consistent:
                    return False

        return True

# Checks if there exists a number that has been placed 8 times (in a 9x9)

    def checkForcedNum(self):
        for i in range(len(self.no_of_nums)):
            if(self.no_of_nums == 1):
                return i
        return -1

# Checks if a certain move is playable

    def possibleMove(self, num, row, col):
        if self.grid[row][col] != 0:
            return False
        box = self.findBox(row, col)
        return not self.check_buddy[0][row][num] and not self.check_buddy[1][col][num] and not self.check_buddy[2][box][num]


