"""
TBA.
"""


def abs(vec):
  return tuple(
      -vec[X] if vec[X] < 0 else vec[X],
      -vec[Y] if vec[Y] < 0 else vec[Y],
      )


def negate(vec):
  return tuple(
      -vec[X],
      -vec[Y],
      )


def add(vec_a, vec_b):
  return tuple(
      vec_a[X] + vec_b[X],
      vec_a[Y] + vec_b[Y],
      )


def subtract(vec_b, vec_a):
  return tuple(
      vec_b[X] - vec_a[X],
      vec_b[Y] - vec_a[Y],
      )


def multiply(vec, scalar):
  return tuple(
      vec[X] * scalar,
      vec[Y] * scalar,
      )


def dot(vec_a, vec_b):
  return vec_a[X] * vec_b[X] + vec_a[Y] * vec_b[Y]


def squared_dist(vec_b, vec_a):
  diff = vec_b[X] - vec_a[X]
  sum = diff * diff
  diff = vec_b[Y] - vec_a[Y]
  sum += diff * diff
  return sum
