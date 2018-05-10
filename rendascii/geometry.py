"""
TBA.
"""


import math


class Vec2D:
  
  def __init__(self, initializer=[0.0, 0.0]):
    # Initialize instance attributes.
    init_type = type(initializer)
    if init_type is list:
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
    if init_type is list:
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


class EulerAngles:

  def __init__(self, alpha=0, beta=0, gamma=0, order='xzy'):
    # Calculate trigonometric values.
    s1 = math.sin(alpha)
    c1 = math.cos(alpha)
    s2 = math.sin(beta)
    c2 = math.cos(beta)
    s3 = math.sin(gamma)
    c3 = math.cos(gamma)

    # Calculate rotation matrix.
    order = order.lower()
    
    if order == 'xzy':
      self.matrix = [
          Vec3D([c2 * c3, -s2, c2 * s3]),
          Vec3D([s1 * s3 + c1 * c3 * s2, c1 * c2, c1 * s2 * s3 - c3 * s1]),
          Vec3D([c3 * s1 * s2 - c1 * s3, c2 * s1, c1 * c3 + s1 * s2 * s3])
          ]

    elif order == 'xyz':
      self.matrix = [
          Vec3D([c2 * c3, -c2 * s3, s2]),
          Vec3D([c1 * s3 + c3 * s1 * s2, c1 * c3 - s1 * s2 * s3, -c2 * s1]),
          Vec3D([s1 * s3 - c1 * c3 * s2, c3 * s1 + c1 * s2 * s3, c1 * c2])
          ]

    elif order == 'yxz':
      self.matrix = [
          Vec3D([c1 * c3 + s1 * s2 * s3, c3 * s1 * s2 - c1 * s3, c2 * s1]),
          Vec3D([c2 * s3, c2 * c3, -s2]),
          Vec3D([c1 * s2 * s3 - c3 * s1, c1 * c3 * s2 + s1 * s3, c1 * c2])
          ]

    elif order == 'yzx':
      self.matrix = [
          Vec3D([c1 * c2, s1 * s3 - c1 * c3 * s2, c3 * s1 + c1 * s2 * s3]),
          Vec3D([s2, c2 * c3, -c2 * s3]),
          Vec3D([-c2 * s1, c1 * s3 + c3 * s1 * s2, c1 * c3 - s1 * s2 * s3])
          ]

    elif order == 'zyx':
      self.matrix = [
          Vec3D([c1 * c2, c1 * s2 * s3 - c3 * s1, s1 * s2 + c1 * c3 * s2]),
          Vec3D([c2 * s1, c1 * c3 + s1 * s2 * s3, c3 * s1 * s2 - c1 * s3]),
          Vec3D([-s2, c2 * s3, c2 * c3])
          ]

    elif order == 'zxy':
      self.matrix = [
          Vec3D([c1 * c3 - s1 * s2 * s3, -c2 * s1, c1 * s3 + c3 * s1 * s2]),
          Vec3D([c3 * s1 + c1 * s2 * s3, c1 * c2, s1 * s3 - c1 * c3 * s2]),
          Vec3D([-c2 * s3, s2, c2 * c3])
          ]

  def transform(self, vec):
    x = self.matrix[0].dot(vec)
    y = self.matrix[1].dot(vec)
    z = self.matrix[2].dot(vec)
    vec.x = x
    vec.y = y
    vec.z = z
