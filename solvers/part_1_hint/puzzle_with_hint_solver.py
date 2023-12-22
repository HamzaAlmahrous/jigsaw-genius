import cv2
import numpy as np
import time 

def create_image_grid(image_list, rows, cols):
    image_list.sort(key=lambda x: x[1])

    images = [img for img, _ in image_list]

    if len(images) != rows * cols:
        raise ValueError("Number of images does not match rows * cols")

    img_height, img_width = images[0].shape[:2]

    grid_image = np.zeros((img_height * rows, img_width * cols, 3), dtype=np.uint8)

    for idx, img in enumerate(images):
        row = idx // cols
        col = idx % cols
        grid_image[row*img_height:(row+1)*img_height, col*img_width:(col+1)*img_width] = img

    return grid_image

def count_similar_pixels(img1, img2, threshold=0):
    if img1.shape != img2.shape:
        raise ValueError("Images must be the same size")

    img1 = np.array(img1)
    img2 = np.array(img2)

    diff = cv2.absdiff(img1, img2)

    similar_pixels = np.sum(diff <= threshold)

    return similar_pixels

def find_piece_positions_pure(puzzle_pieces, original_pieces, rows, cols):
    list1 = puzzle_pieces
    list2 = original_pieces

    threshold = 0.8

    matches = []

    for i, image1 in enumerate(list1):
        max_matches = 0
        best_place = -1

        for j, image2 in enumerate(list2):
            current_match = count_similar_pixels(image1, image2)
            if(current_match > max_matches):
                max_matches = current_match
                best_place = j
        
        matches.append((image1, best_place))

    return matches

def segment_puzzle(image, rows, cols):
    h, w = image.shape[:2]
    piece_width, piece_height = w // cols, h // rows

    piece_size = f"Piece size: {piece_height}, {piece_width}"

    pieces = []

    for y in range(rows):
        for x in range(cols):
            left, top, right, bottom = x * piece_width, y * piece_height, (x + 1) * piece_width, (y + 1) * piece_height
            piece_data = image[top:bottom, left:right, :]
            pieces.append(piece_data)

    return pieces, piece_width, piece_height

def resize_images(img1, img2):
    h = min(img1.shape[0], img2.shape[0])
    w = min(img1.shape[1], img2.shape[1])
    img1_resized = cv2.resize(img1, (w, h))
    img2_resized = cv2.resize(img2, (w, h))
    return img1_resized, img2_resized

def display_pieces(pieces):
    i = 0
    for piece in pieces:
        window_name = f"Piece {i+1}"
        cv2.imshow(window_name, piece)
        i+=1
        cv2.waitKey(500)  # Wait for 500 ms between each piece
    cv2.waitKey(0)  # Wait until a key press to close
    cv2.destroyAllWindows()

def solve_puzzle_with_hint(original_img_path, puzzle_img_path, rows, cols):
    
    start_time_serial_genetic = time.perf_counter()
    
    original_img = cv2.imread(original_img_path)
    puzzle_img = cv2.imread(puzzle_img_path)
    original_img, puzzle_img = resize_images(original_img, puzzle_img)

    puzzle_pieces, puzzle_piece_width, puzzle_piece_height = segment_puzzle(puzzle_img, rows, cols)
    
    original_pieces, original_piece_width, original_piece_height = segment_puzzle(original_img, rows, cols)

    # display_pieces(pieces=pieces)

    correct_images_order = find_piece_positions_pure(puzzle_pieces, original_pieces, rows, cols)
    
    final_image = create_image_grid(correct_images_order, rows, cols)
    finish_time_serial_genetic = time.perf_counter()
    serial_execution_time = finish_time_serial_genetic - start_time_serial_genetic
    print("Algorithm Execution Time: {:.2f} seconds".format(serial_execution_time))

    cv2.imshow('Solved Image', final_image)
    cv2.imshow('Puzzle Grid', puzzle_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()