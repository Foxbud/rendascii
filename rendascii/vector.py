"""
This module contains utilities for efficiently working with 2D and 3D vectors.
"""


class Vec2D:
  
  def __init__(self, initializer=[0.0, 0.0]):
    # Initialize instance attributes.
    init_type = type(initializer)
    if init_type is List:
      self.x = initializer[0]
      self.y = initializer[1]
    else:
      self.x = initializer.x
      self.y = initializer.y

  def set(self, vec):
    self.x = vec.x
    self.y = vec.y

  def abs(self):
    self.x = -self.x if self.x < 0 else self.x
    self.y = -self.y if self.y < 0 else self.y

  def neg(self):
    self.x = -self.x
    self.y = -self.y

  def add(self, vec):
    self.x += vec.x
    self.y += vec.y

  def sub(self, vec):
    self.x -= vec.x
    self.y -= vec.y

  def mul(self, scalar):
    self.x *= scalar
    self.y *= scalar

  def dot(self, vec):
    return self.x * vec.x + self.y * vec.y

  def sdist(self, vec):
    diff = self.x - vec.x
    sum = diff * diff
    diff = self.y - vec.y
    sum += diff * diff
    return sum


class Vec3D:

  def __init__(self, initializer=[0.0, 0.0, 0.0]):
    # Initialize instance attributes.
    init_type = type(initializer)
    if init_type is List:
      self.x = initializer[0]
      self.y = initializer[1]
      self.z = initializer[2]
    else:
      self.x = initializer.x
      self.y = initializer.y
      self.z = initializer.z

  def set(self, vec):
    self.x = vec.x
    self.y = vec.y
    self.z = vec.z

  def abs(self):
    self.x = -self.x if self.x < 0 else self.x
    self.y = -self.y if self.y < 0 else self.y
    self.z = -self.z if self.z < 0 else self.z

  def neg(self):
    self.x = -self.x
    self.y = -self.y
    self.z = -self.z

  def add(self, vec):
    self.x += vec.x
    self.y += vec.y
    self.z += vec.z

  def sub(self, vec):
    self.x -= vec.x
    self.y -= vec.y
    self.z -= vec.z

  def mul(self, scalar):
    self.x *= scalar
    self.y *= scalar
    self.z *= scalar

  def dot(self, vec):
    return self.x * vec.x + self.y * vec.y + self.z * vec.z

  def cross(self, vec):
    x = self.y * vec.z - self.z * vec.y
    y = self.z * vec.x - self.x * vec.z
    z = self.x * vec.y - self.y * vec.x
    self.x = x
    self.y = y
    self.z = z

  def sdist(self, vec):
    diff = self.x - vec.x
    sum = diff * diff
    diff = self.y - vec.y
    sum += diff * diff
    diff = self.z - vec.z
    sum += diff * diff
    return sum
