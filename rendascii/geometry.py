"""
TBA.
"""


import math


class Polygon:

  def __init__(self, vertices, normal):
    # Initialize instance attributes.
    self.vertices = vertices
    self.normal = normal
    self.proj_bound_min = Vec2D([None, None])
    self.proj_bound_max = Vec2D([None, None])

  def interpolate_z(self, vec):
    # Calculate baycentric weights.
    area_t = self._triangle_area_2d(*self.vertices)
    w0 = self._triangle_area_2d(vec, vertices[1], vertices[2]) / area_t
    w1 = self._triangle_area_2d(vec, vertices[2], vertices[0]) / area_t
    w2 = self._triangle_area_2d(vec, vertices[0], vertices[1]) / area_t

    return (
        w0 * self.vertices[0].z
        + w1 * self.vertices[1].z
        + w2 * self.vertices[2].z
        )

  def _triangle_area_2d(self, v0, v1, v2):
    return 0.5 * math.abs(
        v0.x * v1.y+ v1.x * v2.y + v2.x * v0.y
        - v0.x * v2.y - v2.x * v1.y - v1.x * v0.y
        )
