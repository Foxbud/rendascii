"""
This file is part of RendASCII which is released under MIT.
See file LICENSE.txt for full license details.
"""


import math
from rendascii.geometry import X, Y, Z, W


def abs(vec):
  return (
      -vec[X] if vec[X] < 0 else vec[X],
      -vec[Y] if vec[Y] < 0 else vec[Y],
      -vec[Z] if vec[Z] < 0 else vec[Z],
      -vec[W] if vec[W] < 0 else vec[W],
      )


def negate(vec):
  return (
      -vec[X],
      -vec[Y],
      -vec[Z],
      -vec[W],
      )


def add(vec_a, vec_b):
  return (
      vec_a[X] + vec_b[X],
      vec_a[Y] + vec_b[Y],
      vec_a[Z] + vec_b[Z],
      vec_a[W] + vec_b[W],
      )


def subtract(vec_b, vec_a):
  return (
      vec_b[X] - vec_a[X],
      vec_b[Y] - vec_a[Y],
      vec_b[Z] - vec_a[Z],
      vec_b[W] - vec_a[W],
      )


def multiply(vec, scalar):
  return (
      vec[X] * scalar,
      vec[Y] * scalar,
      vec[Z] * scalar,
      vec[W] * scalar,
      )


def dot(vec_a, vec_b):
  return (
      vec_a[X] * vec_b[X]
      + vec_a[Y] * vec_b[Y]
      + vec_a[Z] * vec_b[Z]
      + vec_a[W] * vec_b[W]
      )


def distance(vec_b, vec_a):
  diff = vec_b[X] - vec_a[X]
  sum = diff * diff
  diff = vec_b[Y] - vec_a[Y]
  sum += diff * diff
  diff = vec_b[Z] - vec_a[Z]
  sum += diff * diff
  diff = vec_b[W] - vec_a[W]
  sum += diff * diff
  return math.sqrt(sum)


def homogenize(vec, w=1.0):
  return (
      vec[X],
      vec[Y],
      vec[Z],
      w,
      )


def normalize(vec):
  return (
      vec[X] / vec[W],
      vec[Y] / vec[W],
      vec[Z] / vec[W],
      )


def project_z(vec, focus, ):
  ratio = -focus[Z] / (
      vec[Z] - focus[Z]
      )
  return (
      focus[X] + ratio * (
        vec[X] - focus[X]
        ),
      focus[Y] + ratio * (
        vec[Y] - focus[Y]
        ),
      0.0,
      focus[W] + ratio * (
        vec[W] - focus[W]
        ),
      )
