import cv2 as cv
from edge_extraction_merged import edge_extraction
from match_and_order_with_sift import get_classified_pieces, order_pieces
from list_to_image import convert_list_to_image
import time

def merged_solve(image_path, hint_image_path):
    
    start_time_serial_genetic = time.perf_counter()
    
    hint_image = cv.imread(hint_image_path)

    pieces_borders, puzzle_pieces, puzzle_pieces_top_left_corner = edge_extraction(image_path)

    classified_pieces = get_classified_pieces(pieces_borders)

    puzzle_list, width, height, width_px, height_px= order_pieces(classified_pieces, pieces_borders, hint_image, puzzle_pieces)

    final_image = convert_list_to_image(width, height, width_px, height_px, puzzle_list, puzzle_pieces, puzzle_pieces_top_left_corner)

    finish_time_serial_genetic = time.perf_counter()
    serial_execution_time = finish_time_serial_genetic - start_time_serial_genetic
    print("Algorithm Execution Time: {:.2f} seconds".format(serial_execution_time))

    cv.imshow('final image', final_image)

    cv.waitKey(0)

# image_path = 'C:/ITE/ITE 5/CV/practical_lectures/cv_project/images/part_2_merged/24pieces1.png'
# hint_image_path = 'C:/ITE/ITE 5/CV/practical_lectures/cv_project/images/part_2_merged/24pieces1_solved.png'

# merged_solve(image_path, hint_image_path)