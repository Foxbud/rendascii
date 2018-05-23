
"""
TBA.
"""


from rendascii.geometry import vec3d
from rendascii.geometry import X, Y, Z


def center(poly):
  return (
      (poly[0][X] + poly[1][X] + poly[2][X]) / 3,
      (poly[0][Y] + poly[1][Y] + poly[2][Y]) / 3,
      (poly[0][X] + poly[1][X] + poly[2][Z]) / 3,
      )


def normal(poly):
  return vec3d.cross(
      vec3d.subtract(poly[1], poly[0]), 
      vec3d.subtract(poly[2], poly[0])
      )
