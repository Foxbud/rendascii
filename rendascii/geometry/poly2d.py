"""
TBA.
"""


from rendascii.geometry import X, Y


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

  return (
      (bound_min_x, bound_min_y,),
      (bound_max_x, bound_max_y,),
      )


def aabb_contains_point(aabb, point):
  return (
      aabb[0][X] < point[X] < aabb[1][X]
      and aabb[0][Y] < point[Y] < aabb[1][Y]
      )


def poly_contains_point(vertices, poly, point):
  start = _edge(point, vertices[poly[-1]], vertices[poly[0]]) < 0
  for i in range(len(poly) - 1):
    if (_edge(point, vertices[poly[i]], vertices[poly[i + 1]]) <= 0) != start:
      return False
  return True


def interpolate_attribute(vertices, poly, attributes, point):
  v0 = vertices[poly[0]]
  v1 = vertices[poly[1]]
  v2 = vertices[poly[2]]

  # Calculate baycentric weights.
  area_t = _double_area(v0, v1, v2)
  w0 = _double_area(point, v1, v2) / area_t
  w1 = _double_area(point, v2, v0) / area_t
  w2 = _double_area(point, v0, v1) / area_t

  return (
      w0 * attributes[poly[0]]
      + w1 * attributes[poly[1]]
      + w2 * attributes[poly[2]]
      )


def _edge(vec, line_s, line_e):
  # Check which side of line a vector lies on (sign).
  return (
      (vec[X] - line_e[X]) * (line_s[Y] - line_e[Y])
      - (line_s[X] - line_e[X]) * (vec[Y] - line_e[Y])
      )


def _double_area(v0, v1, v2):
  area = (
      v0.x * v1.y + v1.x * v2.y + v2.x * v0.y
      - v0.x * v2.y - v2.x * v1.y - v1.x * v0.y
      )
  if area < 0:
    area = -area
  return area
