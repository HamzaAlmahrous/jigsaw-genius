import numpy as np

# Piece class, holds data of each piece
class Piece:
    def __init__(self, num, s_vert, s_horz, chn, start, data, total):
        self.pieceNum = num
        self.size_vertical = s_vert
        self.size_horizontal = s_horz
        self.pieceChn = chn
        self.pieceStart = start
        self.pieceData = np.ndarray((s_vert, s_horz, chn), buffer=data, dtype=np.uint8)
        self.pieceTotal = total

        # the 4 borders of the piece
        self.sideUp = []
        self.sideRight = []
        self.sideDown = []
        self.sideLeft = []

        for i in range(self.size_horizontal):
            self.sideUp.append(self.pieceData[0][i])
            self.sideDown.append(self.pieceData[-1][i])

        for i in range(self.size_vertical):
            self.sideRight.append(self.pieceData[i][-1])
            self.sideLeft.append(self.pieceData[i][0])

        self.sides = [self.sideUp, self.sideRight, self.sideDown, self.sideLeft]

        self.difference = [None for x in range(total)]

        self.neighbors = [None for x in range(4)]

        self.differences = [None for x in range(4)]

def calculate_difference(side1, side2):
    diff = 0
    for i in range(len(side1)):
        for j in range(len(side1[i])):
            diff += abs(int(side1[i][j]) - int(side2[i][j]))
    return diff

def find_neighbors(pieces):
    for piece in pieces:
        min_diffs = [float('inf')] * 4
        best_neighbors = [None] * 4
        best_differences = [None] * 4

        for other_piece in pieces:
            if piece.pieceNum == other_piece.pieceNum:
                continue

            for i, side in enumerate(piece.sides):
                other_side = other_piece.sides[(i + 2) % 4]  # Opposite side
                diff = calculate_difference(side, other_side)
                
                if diff < min_diffs[i]:
                    min_diffs[i] = diff
                    best_neighbors[i] = other_piece.pieceNum
                    best_differences[i] = diff

        piece.neighbors = best_neighbors
        piece.differences = best_differences


#find the start piece
#___________________________________________________________________

def find_up_left_piece(pieces):
    index = -1
    max_difference = -1
    for i, piece in enumerate(pieces):
        current_difference = piece.differences[0] + piece.differences[3]
        if current_difference > max_difference:
            index = i
            max_difference = current_difference
    return "UL", index, max_difference

def find_up_right_piece(pieces):
    index = -1
    max_difference = -1
    for i, piece in enumerate(pieces):
        current_difference = piece.differences[0] + piece.differences[1]
        if current_difference > max_difference:
            index = i
            max_difference = current_difference
    return "UR", index, max_difference

def find_down_right_piece(pieces):
    index = -1
    max_difference = -1
    for i, piece in enumerate(pieces):
        current_difference = piece.differences[2] + piece.differences[1]
        if current_difference > max_difference:
            index = i
            max_difference = current_difference
    return "DR", index, max_difference

def find_down_left_piece(pieces):
    index = -1
    max_difference = -1
    for i, piece in enumerate(pieces):
        current_difference = piece.differences[2] + piece.differences[3]
        if current_difference > max_difference:
            index = i
            max_difference = current_difference
    return "DL", index, max_difference

#___________________________________________________________________


def find_starting_piece(pieces, piece, rows, cols):
    starting_piece = piece[1]
    if piece[0] == "DL":
        x = rows - 1
        while x != 0:
            starting_piece = pieces[starting_piece].neighbors[0]
            x -= 1

    elif piece[0] == "DR":
        x = rows - 1
        y = cols - 1
        while x != 0:
            starting_piece = pieces[starting_piece].neighbors[0]
            x -= 1

        while y != 0:
            starting_piece = pieces[starting_piece].neighbors[3]
            y -= 1

    # elif piece[0] == "UL":
    elif piece[0] == "UR":
        y = cols - 1
        while y != 0:
            starting_piece = pieces[starting_piece].neighbors[3]
            print(starting_piece)
            print(pieces[starting_piece].differences)
            y -= 1
    
    return starting_piece
