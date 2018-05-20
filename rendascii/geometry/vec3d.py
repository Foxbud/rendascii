"""
TBA.
"""


def abs(vec):
  return tuple(
      -vec[X] if vec[X] < 0 else vec[X],
      -vec[Y] if vec[Y] < 0 else vec[Y],
      -vec[Z] if vec[Z] < 0 else vec[Z],
      )


def negate(vec):
  return tuple(
      -vec[X],
      -vec[Y],
      -vec[Z],
      )


def add(vec_a, vec_b):
  return tuple(
      vec_a[X] + vec_b[X],
      vec_a[Y] + vec_b[Y],
      vec_a[Z] + vec_b[Z],
      )


def subtract(vec_b, vec_a):
  return tuple(
      vec_b[X] - vec_a[X],
      vec_b[Y] - vec_a[Y],
      vec_b[Z] - vec_a[Z],
      )


def multiply(vec, scalar):
  return tuple(
      vec[X] * scalar,
      vec[Y] * scalar,
      vec[Z] * scalar,
      )


def dot(vec_a, vec_b):
  return vec_a[X] * vec_b[X] + vec_a[Y] * vec_b[Y] + vec_a[Z] * vec_b[Z]


def squared_dist(vec_b, vec_a):
  diff = vec_b[X] - vec_a[X]
  sum = diff * diff
  diff = vec_b[Y] - vec_a[Y]
  sum += diff * diff
  diff = vec_b[Z] - vec_a[Z]
  sum += diff * diff
  return sum


def cross(vec_a, vec_b):
  return tuple(
      vec_a[Y] * vec_b[Z] - vec_a[Z] * vec_b[Y],
      vec_a[Z] * vec_b[X] - vec_a[X] * vec_b[Z],
      vec_a[X] * vec_b[Y] - vec_a[Y] * vec_b[X],
      )
