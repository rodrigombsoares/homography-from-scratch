import os
from PIL import Image

from utils.shape import is_inside, get_polygon
from utils.homography import find_h_inv, find_decal_point
from config import PICTURE, DECAL, PICTURE_BORDER


def apply_decal_if_inside_border(point, polygon, h_inv, limit):
    """
    If point inside border (Polygon), apply decal
    """
    if is_inside(point, polygon):
        decal_point = find_decal_point(h_inv, point, limit)
        picture.putpixel(point, decal.getpixel(decal_point))

# Open original image
cwd = os.getcwd()
picture = Image.open(os.path.join(cwd, "images", PICTURE))
decal = Image.open(os.path.join(cwd, "images", DECAL))
polygon = get_polygon(PICTURE_BORDER)
limit = (decal.width-1, decal.height-1)
DECAL_BORDER = [(0,0), (limit[0]+1,0), (limit[0]+1, limit[1]+1), (0, limit[1]+1)]

# Find Inverse Homography
h_inv = find_h_inv(PICTURE_BORDER, DECAL_BORDER)

# Run for every pixel in Picture
for i in range(picture.width):
    for j in range(picture.height):
        apply_decal_if_inside_border((i,j), polygon, h_inv, limit)

# Save result
picture.save("result.jpg", "JPEG")