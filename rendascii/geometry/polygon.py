"""
This file is part of RendASCII which is released under MIT.
See file LICENSE.txt for full license details.
"""


from rendascii.geometry import vector
from rendascii.geometry import PLANE_NORMAL, PLANE_POINT
from rendascii.geometry import X, Y


# 2D polygon functions.

def generate_aabb_2d(poly):
  bound_min_x = None
  bound_min_y = None
  bound_max_x = None
  bound_max_y = None

  for vertex in poly:
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


def aabb_contains_point_2d(aabb, point):
  return (
      aabb[0][X] < point[X] < aabb[1][X]
      and aabb[0][Y] < point[Y] < aabb[1][Y]
      )


def poly_contains_point_2d(poly, point):
  start = _edge_2d(point, poly[-1], poly[0]) <= 0
  for i in range(len(poly) - 1):
    if (_edge_2d(point, poly[i], poly[i + 1]) <= 0) != start:
      return False
  return True


def interpolate_attribute_2d(poly, attributes, point):
  v0 = poly[0]
  v1 = poly[1]
  v2 = poly[2]

  # Calculate baycentric weights.
  area_t = _double_area_2d(v0, v1, v2)
  w0 = _double_area_2d(point, v1, v2) / area_t
  w1 = _double_area_2d(point, v2, v0) / area_t
  w2 = _double_area_2d(point, v0, v1) / area_t

  return (
      w0 * attributes[0]
      + w1 * attributes[1]
      + w2 * attributes[2]
      )


# 3D polygon functions.

def normal_3d(poly):
  return vector.cross_3d(
      vector.subtract(poly[1], poly[0]), 
      vector.subtract(poly[2], poly[0])
      )


# Homogenous polygon functions.

def f_cull_h(poly, plane):
  # Determine which vertices are outside the clipping plane.
  inside = []
  outside = []
  for v in range(len(poly)):
    if (
        vector.dot(
          plane[PLANE_NORMAL],
          vector.subtract(
            poly[v],
            plane[PLANE_POINT]
            )
          ) < 0.0
        ):
      outside.append(v)
    else:
      inside.append(v)

  # Declare output polygons.
  out_polys = []
  # No vertices outside.
  if len(outside) == 0:
    out_polys = [poly,]
  # One vertex outside.
  elif len(outside) == 1:
    out_polys = _f_cull_1(poly, plane, inside, outside)
  # Two vertices outside.
  elif len(outside) == 2:
    out_polys = _f_cull_2(poly, plane, inside, outside)

  return out_polys


# Helper functions.

def _f_cull_1(poly, plane, inside, outside):
  # Initialize output polygons.
  out_polys = [[None,] * 3,] * 2

  # Calculate output polygons.
  i0 = inside[0]
  i1 = inside[1]
  o0 = outside[0]
  p0 = vector.project_h(
      poly[i0],
      poly[o0],
      plane
      )
  p1 = vector.project_h(
      poly[i1],
      poly[o0],
      plane
      )
  # Set output polygons.
  out_polys[0][i0] = poly[i0]
  out_polys[0][i1] = poly[i1]
  out_polys[0][o0] = p1
  out_polys[0] = tuple(out_polys[0])
  out_polys[1][i0] = poly[i0]
  out_polys[1][i1] = p0
  out_polys[1][o0] = p1
  out_polys[1] = tuple(out_polys[1])
  
  return out_polys


def _f_cull_2(poly, plane, inside, outside):
  # Initialize output polygons.
  out_polys = [[None,] * 3,]

  # Calculate output polygon.
  i0 = inside[0]
  o0 = outside[0]
  o1 = outside[1]
  p0 = vector.project_h(
      poly[i0],
      poly[o0],
      plane
      )
  p1 = vector.project_h(
      poly[i0],
      poly[o1],
      plane
      )
  # Set packet data.
  out_polys[0][i0] = poly[i0]
  out_polys[0][o0] = p0
  out_polys[0][o1] = p1
  out_polys[0] = tuple(out_polys[0])

  return out_polys


def _edge_2d(vec, line_s, line_e):
  # Check which side of line a vector lies on (sign).
  return (
      (vec[X] - line_e[X]) * (line_s[Y] - line_e[Y])
      - (line_s[X] - line_e[X]) * (vec[Y] - line_e[Y])
      )


def _double_area_2d(v0, v1, v2):
  area = (
      v0[X] * v1[Y] + v1[X] * v2[Y] + v2[X] * v0[Y]
      - v0[X] * v2[Y] - v2[X] * v1[Y] - v1[X] * v0[Y]
      )
  if area < 0:
    area = -area
  return area
