"""
TBA.
"""


def generate_aabb(vertices, poly):
  bound_min_x = None
  bound_min_y = None
  bound_max_x = None
  bound_max_y = None
  for i in poly:
    vertex = vertices[i]
    if bound_min_x is None or vertex[X] < bound_min_x:
      bound_min_x = vertex[X]
    if bound_min_y is None or vertex[Y] < bound_min_y:
      bound_min_y = vertex[Y]
    if bound_max_x is None or vertex[X] > bound_max_x:
      bound_max_x = vertex[X]
    if bound_max_y is None or vertex[Y] > bound_max_y:
      bound_max_y = vertex[Y]
  return tuple(
      tuple(bound_min_x, bound_min_y),
      tuple(bound_max_x, bound_max_y),
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


def aabb_contains_point(aabb, point):
  return (
      aabb[0][X] < point[X] < aabb[1][X]
      and aabb[0][Y] < point[Y] < aabb[1][Y]
      )


def poly_contains_point(vertices, poly, point):


def _edge(vec, line_s, line_e):
  # Check which side of line a vector lies on (sign).
  return (
      (vec[X] - line_e[X]) * (line_s[Y] - line_e[Y])
      - (line_s[X] - line_e[X]) * (vec[Y] - line_e[Y])
      )
