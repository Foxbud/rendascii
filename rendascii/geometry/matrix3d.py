"""
TBA.
"""


from math import sin, cos
from rendascii.geometry import X, Y, Z, ALPHA, BETA, GAMMA
from rendascii.geometry import vec3d


def transform_vector(matrix, vec):
  return tuple(
      vec3d.dot(matrix[X], vec),
      vec3d.dot(matrix[Y], vec),
      vec3d.dot(matrix[Z], vec),
      )


def generate_rotation_matrix(euler_angles, order='xzy'):
  # Calculate trigonometric values.
  s1 = sin(euler_angles[ALPHA])
  c1 = cos(euler_angles[ALPHA])
  s2 = sin(euler_angles[BETA])
  c2 = cos(euler_angles[BETA])
  s3 = sin(euler_angles[GAMMA])
  c3 = cos(euler_angles[GAMMA])

  # Calculate rotation matrix.
  order = order.lower()
  
  if order == 'xzy':
    return tuple(
        tuple(c2 * c3, -s2, c2 * s3),
        tuple(s1 * s3 + c1 * c3 * s2, c1 * c2, c1 * s2 * s3 - c3 * s1),
        tuple(c3 * s1 * s2 - c1 * s3, c2 * s1, c1 * c3 + s1 * s2 * s3),
        )

  elif order == 'xyz':
    return tuple(
        tuple(c2 * c3, -c2 * s3, s2),
        tuple(c1 * s3 + c3 * s1 * s2, c1 * c3 - s1 * s2 * s3, -c2 * s1),
        tuple(s1 * s3 - c1 * c3 * s2, c3 * s1 + c1 * s2 * s3, c1 * c2),
        )

  elif order == 'yxz':
    return tuple(
        tuple(c1 * c3 + s1 * s2 * s3, c3 * s1 * s2 - c1 * s3, c2 * s1),
        tuple(c2 * s3, c2 * c3, -s2),
        tuple(c1 * s2 * s3 - c3 * s1, c1 * c3 * s2 + s1 * s3, c1 * c2),
        )

  elif order == 'yzx':
    return tuple(
        tuple(c1 * c2, s1 * s3 - c1 * c3 * s2, c3 * s1 + c1 * s2 * s3),
        tuple(s2, c2 * c3, -c2 * s3),
        tuple(-c2 * s1, c1 * s3 + c3 * s1 * s2, c1 * c3 - s1 * s2 * s3),
        )

  elif order == 'zyx':
    return tuple(
        tuple(c1 * c2, c1 * s2 * s3 - c3 * s1, s1 * s2 + c1 * c3 * s2),
        tuple(c2 * s1, c1 * c3 + s1 * s2 * s3, c3 * s1 * s2 - c1 * s3),
        tuple(-s2, c2 * s3, c2 * c3),
        )

  elif order == 'zxy':
    return tuple(
        tuple(c1 * c3 - s1 * s2 * s3, -c2 * s1, c1 * s3 + c3 * s1 * s2),
        tuple(c3 * s1 + c1 * s2 * s3, c1 * c2, s1 * s3 - c1 * c3 * s2),
        tuple(-c2 * s3, s2, c2 * c3),
        )
