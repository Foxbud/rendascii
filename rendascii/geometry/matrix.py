"""
TBA.
"""


import math
from rendascii.geometry import X, Y, Z


IDENTITY_3D = (
      (1.0, 0.0, 0.0, 0.0,),
      (0.0, 1.0, 0.0, 0.0,),
      (0.0, 0.0, 1.0, 0.0,),
      (0.0, 0.0, 0.0, 1.0,),
      )


def compose(matrix_a, matrix_b):
  return tuple(
      tuple(
        sum(
          tuple(
            matrix_a[i][k] * matrix_b[k][j]
            for k
            in range(len(matrix_b))
            )
          )
        for j
        in range(len(matrix_b[0]))
        )
      for i
      in range(len(matrix_a))
      )


def transpose(matrix):
  return tuple(
      tuple(
        matrix[j][i]
        for j
        in range(len(matrix[0]))
        )
      for i
      in range(len(matrix))
      )


def transform_3d(matrix, vector):
  h_vec = (
      vector[X],
      vector[Y],
      vector[Z],
      1.0,
      )
  return tuple(
      sum(
        tuple(
          matrix[i][j] * h_vec[j]
          for j
          in range(len(h_vec))
          )
        )
      for i
      in range(len(vector))
      )


def scaling_3d(scalar):
  return (
      (scalar, 0.0, 0.0, 0.0,),
      (0.0, scalar, 0.0, 0.0,),
      (0.0, 0.0, scalar, 0.0,),
      (0.0, 0.0, 0.0, 1.0,),
      )


def translation_3d(vector):
  return (
      (1.0, 0.0, 0.0, vector[X],),
      (0.0, 1.0, 0.0, vector[Y],),
      (0.0, 0.0, 1.0, vector[Z],),
      (0.0, 0.0, 0.0, 1.0,),
      )


def rotation_3d(theta, axis):
  x = axis[X]
  y = axis[Y]
  z = axis[Z]
  s = math.sin(theta)
  c = math.cos(theta)
  o = (1 - c)
  return (
      (o * x * x + c, o * y * x - z * s, o * z * x + y * s, 0.0,),
      (o * x * y + z * s, o * y * y + c, o * z * y - x * s, 0.0,),
      (o * x * z - y * s, o * y * z + x * s, o * z * z + c, 0.0,),
      (0.0, 0.0, 0.0, 1.0,),
      )
