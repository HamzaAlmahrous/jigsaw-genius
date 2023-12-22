# imports:
import cv2 as cv
from edge_extraction_functions import edge_extraction
from match_and_order import get_classified_pieces, order_pieces
from list_to_image import convert_list_to_image

def solve_jigsaw(jigsaw_path):
    original_img = cv.imread(jigsaw_path)
    pieces_borders, pieces_countours, puzzle_pieces, puzzle_pieces_top_left_corner = edge_extraction(jigsaw_path)
    # print("done1")
    classified_pieces = get_classified_pieces(pieces_borders)
    # print("done2")
    puzzle_list, width, height, width_px, height_px= order_pieces(classified_pieces, pieces_borders)
    # print("done3")
    final_image = convert_list_to_image(width, height, width_px, height_px, puzzle_list, puzzle_pieces, puzzle_pieces_top_left_corner)
    # print("done4")

    cv.imshow('Solved Image', final_image)
    cv.imshow('Jigsaw Image', original_img)
    cv.waitKey(0)
    cv.destroyAllWindows()