"""
This file is part of RendASCII which is released under MIT.
See file LICENSE.txt for full license details.
"""


import math
from rendascii.geometry import PLANE_NORMAL, PLANE_POINT
from rendascii.geometry import X, Y, Z, W
from sys import float_info


# Common vector functions.

def abs(vec):
  return tuple(
      -vec[c] if vec[c] < 0 else vec[c]
      for c
      in range(len(vec))
      )


def negate(vec):
  return tuple(
      -vec[c]
      for c
      in range(len(vec))
      )


def add(vec_a, vec_b):
  return tuple(
      vec_a[c] + vec_b[c]
      for c
      in range(len(vec_a))
      )


def subtract(vec_b, vec_a):
  return tuple(
      vec_b[c] - vec_a[c]
      for c
      in range(len(vec_b))
      )


def multiply(vec, scalar):
  return tuple(
      vec[c] * scalar
      for c
      in range(len(vec))
      )


def dot(vec_a, vec_b):
  return sum(
      vec_a[c] * vec_b[c]
      for c
      in range(len(vec_a))
      )


def distance(vec_b, vec_a):
  vec_diff = subtract(vec_b, vec_a)
  return math.sqrt(
      dot(
        vec_diff,
        vec_diff
        )
      )


# 3D vector functions.

def cross_3d(vec_a, vec_b):
  return (
      vec_a[Y] * vec_b[Z] - vec_a[Z] * vec_b[Y],
      vec_a[Z] * vec_b[X] - vec_a[X] * vec_b[Z],
      vec_a[X] * vec_b[Y] - vec_a[Y] * vec_b[X],
      )


# Homogeneous vector functions.

def project_h(vec, focus, plane):
  u = subtract(vec, focus)
  direction = dot(plane[PLANE_NORMAL], u)
  # Handle potential division by zero.
  if direction == 0.0:
    direction = float_info.min
  w = subtract(focus, plane[PLANE_POINT])
  ratio = -dot(plane[PLANE_NORMAL], w) / direction
  u = multiply(u, ratio)
  return add(focus, u)


# Vector conversion functions.

def conv_2d_to_3d(vec_2d, order=(X, Y, None,)):
  return tuple(
      vec_2d[order[c]] if order[c] is not None else 0.0
      for c
      in range(len(order))
      )


def conv_3d_to_2d(vec_3d, order=(X, Y,)):
  return tuple(
      vec_3d[order[c]]
      for c
      in range(len(order))
      )


def conv_3d_to_h(vec_3d, w=1.0):
  return (
      vec_3d[X],
      vec_3d[Y],
      vec_3d[Z],
      w,
      )


def conv_h_to_3d(vec_h):
  return (
      vec_h[X] / vec_h[W],
      vec_h[Y] / vec_h[W],
      vec_h[Z] / vec_h[W],
      )
