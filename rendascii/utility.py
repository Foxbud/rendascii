"""
This file is part of RendASCII which is released under MIT.
See file LICENSE.txt for full license details.
"""


from rendascii.geometry import matrix, vector


class Transformer:

  def __init__(self, inverse=False):
    # Initialize instance attributes.
    self._inverse = inverse
    self._transformation = matrix.IDENTITY_3D

  def scale(self, scalar):
    if self._inverse:
      self._transformation = matrix.compose(
          self._transformation,
          matrix.scaling_3d(
            1.0 / scalar
            )
          )
    else:
      self._transformation = matrix.compose(
          matrix.scaling_3d(
            scalar
            ),
          self._transformation
          )

    # Return self for convenience.
    return self

  def translate(self, vec):
    if self._inverse:
      self._transformation = matrix.compose(
          self._transformation,
          matrix.translation_3d(
            vector.negate(
              vec
              )
            )
          )
    else:
      self._transformation = matrix.compose(
          matrix.translation_3d(
            vec
            ),
          self._transformation
          )

    # Return self for convenience.
    return self

  def rotate(self, theta, axis_normal):
    if self._inverse:
      self._transformation = matrix.compose(
          self._transformation,
          matrix.rotation_3d(
            -theta,
            axis_normal
            )
          )
    else:
      self._transformation = matrix.compose(
          matrix.rotation_3d(
            theta,
            axis_normal
            ),
          self._transformation
          )

    # Return self for convenience.
    return self

  def apply(self, vec):
    return vector.conv_h_to_3d(
        matrix.transform_3d(
          self._transformation,
          vector.conv_3d_h(
            vec
            )
          )
        )

  def clear(self):
    self._transformation = matrix.IDENTITY_3D

    # Return self for convenience.
    return self

  def get_transformation(self):
    return self._transformation
