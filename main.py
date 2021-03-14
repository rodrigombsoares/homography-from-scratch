import os
from PIL import Image

from utils.shape import is_inside, get_polygon
from utils.homography import find_h_inv, find_decal_point
from config import config1, config2, BOUND


def apply_decal_if_inside_border(picture, decal, point, polygon, h_inv, limit):
    """
    If point inside border (Polygon), apply decal
    """
    if is_inside(point, polygon):
        decal_point = find_decal_point(h_inv, point, limit)
        picture.putpixel(point, decal.getpixel(decal_point))

def build_image(config):
    # Open original image
    cwd = os.getcwd()
    picture = Image.open(os.path.join(cwd, "images", config["PICTURE"]))
    decal = Image.open(os.path.join(cwd, "images", config["DECAL"]))
    polygon = get_polygon(config["PICTURE_BORDER"])
    limit = (decal.width-BOUND, decal.height-BOUND)
    DECAL_BORDER = [(0,0), (decal.width,0), (decal.width, decal.height), (0, decal.height)]

    # Find Inverse Homography
    h_inv = find_h_inv(config["PICTURE_BORDER"], DECAL_BORDER)

    # Run for every pixel in Picture
    for i in range(picture.width):
        for j in range(picture.height):
            apply_decal_if_inside_border(picture, decal, (i,j), polygon, h_inv, limit)
    # Save result
    picture.save(os.path.join("results", config["NAME"]), "PNG")

build_image(config1)
build_image(config2)