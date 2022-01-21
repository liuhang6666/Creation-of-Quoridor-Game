import math
import pprint
import copy


class QuoridorGame:
    """"""
    def __init__(self):
        self.fence1 = [[0] * 9 for i in range(9)]
        self.fence2 = [[0] * 9 for i in range(9)]
        self.piece = [[0] * 9 for i in range(9)]
        self.piece[4][0] = 1
        self.piece[4][8] = 2
        self.winner = 0
        self.num = [0, 10, 10]
        self.current = 1
        self.player = [(), (4, 0), (4, 8)]
        self.dir = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1), (0, 2), (0, -2)]

    def checkValid(self, id, location):
        if self.winner != 0:
            return False
        if location[0] < 0 or location[0] > 8 or location[1] < 0 or location[1] > 8:
            return False
        if self.current != id:
            return False
        return True

    def checkDiagonal(self, id, location, x, y):
        x1 = self.player[id][0]
        y1 = self.player[id][1]
        flag = False
        if y1 - 2 >= 0 and self.fence2[x1][y1 - 1] != 0:
            flag = True
        if y1 + 2 <= 8 and self.fence2[x1][y1 + 2] != 0:
            flag = True
        if not flag:
            return False
        if y == 1 and self.player[id][1] + 1 != self.player[3 - id][1]:
            return False
        if y == -1 and self.player[id][1] - 1 != self.player[3 - id][1]:
            return False
        if x == -1 and self.fence1[self.player[id][0]][self.player[3 - id][1]] != 0:
            return False
        if x == 1 and self.fence1[self.player[id][0] + 1][self.player[3 - id][1]] != 0:
            return False
        return True

    def checkNotUpDownLeftRight(self, id, location, x, y):
        if self.player[1][0] != self.player[2][0] or int(math.fabs(self.player[2][1] - self.player[1][1])) != 1:
            return False
        y1 = max(self.player[2][1], self.player[1][1])
        if self.fence2[self.player[2][0]][y1] != 0:
            return False
        if x == 0 and y == 2:
            if self.fence2[location[0]][location[1]] != 0:
                return False
        elif x == 0 and y == -2:
            if self.fence2[location[0]][location[1] - 1] != 0:
                return False
        else:
            if not self.checkDiagonal(id, location, x, y):
                return False
        return True

    def checkMove(self, id, location, x, y):
        if x == 1 and y == 0:
            if self.fence1[location[0]][location[1]] != 0:
                return False
        elif x == -1 and y == 0:
            if self.fence1[self.player[id][0]][self.player[id][1]] != 0:
                return False
        elif x == 0 and y == 1:
            if self.fence2[location[0]][location[1]] != 0:
                return False
        elif x == 0 and y == -1:
            if self.fence2[self.player[id][0]][self.player[id][1]] != 0:
                return False
        else:
            if not self.checkNotUpDownLeftRight(id, location, x, y):
                return False
        return True

    def move_pawn(self, id, location):
        if not self.checkValid(id, location):
            return False
        x = location[0] - self.player[id][0]
        y = location[1] - self.player[id][1]
        if not self.checkMove(id, location, x, y):
            return False
        if (x, y) not in self.dir:
            return False
        self.current = 3 - id
        self.piece[location[0]][location[1]] = id
        self.player[id] = (location[0], location[1])
        if id == 1 and location[1] == 8:
            self.winner = 1
        elif id == 2 and location[1] == 0:
            self.winner = 2
        return True

    def place_fence(self, id, c, location):
        if not self.checkValid(id, location):
            return False
        if c == 'v' and self.fence1[location[0]][location[1]] != 0:
            return False
        if c == 'h' and self.fence2[location[0]][location[1]] != 0:
            return False
        if self.num[id] == 0:
            return False
        self.num[id] -= 1
        self.current = 3 - id
        if c == 'v':
            self.fence1[location[0]][location[1]] = id
        else:
            self.fence2[location[0]][location[1]] = id
        return True

    def is_winner(self, id):
        if self.winner == id:
            return True
        else:
            return False


if __name__ == '__main__':
    q = QuoridorGame()
    print(q.move_pawn(1, (4, 1)))  # moves the Player2 pawn -- invalid move because only Player1 can start, returns False
    print(q.move_pawn(2, (5, 8)))
    print(q.place_fence(1, "h", (5, 8)))
    print(q.place_fence(2, "h", (5, 8)))
