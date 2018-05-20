"""
TBA.
"""


from rendascii.geometry import Vec2D
from rendascii.geometry import Vec3D


class Pipeline:

  def __init__(self):
    # Initialize instance attributes.
    self.vertices = []
    self.polygons = []


class Camera:

  def __init__(self, width, height, num_pixels_x, num_pixels_y, focal_dist):
    # Initialize instance attributes.
    self.max_bound = Vec2D([width / 2, height / 2])
    self.min_bound = Vec2D(self.max_bound).neg()
    frag_size = Vec2D([width / num_pixels_x, height / num_pixels_y])
    self.fragments = [
        [
          Vec2D(
            [
              self.min_bound.x + frag_size.x * (x + 0.5),
              self.min_bound.y + frag_size.y * (y + 0.5)
              ]
            )
          for x
          in range(num_pixels_x)
          ]
        for y
        in range(num_pixels_y)
        ]
    self.focal_point = Vec3D([0, 0, -focal_dist])
