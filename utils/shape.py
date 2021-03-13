from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

def get_polygon(points):
    return Polygon(points)


def is_inside(point, polygon):
    point = Point(*point)
    return polygon.contains(point)
