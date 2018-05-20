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

  def update_bounds_2d(self):
    # Calculate 2D AABB.
    for vertex in self.vertices:
      if self.proj_bound_min.x is None or vertex.x < self.proj_bound_min.x:
        self.proj_bound_min.x = vertex.x
      if self.proj_bound_min.y is None or vertex.y < self.proj_bound_min.y:
        self.proj_bound_min.y = vertex.y
      if self.proj_bound_max.x is None or vertex.x > self.proj_bound_max.x:
        self.proj_bound_max.x = vertex.x
      if self.proj_bound_max.y is None or vertex.y > self.proj_bound_max.y:
        self.proj_bound_max.y = vertex.y

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

  def contains_point_2d(self, vec):
    # Check if vector is inside AABB.
    if (
        self.proj_bound_min.x < vec.x < self.proj_bound_max.x
        and self.proj_bound_min.y < vec.y < self.proj_bound_max.y
        ):
      # Check if vector is inside polygon.
      start = self._edge_2d(vec, self.vertices[-1], self.vertices[0]) < 0

      for i in range(len(self.vertices) - 1):
        if (
            (self._edge_2d(vec, self.vertices[i], self.vertices[i + 1]) <= 0)
            != start
            ):
          return False

      return True

    return False

  def _edge_2d(self, vec, line_s, line_e):
    # Check which side of line a vector lies on (sign).
    return (
        (vec.x - line_e.x) * (line_s.y - line_e.y)
        - (line_s.x - line_e.x) * (vec.y - line_e.y)
        )

  def _triangle_area_2d(self, v0, v1, v2):
    return 0.5 * math.abs(
        v0.x * v1.y+ v1.x * v2.y + v2.x * v0.y
        - v0.x * v2.y - v2.x * v1.y - v1.x * v0.y
        )
