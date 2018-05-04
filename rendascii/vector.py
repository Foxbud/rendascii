"""
This module contains utilities for efficiently working with 2D and 3D vectors.
"""


class Vec2D:
  
  def __init__(self):
    pass


class Vec3D:

  def __init__(self, initializer=None):
    # Initialize instance attributes.
    if initializer is None:
      self._x = 0.0
      self._y = 0.0
      self._z = 0.0
    else:
      self._x = initializer[0]
      self._y = initializer[1]
      self._z = initializer[2]

  def set_x(self, val):
    self._x = val

  def set_y(self, val):
    self._y = val

  def set_z(self, val):
    self._z = val

  def get_x(self):
    return self._x

  def get_y(self):
    return self._y

  def get_z(self):
    return self._z

  def abs(self):
    self._x = -self._x if self._x < 0 else self._x
    self._y = -self._y if self._y < 0 else self._y
    self._z = -self._z if self._z < 0 else self._z

  def neg(self):
    self._x = -self._x
    self._y = -self._y
    self._z = -self._z

  def add(self, vec):
    self._x += vec._x
    self._y += vec._y
    self._z += vec._z

  def sub(self, vec):
    self._x -= vec._x
    self._y -= vec._y
    self._z -= vec._z

  def mul(self, scalar):
    self._x *= scalar
    self._y *= scalar
    self._z *= scalar

  def dot(self, vec):
    return self._x * vec._x + self._y * vec._y + self._z * vec._z

  def cross(self, vec):
    x = self._y * vec._z - self._z * vec._y
    y = self._z * vec._x - self._x * vec._z
    z = self._x * vec._y - self._y * vec._x
    self._x = x
    self._y = y
    self._z = z

  def sdist(self, vec):
    diff = self._x - vec._x
    sum = diff * diff
    diff = self._y - vec._y
    sum += diff * diff
    diff = self._z - vec._z
    sum += diff * diff
    return sum
