import cv2
import numpy as np
from makePieces import get_pieces
import readImage as readImg
import Piece as p
import time

def create_big_image(pieces, rows, cols):
    if not pieces:
        return None

    piece_height = pieces[0].size_vertical
    piece_width = pieces[0].size_horizontal
    channels = pieces[0].pieceChn

    big_image_height = rows * piece_height
    big_image_width = cols * piece_width
    big_image = np.zeros((big_image_height, big_image_width, channels), dtype=np.uint8)

    for i, piece in enumerate(pieces):
        row = i // cols
        col = i % cols

        start_row = row * piece_height
        start_col = col * piece_width

        big_image[start_row:start_row+piece_height, start_col:start_col+piece_width, :] = piece.pieceData

    return big_image

def display_pieces(pieces):
    i = 0
    for piece in pieces:
        window_name = f"Piece {i+1}"
        cv2.imshow(window_name, piece.pieceData)
        i+=1
        cv2.waitKey(500)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def solve_puzzle(puzzle_img_path, rows, cols):
    
    start_time_serial_genetic = time.perf_counter()

    img, imgRow, imgCol, imgChn = readImg.read_image(puzzle_img_path, cv2.IMREAD_COLOR)
    pList, pSize_vertical, pSize_horizontal, pCnt_row, pCnt_column, pCnt_total = get_pieces(img, imgRow, imgCol, imgChn, cols, rows)

    p.find_neighbors(pList)

    # for x in pList:
    #     print(f"{x.pieceNum}")
    #     print(x.neighbors)

    up_left = p.find_up_left_piece(pList)
    up_right = p.find_up_right_piece(pList)
    down_left = p.find_down_left_piece(pList)
    down_right = p.find_down_right_piece(pList)

    corners = [up_left, up_right, down_left, down_right]
    
    max_corner = max(corners, key=lambda corner: corner[2])
    print("Point with the maximum x value:", max_corner)

    starting_piece = p.find_starting_piece(pList, max_corner, rows, cols)

    print(f"starting piece {starting_piece}")
    print(pList[starting_piece].neighbors)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    solved_puzzle = [[None for y in range(rows)] for x in range(cols)]

    next_piece_index = starting_piece
    for i in range(cols):
        for j in range(rows):
            solved_puzzle[i][j] = pList[next_piece_index]
            next_piece_index = pList[next_piece_index].neighbors[1]
        next_piece_index = pList[solved_puzzle[i][0].pieceNum].neighbors[2]

    solved_puzzle = [item for sublist in solved_puzzle for item in sublist]

    solved_image = create_big_image(solved_puzzle, rows, cols)

    finish_time_serial_genetic = time.perf_counter()
    serial_execution_time = finish_time_serial_genetic - start_time_serial_genetic
    print("Algorithm Execution Time: {:.2f} seconds".format(serial_execution_time))

    cv2.imshow("Solved Image", solved_image)
    cv2.imshow('Puzzle Grid', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()