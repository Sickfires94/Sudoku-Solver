import copy

from Sudoku import sudoku
from copy import deepcopy


class solver:
    def __init__(self, game: sudoku):
        self.game = game



    # Solving using CSP and A* Search

    def make_forced_moves(self, game : sudoku):     # checks and fills if a box can only fill one number

        if self.single_remaining(game):
            return True
        print(" no remaining")
        if self.single_option(game):
            return True

        print(" no option")
        if self.single_place(game):
            return True

        print(" no place")
        return False



# Checks if a number has been placed 8 times and only need to place one more of that number in a forced position

    def single_remaining(self, game : sudoku):
        forced_num = game.checkForcedNum()

        if(forced_num != -1):
            print("forced num")
            for row in range(game.size):
                if(game.check_buddy[0][row][forced_num]):
                    continue

                for col in range(game.size):
                    if(game.check_buddy[1][col][forced_num]):
                        continue
                    game.make_move(forced_num + 1, row, col )
                    print("move  = ", forced_num + 1, ", ", row, ", ", col)
                    return True
        return False


# Checks if a cell can only one number

    def single_option(self, game : sudoku):
        for row in range(game.size):
            for col in range(game.size):
                if(game.grid[row][col] == 0):
                    nums = []

                    for num in range(game.size):
                        if game.possibleMove(num, row, col):
                            nums.append(num + 1)
                    if len(nums) == 1:
                        num = nums[0]
                        game.make_move(nums.pop(), row, col)
                        print("move  = ", num, ", ", row, ", ", col)
                        return True

        return False



# Checks if a number can only come in one cell in a box/row/col

    def single_place(self, game : sudoku):
        for num in range(game.size):
            for row in range(game.size):
                if(game.check_buddy[0][num]):
                    continue
                moves = []
                for pos in range(game.size):
                    if game.possibleMove(num, row, pos):
                        moves.append(pos)
                if len(moves) == 1:
                    game.make_move(num + 1, row, moves.pop())
                    return True

            for col in range(game.size):
                if(game.check_buddy[1][num]):
                    continue
                moves = []
                for pos in range(game.size):
                    if game.possibleMove(num, pos, col):
                        moves.append(pos)
                if len(moves) == 1:
                    game.make_move(num + 1, moves.pop(), col)
                    return True

            for box in range(game.size):
                if(game.check_buddy[2][box][num]):
                    continue

                row_increment = int(box / game.box_size) * game.box_size
                col_increment = (box % game.box_size) * game.box_size

                moves = []
                for row in range(row_increment, game.box_size + row_increment):
                    for col in range(col_increment, game.box_size + col_increment):
                        if game.possibleMove(num, row, col):
                            moves.append([row, col])

                if len(moves) == 1:
                    game.make_move(num + 1, moves[0][0], moves[0][1])
                    return True

        return False






    # Solving using CSP and A* Search

    def A_Star_Search(self):
        states = [self.game]   # queue of states
        solved = False
        solution = self.game



        while len(states) != 0 and not solved:
            current = states.pop(0)
            print("************** MOVE ", current.move, " *********************")
            current.print_grid()



            while self.make_forced_moves(current):
                print("******* Made forced move ************* ")


                pass

            print("************ After forced ************")
            current.print_grid()
            if current.solved:
                solution = current
                break

            for row in range(len(current.grid)):
                for col in range(current.size):
                    if current.grid[row][col] != 0:
                        continue
                    for num in range(current.size):
                        if current.possibleMove(num, row, col):
                            next_state = copy.deepcopy(current)
                            next_state.make_move(num + 1, row, col)
                            if not next_state.checkConsistency():
                                continue
                            if next_state.solved:
                                solution = next_state
                                solved = True
                                break

                            if len(states) == 0:
                                states.append(next_state)
                            for i in range(len(states)):
                                if states[i].score < next_state.score:
                                    states.insert(i, next_state)
                                    break
                            else:
                                states.append(next_state)


        print("************** GAME COMPLETED *****************")
        print("***************** SOLUTION ********************")
        solution.print_grid()

        print("\n*************** Moves = ", solution.move, "  ******************\n")




