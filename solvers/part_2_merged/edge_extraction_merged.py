import cv2 as cv
import numpy as np
from collections import Counter
import itertools
import math

def most_frequent_color(image):
    pixels = image.reshape(-1, image.shape[-1])
    count = Counter(map(tuple, pixels))
    most_common = count.most_common(1)[0][0]
    return most_common

def create_mask(image, color):
    mask = np.all(image == color, axis=-1)
    return 1 - mask.astype(np.uint8)    

def extract_puzzle_pieces(image_path):
  """
  input: image path,
  output: contours, image, mask
  finds most frequent color in the image (most probably its the background),
  then masks the imageimage based on the color,
  find contours then seperates each puzzle piece
  """
  image = cv.imread(image_path)
  # if(True):
  #   h, w = image.shape[:2]
  #   resized_image = cv.resize(image, (w*2, h*2))
  #   image = resized_image
  mfc = most_frequent_color(image)

  mask = create_mask(image, mfc)
  # mask = apply_color_mask(image,  [45, 10, 10], [95, 255, 255])

  # Apply morphological operations(opening to remove noise, then closing):
  kernel = np.ones((5,5), np.uint8)
  mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
  mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)

  # Find contours
  contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)


  return contours, image, mask

def and_operation(puzzle_piece, mask_piece):
  binary_image_3_channel = np.stack((mask_piece,)*3, axis=-1)
  result_image = np.bitwise_and(puzzle_piece, binary_image_3_channel * 255)
  return result_image

def get_border_mask(mask_piece):
  kernel = np.ones((3,3), np.uint8)
  eroded_mask = cv.erode(mask_piece, kernel, iterations = 1)
  border_mask = mask_piece - eroded_mask
  return border_mask

def distance_px(val1, val2):
  return abs(val1[0] - val2[0]) + abs(val1[1] - val2[1])

def sort_points(points):
    centroid = [sum(x) / len(points) for x in zip(*points)]
    def angle(point):
        return math.atan2(point[1] - centroid[1], point[0] - centroid[0])
    sorted_points = sorted(points, key=angle)
    return sorted_points

def distance(x, y, a, b):
    return math.sqrt((a - x)**2 + (b - y)**2)

def edge_length_error(points):
  dist = []
  avg_dist = 0
  for i in range(0, len(points)):
    j = i - 1
    if j < 0: j = len(points) - 1
    tmp = distance(*points[i], *points[j])
    avg_dist += tmp
    dist.append(tmp)
  avg_dist /= 4
  error = 0
  for val in dist:
    error += abs(avg_dist - val)
  return error

def area_with_mask(points, mask_piece):
  height, width = mask_piece.shape
  tmp_mask = np.zeros((height, width), dtype=np.uint8)
  reversed_points = [[y,x] for x, y in points]
  points_array = np.array([reversed_points], dtype=np.int32)
  cv.fillPoly(tmp_mask, points_array, 1)
  bitwise_and_result = cv.bitwise_and(mask_piece, tmp_mask)
  area = np.count_nonzero(bitwise_and_result)
  return area

def find_largest_quadrilateral(points, mask_piece):

    max_area = -1e10
    max_quad = points[:4]

    square_treshold = 100

    for quad in itertools.combinations(points, 4):
        quad = sort_points(quad)
        # area = quadrilateral_area(*quad)
        area = area_with_mask(quad, mask_piece)
        edges_error = edge_length_error(quad)
        area -= square_treshold * edges_error
        if area > max_area:
            max_area = area
            max_quad = quad

    return max_quad

def get_corner_points_2(border_mask, mask_piece):
  gray = np.float32(border_mask)
  gray = cv.GaussianBlur(gray, (7, 7), 0)
  gray = cv.GaussianBlur(gray, (7, 7), 0)
  dst = cv.cornerHarris(gray, blockSize=2, ksize=3, k=0.04)
  dst = cv.dilate(dst, None)
  corner_mask = dst >  0.03 * dst.max()

  corner_points = []
  for i in range(corner_mask.shape[0]):
    for j in range(corner_mask.shape[1]):
      if(corner_mask[i, j]):
        corner_points.append((i, j))

  thresh = 20
  pot_points = {}
  for point in corner_points:
    x , y = point
    found = False
    keys_to_del = []
    for key, val in pot_points.items():
      if distance_px(point, key) <= thresh:
        if  dst[x, y] > val:
          keys_to_del.append(key)
          pot_points[point] = dst[x, y]
        found = True
        break
    for key in keys_to_del:
      del pot_points[key]
    if not found:
      pot_points[point] = dst[x, y]

  final_corner_points = find_largest_quadrilateral(list(pot_points.keys()), mask_piece)
  return final_corner_points

def get_borders(border_mask, mask_piece):

  # divide the border into four parts
  border_indicies = np.where(border_mask == 255)
  border_indicies = list(zip(*border_indicies))

  corner_points = get_corner_points_2(border_mask, mask_piece)

  border_indicies = sort_points(border_indicies)

  border_indicies = np.array(border_indicies)
  border_corner_points = []
  for corner in corner_points:
    min_in = -1
    min_val = 10000
    for i, point in enumerate(border_indicies):
      dis = distance_px(point, corner)
      if(dis < min_val):
        min_val = dis
        min_in = i
    border_corner_points.append(min_in)

  borders = []
  border_corner_points.append(len(border_indicies)) #help for later
  for i in range(len(border_corner_points) - 1):
    cur_border = []
    for j in range(border_corner_points[i], border_corner_points[i+1]):
      cur_border.append(border_indicies[j])
    if(i == len(border_corner_points) - 2):
      for j in range(0, border_corner_points[0]):
        cur_border.append(border_indicies[j])
    cur_border = np.array(cur_border)

    borders.append(cur_border)
  return borders, border_indicies[border_corner_points[0]]

def get_border_color(border, puzzle_piece):
  color = []
  for point in border:
    color.append(puzzle_piece[point[0], point[1]])
  return color

def keep_one_each_unit(border, axis):
  # axis = 0 => x-axis
  # axis = 1 => y_axis
  i = axis%2
  points = {}
  for point in border:
    key = point[i]
    val = point[1-i]
    if key in points.keys():
      points[key].append(val)
    else:
      points[key] = [val]
  new_border = []
  for key, val in points.items():
    new_point = np.zeros(2, dtype=int)
    new_point[i] = key
    tmp = 0
    if(axis == 0 or axis == 3):
      tmp = min(val)
    else:
      tmp = max(val)
    new_point[1-i] = tmp
    new_border.append(new_point)
  new_border = np.array(new_border)
  if(axis < 2):
    sorted_indices = np.argsort(new_border[:, i])[::-1]
  else:
    sorted_indices = np.argsort(new_border[:, i])

  new_border = new_border[sorted_indices]

  return new_border

def align_border(border):
    border = np.array(border)
    # Calculate the angle to rotate
    dx = dy = 0
    dx = border[-1][0] - border[0][0]
    dy = border[-1][1] - border[0][1]
    angle = np.arctan2(dy, dx)

    # Rotation matrix
    rotation_matrix = np.array([[np.cos(angle), -np.sin(angle)],
                                [np.sin(angle), np.cos(angle)]])

    # Apply rotation
    aligned_border = np.dot(border - border[0], rotation_matrix)
    return aligned_border

def average_of_points(points):
    points_array = np.array(points)
    y_values = points_array[:, 1]  # Extracting the y-values
    max_y = np.max(y_values)
    min_y = np.min(y_values)
    avg = np.mean(y_values)
    return min_y, max_y, avg

def edge_extraction(image_path):
  
  contours, image, mask = extract_puzzle_pieces(image_path)

  pieces_borders = []
  puzzle_pieces = []
  puzzle_pieces_top_left_corner = []

  for i, contour in enumerate(contours):

    x, y, w, h = cv.boundingRect(contour)
    puzzle_piece = image[y-3:y+h+3, x-3:x+w+3]
    mask_piece = mask[y-3:y+h+3, x-3:x+w+3] * 255

    masked_piece = and_operation(image[y:y+h, x:x+w], mask[y:y+h, x:x+w])
    puzzle_pieces.append(masked_piece)

    border_mask = get_border_mask(mask_piece)
    tmp_borders, left_corner = get_borders(border_mask, mask_piece)
    puzzle_pieces_top_left_corner.append(left_corner)

    colors_border=[]
    for j in range(len(tmp_borders)):
      colors_border.append(get_border_color(tmp_borders[j], puzzle_piece))
      tmp_borders[j] = keep_one_each_unit(tmp_borders[j], j)

    borders = {}
    borders["border"] = tmp_borders
    borders["aligned_border"] = []
    borders["border_type"] = []
    borders["colors_border"] = colors_border


    # align border and try to detect if its straight or ..
    for i, border in enumerate(borders["border"]):

      aligned_border = align_border(border)
      borders["aligned_border"].append(aligned_border)

      min, max, _ = average_of_points(aligned_border)
      dif = max - min
      edge_type = 0 # 2 if straight, 0 if ntoo2, 1 if hole
      # classifying the edge based on minimum and maximum y value after aligning it to the x axis
      if(dif <= 10):
        edge_type = 2
      elif(min <= -25):
        edge_type = 1

      borders["border_type"].append(edge_type)
    pieces_borders.append(borders)

  return pieces_borders, puzzle_pieces, puzzle_pieces_top_left_corner