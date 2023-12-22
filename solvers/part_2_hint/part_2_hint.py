import cv2
import numpy as np
import time

def extract_features(image, method='SIFT'):
    if method == 'SIFT':
        sift = cv2.SIFT_create()
        keypoints, descriptors = sift.detectAndCompute(image, None)
    return keypoints, descriptors

def match_features(desc1, desc2, method='BF'):
    if method == 'BF':
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(desc1, desc2, k=2)
    good_matches = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good_matches.append(m)
    return good_matches

def draw_matches(img1, keypoints1, img2, keypoints2, matches):

    match_img = cv2.drawMatches(img1, keypoints1, img2, keypoints2, matches, None,
                                flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    return match_img

def find_piece_placement_and_draw_matches(piece_image, hint_image):
    start_time = time.time()
    keypoints1, descriptors1 = extract_features(piece_image)
    keypoints2, descriptors2 = extract_features(hint_image)

    matches = match_features(descriptors1, descriptors2)

    if len(matches) > 10:
        match_img = draw_matches(piece_image, keypoints1, hint_image, keypoints2, matches)
        end_time = time.time() 
        print(f"Time taken for find_piece_placement_and_draw_matches: {end_time - start_time} seconds")
        return match_img
    else:
        return None
    

def extract_features(image):
    
    sift = cv2.SIFT_create()
   
    keypoints, descriptors = sift.detectAndCompute(image, None)
    return keypoints, descriptors

def match_features(desc1, desc2):
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(desc1, desc2, k=2)
    good_matches = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good_matches.append(m)
    return good_matches

def annotate_piece(piece_image, order_number):
    font = cv2.FONT_HERSHEY_SIMPLEX
    position = (10, piece_image.shape[0] - 10)
    cv2.putText(piece_image, str(order_number), position, font, 1, (0, 255, 0), 2, cv2.LINE_AA)
    return piece_image


def find_homography(piece_keypoints, hint_keypoints, matches, min_match_count=0, min_inliers=6):
    if len(matches) >= min_match_count:
        src_pts = np.float32([piece_keypoints[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([hint_keypoints[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
        matrix, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        if mask is not None:
            inliers = np.sum(mask)
            print(f"Homography inliers count is {inliers}")
            if inliers >= min_inliers:
                return matrix, mask
    return None, None

def remove_white_background(image, threshold=240):
    mask = cv2.inRange(image, np.array([threshold, threshold, threshold]), np.array([255, 255, 255]))
    mask_inv = cv2.bitwise_not(mask)
    image_rgba = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
    image_rgba[:, :, 3] = mask_inv

    return image_rgba

def save_transformed_image(image, filename):
    print(filename)
    # cv2.imwrite(filename, image)

def solve_jigsaw_with_hint(piece_image_path, hint_image_path, piece_images_path, number_of_pieces, number_of_score):
    
    piece_image = cv2.imread(piece_image_path)
    hint_image = cv2.imread(hint_image_path)
    number_of_pieces=number_of_pieces
    number_of_score=number_of_score

    piece_images = [remove_white_background(cv2.imread(f'{piece_images_path}\puzzle_piece_{i}.png')) for i in range(number_of_pieces)]

    sift = cv2.SIFT_create()
    bf = cv2.BFMatcher()

    desired_width = 1000
    desired_height = 400

    match_img = find_piece_placement_and_draw_matches(piece_image, hint_image)
    if match_img is not None:
        smaller_img = cv2.resize(match_img, (desired_width, desired_height))

        # cv2.imshow("match_img",smaller_img)
        # cv2.imwrite("match_img.png", match_img)


    scale_factor = 1.2
    new_width = int(hint_image.shape[1] * scale_factor)
    new_height = int(hint_image.shape[0] * scale_factor)
    resized_hint_image = cv2.resize(hint_image, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
    hint_keypoints, hint_descriptors = extract_features(resized_hint_image)
    canvas = np.zeros((new_height, new_width, 4), dtype=np.uint8)

    matches_dict = {}



    for i, piece_image in enumerate(piece_images):
        piece_keypoints, piece_descriptors = extract_features(piece_image)
        good_matches = match_features(piece_descriptors, hint_descriptors)
        matches_dict[i] = len(good_matches)

    sorted_pieces = sorted(matches_dict.items(), key=lambda item: item[1], reverse=True)

    for order, (piece_idx, _) in enumerate(sorted_pieces):
        piece_image = piece_images[piece_idx]
        annotated_image = annotate_piece(piece_image, order + 1)
        # cv2.imshow("annotated_image",annotated_image)



    puzzle_pieces_transformed = []

    untransformed_x, untransformed_y = 0, hint_image.shape[0]



    placed_pieces_count = 0

    height, width = hint_image.shape[:2]


    piece_width = new_width // 4
    piece_height = new_height // 4


    for i, piece_image in enumerate(piece_images):
        piece_keypoints, piece_descriptors = extract_features(piece_image)
        good_matches = match_features(piece_descriptors, hint_descriptors)
        print(f"Piece {i}: {len(good_matches)} good matches")

        if len(good_matches) >= number_of_score:
            matrix, mask = find_homography(piece_keypoints, hint_keypoints, good_matches)
            if matrix is not None:
                print(f"Piece {i}: Homography matrix is\n{matrix}")
                h, w = hint_image.shape[:2]
                transformed_image = cv2.warpPerspective(piece_image, matrix, (new_width, new_height))
                # cv2.imshow("transformed_image", transformed_image)
                # cv2.waitKey(0)
                puzzle_pieces_transformed.append(transformed_image)
            else:
                print(f"Piece {i}: Homography matrix could not be found or is not reliable.")


    for transformed_piece in puzzle_pieces_transformed:
        mask = cv2.cvtColor(transformed_piece, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(mask, 1, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            placed_pieces_count += 1
            cnt = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(cnt)
            canvas_piece = canvas[y:y+h, x:x+w]
            transformed_piece_section = transformed_piece[y:y+h, x:x+w]

            canvas_piece[np.where(transformed_piece_section > 0)] = transformed_piece_section[np.where(transformed_piece_section > 0)]
            canvas[y:y+h, x:x+w] = canvas_piece


    print("Number of pieces transformed:", len(puzzle_pieces_transformed))

    print("Estimated Time Complexity:")
    print("Feature Extraction for each piece: O(N^2)")
    print("Feature Matching for each piece with hint image: O(M * N)")
    print("Overall for P pieces: O(P * N^2) for feature extraction, O(P * M * N) for matching")
    print(f"With {number_of_pieces} pieces, the complexities become O({number_of_pieces} * N^2) and O({number_of_pieces} * M * N) respectively.")


    # cv2.imwrite("canvas.png", canvas)
    cv2.imshow("canvas",canvas)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# solve_jigsaw_with_hint("C:/ITE/ITE 5/CV/practical_lectures/project/images/part_2_hint/meme2/puzzle.png", "C:/ITE/ITE 5/CV/practical_lectures/project/images/part_2_hint/meme2/puzzle_solved.jpeg", "C:/ITE/ITE 5/CV/practical_lectures/project/images/part_2_hint/meme2/puzzle_piece_", 9, 4)